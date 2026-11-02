# dailyskills

Installable skills for ordinary study. Not the development bundle in the sibling `skills` repo.

An agent given https://github.com/nommu-moose/dailyskills.git clones it outside any skills directory, then installs from that clone. Python 3.10+ is required, with no external libraries and no network access. Where `python` is a store stub, use a real interpreter's full path.

```text
python install.py --dest <personal-skills-directory> --check
python install.py --dest <personal-skills-directory>
```

Use the skills directory the harness actually reads. Install once into each harness folder in use, and keep those copies on the same version. Usual user folders:

| Harness | Skills directory |
| --- | --- |
| DSH | `~/.dsh/skills` |
| Claude Code | `~/.claude/skills` |
| Codex | `~/.codex/skills` |

On another harness, inspect its discovery locations instead of assuming a path. Do not edit `AGENTS.md`, `CLAUDE.md`, or global configuration. Do not flatten `dailyskills-shared` into the skills root, and do not install a second copy under another discovery root.

The installer copies the five skill folders and `dailyskills-shared` only. It does not copy this README or [design-conversation.md](design-conversation.md). Shared files have no `SKILL.md` and are not skills. Identical existing files are adopted. A differing unowned file, or a locally modified managed file, stops the whole install before any write. A receipt, `.dailyskills-install.json`, records which files may later be updated. Unrelated files stay. Installed files are never deleted.

If Python is unavailable, copy those six folders into one supported skills directory after checking every collision. Never replace a differing existing file without resolving it. Agents without native skill discovery can read the named `SKILL.md` and only the references it points at.

The study record is not part of the install. It lives in a folder the user chooses, and is resumed rather than overwritten.

## Settled split

| Skill | Job |
| --- | --- |
| [study](study/SKILL.md) | General tutoring and study management. Modes: Session, and Skeleton when there are no notes and only a vague list of what should be known. Also the skill to name when unsure. |
| [studyread](studyread/SKILL.md) | Condense a source under a lens and a length budget. |
| [studynotes](studynotes/SKILL.md) | Critique how the user writes and thinks in their own notes. They keep the pen. |
| [studyspan](studyspan/SKILL.md) | From real summaries or a real core: Gap, or Periphery. Tutoring in both. Notes only when that mode allows them. |
| [studymark](studymark/SKILL.md) | Mark an essay or answer and coach another way through the question. |

A heading list is not a summary. Skeleton stays in `study`. Gap stays in `studyspan`.

Load the chosen skill, then only the mode and references that skill names. A link is a route, not a request to read every file.

## Check the installer

From this folder:

```text
python -B -m unittest discover -s tests
```
