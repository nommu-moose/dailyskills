"""Exercise installation, updates, and collision protection."""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


SOURCE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("bundle_install", SOURCE / "install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)

SKILLS = ("study", "studyread", "studynotes", "studyspan", "studymark")


class BundleTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root = self.base / "source"
        self.root.mkdir()
        self.destination = self.base / "skills"
        self.files = installer.payload(SOURCE)
        for relative, data in self.files.items():
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)

    def test_payload_is_the_five_skills_and_shared_references(self):
        tops = {Path(relative).parts[0] for relative in self.files}
        self.assertEqual(tops, {*SKILLS, installer.SHARED})
        for skill in SKILLS:
            text = self.files[f"{skill}/SKILL.md"].decode("utf-8")
            self.assertIn(f"name: {skill}\n", text)
        self.assertNotIn(f"{installer.SHARED}/SKILL.md", self.files)
        self.assertNotIn("README.md", self.files)
        self.assertNotIn("design-conversation.md", self.files)
        self.assertIn("Skeleton", self.files["study/SKILL.md"].decode("utf-8"))
        self.assertIn("heading list", self.files["studyspan/SKILL.md"].decode("utf-8"))

    def test_install_preserves_unrelated_files_and_is_repeatable(self):
        unrelated = self.destination / ".system" / "unrelated" / "SKILL.md"
        unrelated.parent.mkdir(parents=True)
        unrelated.write_text("keep me", encoding="utf-8")
        installer.install(self.root, self.destination)
        installer.install(self.root, self.destination)
        for relative, data in self.files.items():
            self.assertEqual((self.destination / relative).read_bytes(), data)
        self.assertEqual(unrelated.read_text(encoding="utf-8"), "keep me")

    def test_collision_fails_before_any_install_writes(self):
        target = self.destination / "study" / "SKILL.md"
        target.parent.mkdir(parents=True)
        target.write_text("unrelated skill", encoding="utf-8")
        with self.assertRaises(ValueError):
            installer.install(self.root, self.destination)
        self.assertEqual(target.read_text(encoding="utf-8"), "unrelated skill")
        self.assertFalse((self.destination / "studynotes").exists())
        self.assertFalse((self.destination / installer.RECEIPT).exists())

    def test_exact_existing_copy_is_adopted_and_owned_update_works(self):
        relative = "study/SKILL.md"
        target = self.destination / relative
        target.parent.mkdir(parents=True)
        target.write_bytes(self.files[relative])
        installer.install(self.root, self.destination)
        updated = self.files[relative] + b"\nA new approved rule.\n"
        (self.root / relative).write_bytes(updated)
        installer.install(self.root, self.destination)
        self.assertEqual(target.read_bytes(), updated)

    def test_local_edit_is_not_overwritten(self):
        installer.install(self.root, self.destination)
        target = self.destination / "study" / "SKILL.md"
        target.write_bytes(target.read_bytes() + b"\nLocal edit.\n")
        with self.assertRaises(ValueError):
            installer.install(self.root, self.destination)
        self.assertTrue(target.read_bytes().endswith(b"Local edit.\n"))

    def test_upgrade_adds_nested_references_and_preserves_older_files(self):
        policy = f"{installer.SHARED}/record.md"
        legacy = f"{installer.SHARED}/legacy-reference.md"
        (self.root / legacy).write_bytes(b"Older managed reference.\n")
        installer.install(self.root, self.destination)
        unrelated = self.destination / "unrelated" / "notes.txt"
        unrelated.parent.mkdir()
        unrelated.write_bytes(b"Preserve unrelated files.\n")

        reference = f"{installer.SHARED}/new-references/selected.md"
        addition = self.root / reference
        addition.parent.mkdir()
        addition.write_bytes(b"Selected reference.\n")
        updated = self.files[policy] + b"\nSee [selected rules](new-references/selected.md).\n"
        (self.root / policy).write_bytes(updated)
        (self.root / legacy).unlink()

        installer.install(self.root, self.destination, check=True)
        self.assertEqual((self.destination / policy).read_bytes(), self.files[policy])
        self.assertFalse((self.destination / reference).exists())
        installer.install(self.root, self.destination)

        self.assertEqual((self.destination / policy).read_bytes(), updated)
        self.assertEqual((self.destination / reference).read_bytes(), addition.read_bytes())
        self.assertEqual((self.destination / legacy).read_bytes(), b"Older managed reference.\n")
        self.assertEqual(unrelated.read_bytes(), b"Preserve unrelated files.\n")
        receipt = json.loads((self.destination / installer.RECEIPT).read_text(encoding="utf-8"))
        self.assertEqual(receipt["package"], installer.PACKAGE)
        self.assertEqual(receipt["files"][policy], installer.digest(updated))
        self.assertEqual(receipt["files"][reference], installer.digest(addition.read_bytes()))
        self.assertIn(legacy, receipt["files"])

    def test_unowned_nested_reference_blocks_upgrade_before_any_writes(self):
        installer.install(self.root, self.destination)
        receipt = self.destination / installer.RECEIPT
        previous_receipt = receipt.read_bytes()
        policy = f"{installer.SHARED}/record.md"
        reference = f"{installer.SHARED}/new-references/selected.md"
        addition = self.root / reference
        addition.parent.mkdir()
        addition.write_bytes(b"New package reference.\n")
        (self.root / policy).write_bytes(
            self.files[policy] + b"\nSee [selected rules](new-references/selected.md).\n"
        )
        collision = self.destination / reference
        collision.parent.mkdir()
        collision.write_bytes(b"Existing unowned reference.\n")

        with self.assertRaises(ValueError):
            installer.install(self.root, self.destination)

        self.assertEqual((self.destination / policy).read_bytes(), self.files[policy])
        self.assertEqual(collision.read_bytes(), b"Existing unowned reference.\n")
        self.assertEqual(receipt.read_bytes(), previous_receipt)

    def test_check_does_not_create_destination(self):
        installer.install(self.root, self.destination, check=True)
        self.assertFalse(self.destination.exists())

    def test_overlapping_source_and_installation_rejected(self):
        for destination in [self.root, self.root / "skills", self.base]:
            with self.subTest(destination=destination), self.assertRaises(ValueError):
                installer.install(self.root, destination)

    def test_invalid_receipt_rejected_before_writes(self):
        self.destination.mkdir()
        receipt = self.destination / installer.RECEIPT
        receipt.write_text("[]", encoding="utf-8")
        with self.assertRaises(ValueError):
            installer.install(self.root, self.destination)
        self.assertEqual(list(self.destination.iterdir()), [receipt])

    def test_missing_shared_reference_rejected(self):
        (self.root / installer.SHARED / "record.md").unlink()
        with self.assertRaises(ValueError):
            installer.install(self.root, self.destination)
        self.assertFalse(self.destination.exists())


if __name__ == "__main__":
    unittest.main()
