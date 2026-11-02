#!/usr/bin/env python3
"""Install this skill bundle into a harness skills directory. Requires Python 3.10+."""

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import tempfile


ROOT = Path(__file__).resolve().parent
SHARED = "dailyskills-shared"
RECEIPT = ".dailyskills-install.json"
PACKAGE = "moose.dailyskills"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def plain_path(path, root):
    """Reject redirected paths inside the chosen source or destination root."""
    for item in [path, *path.parents]:
        if item == root:
            break
        if item.is_symlink() or getattr(item, "is_junction", lambda: False)():
            raise ValueError(f"Linked path requires manual review: {item}")


def payload(root):
    files = {}
    skills = sorted(p for p in root.iterdir() if (p / "SKILL.md").is_file())
    if not skills or not (root / SHARED).is_dir():
        raise ValueError("Incomplete bundle: skill folders or shared references missing.")
    for folder in [*skills, root / SHARED]:
        if folder in skills:
            name = folder.name
            if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", name):
                raise ValueError(f"Invalid skill folder: {name}")
            text = (folder / "SKILL.md").read_text(encoding="utf-8-sig")
            header = text.split("---", 2)
            if len(header) != 3 or header[0].strip() or not re.search(
                rf"^name: {re.escape(name)}\s*$", header[1], re.MULTILINE
            ) or not re.search(r"^description: .+", header[1], re.MULTILINE):
                raise ValueError(f"Missing or mismatched skill metadata: {name}")
        plain_path(folder, root)
        for path in sorted(folder.rglob("*")):
            plain_path(path, root)
            if path.is_file() and "__pycache__" not in path.parts:
                files[path.relative_to(root).as_posix()] = path.read_bytes()
    check_links(files)
    return files


def check_links(files):
    for relative, data in files.items():
        if not relative.endswith(".md"):
            continue
        for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", data.decode("utf-8-sig")):
            if "://" in link or link.startswith(("#", "mailto:")):
                continue
            target = link.split("#", 1)[0]
            resolved = os.path.normpath(str(PurePosixPath(relative).parent / target)).replace("\\", "/")
            if resolved not in files:
                raise ValueError(f"Unpackaged reference in {relative}: {link}")


def atomic_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix=".dailyskills-", dir=path.parent)
    try:
        with os.fdopen(handle, "wb") as stream:
            stream.write(data)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def install(root, destination, check=False):
    files = payload(root)
    destination = destination.expanduser().resolve()
    if destination == root or destination.is_relative_to(root) or root.is_relative_to(destination):
        raise ValueError("Keep the source bundle and installation directory in separate directory trees.")
    receipt_path = destination / RECEIPT
    plain_path(receipt_path, destination)
    previous = {}
    if receipt_path.exists():
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        if not isinstance(receipt, dict) or receipt.get("package") != PACKAGE or receipt.get("format") != 1:
            raise ValueError(f"Unrecognised installation receipt: {receipt_path}")
        previous = receipt.get("files", {})
        if not isinstance(previous, dict) or any(
            not isinstance(k, str) or not isinstance(v, str) for k, v in previous.items()
        ):
            raise ValueError("Invalid installation receipt file list.")

    changed, conflicts = {}, []
    for relative, data in files.items():
        target = destination / relative
        plain_path(target, destination)
        for parent in target.parents:
            if parent == destination:
                break
            if parent.exists() and not parent.is_dir():
                conflicts.append(str(parent))
        if target.exists():
            if not target.is_file():
                conflicts.append(str(target))
                continue
            current = target.read_bytes()
            if current == data:
                continue
            if digest(current) != previous.get(relative):
                conflicts.append(str(target))
                continue
        changed[relative] = data
    if destination.exists() and not destination.is_dir():
        conflicts.append(str(destination))
    if conflicts:
        raise ValueError("No files installed. Conflicting or locally modified files:\n" + "\n".join(sorted(set(conflicts))))
    if check:
        print(f"Ready: {len(changed)} new/updated, {len(files) - len(changed)} identical files in {destination}")
        return

    for relative, data in changed.items():
        atomic_write(destination / relative, data)
    recorded = {**previous, **{p: digest(data) for p, data in files.items()}}
    receipt = {"package": PACKAGE, "format": 1, "files": recorded}
    atomic_write(receipt_path, (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    print(f"Installed: {len(changed)} new/updated, {len(files) - len(changed)} identical files in {destination}")
    if set(previous) - set(files):
        print("Older managed files were retained; this installer never deletes installed files.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dest", type=Path, required=True, help="Harness skills directory")
    parser.add_argument("--check", action="store_true", help="Check an installation without writing")
    args = parser.parse_args()
    try:
        install(ROOT, args.dest, args.check)
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
