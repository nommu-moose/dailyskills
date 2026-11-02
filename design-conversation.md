# Study skills design

Moved here from the `skills` project session `session-9c1fe123-783a-45c5-8565-51e46a38507e`. DSH will not attach that session to this folder: a session's stored directory is fixed at creation, and a fork keeps the source directory. This file is the conversation. Continue the work in this project.

## What was asked for

Skills for a normal harness, separate from the development bundle, that can:

1. Read a book and condense it for learning. The lens changes the notes: learning a psychology textbook, analysing it, the author's motives and place in the literature, close reading of poetry or literature. Ask for the intended scope. Notes as concise and as broad as a length limit allows, including less obvious notes when the lens earns them, not a default summary every time.
2. Read the user's own notes. Mark what is over-explained, not the core, or verbose without analysis. Tutor a way of thinking that is not their brute-force habit. They still write the notes. Remember the pitfalls they repeat.
3. Keep a record of where they are. Correct a past record when it no longer looks solid. Use it to tutor, to estimate where they should be, and to hurry them or tell them they are ahead. Keeping study on track matters as much as the notes.
4. From summaries of current materials, make plans and new notes so they can learn a part they have no notes for, or learn around notes they already have.
5. Mark essays and coach other ways into the question.
6. One main skill to name when they are unsure. It asks a few simple questions and says which skill to use.

## What the first split got wrong

Four skills, with `study` only as a router that refused to teach, and with "no notes" and "widen around my notes" filed as a mode of note-critique. That dropped ordinary tutoring, and it required notes that do not exist.

## What the second split still got wrong

`studyspan` still started from summaries. It missed: no notes at all, only a vague skeleton of what should be known, and they want tutoring, not a note pack.

## Settled

Five skills. Shared files are not skills. The record lives in a folder the user chooses, and is resumed rather than overwritten.

| Skill | Use when | Do not use when |
| --- | --- | --- |
| `study` | Tutor me, I don't get this, quiz me, am I behind, what should tonight be, or they don't know which skill | They already asked for a condensation, a note critique, a coverage map, or a mark |
| `studyread` | A source is there and they want notes | There is no source, or they want to be taught rather than handed a condensation |
| `studynotes` | Their notes are bloated, core-less, or brute-force | They have no notes, or the notes are fine and they want the surroundings |
| `studyspan` | Summaries or a real core exist, and they want holes filled or the edges widened | They want the book condensed, their prose critiqued, or they have only a skeleton |
| `studymark` | An essay, answer, or problem attempt | They want a replacement essay |

`study` modes:

- **Session.** They can name the concept or the stuck point. Teach, question, check, use the record, hurry or ease off. Notes only as a short example when that is the teaching.
- **Skeleton.** Nothing in front of them, or only a vague list of what should be known. Do not ask for notes, summaries, or a source before teaching. If the list is vague, propose a short working version, mark what was inferred, let them correct it in a sentence, then teach. Do not run an interview. Do not write the subject up as their notes: with no source, that is an invented textbook. Write something down only if they ask, and label it as the sitting's teaching record. An empty record is not a reason to wait. Pace is against the skeleton and the time they have.

`studynotes` still teaches, but only from the notes in front of it. If the real problem is that they do not understand the concept, say so and hand that to `study`.

`studyspan` modes, loaded separately:

- **Gap.** Name what the summaries leave uncovered. Separate "studied, no notes yet" from "never studied". Plan the sitting. Tutor. Scaffolds only, not a substitute chapter. Point at `studyread` only if they decide they want a condensation of a source they actually have.
- **Periphery.** Start from their core. Teach what it assumes, what sits next to it, and what a wider reading changes. Write those notes under a length they set, then say what to add in their own words, what to read, and what not to memorize. Do not restate the core.

Who may write notes:

| Job | Agent-written notes |
| --- | --- |
| Session tutoring | Only a short example, if that is the teaching |
| Skeleton | Not a note pack. A teaching record only if asked, and labelled as one |
| Gap | Scaffolds only |
| Periphery | Yes: the wider map, under their length |
| Source distillation | Yes: the condensation, under the lens and the length |
| Note practice | One short contrast, not a replacement set |
| Essay | Not a replacement essay |

Lenses, for `studyread`, and for periphery when the widening has one. One primary, optional short secondary. A custom lens in one sentence is allowed.

- **Learn.** What has to be usable later: claims, distinctions, conditions, exceptions, application.
- **Analyse.** The text as an argument: assumptions, what does the work, where it strains.
- **Situate.** Author, motive, audience, and what it is answering.
- **Close-read.** Form, diction, ambiguity, what is not said.

Less obvious notes are required when the lens earns them, and kept short under Learn. The length is a budget. If they name none, ask before writing.

When unsure, `study` asks only what it cannot see: what is in front of them, what this sitting should change, and, for a source or for periphery notes, the lens and the length. "Nothing, or only a rough list" selects Skeleton, not `studyspan`, and not "go take notes first".

Record, read by every skill, interpreted by `study`: `INDEX.md`, `POSITION.md`, `CLAIMS.md`, `PACE.md`, `PITFALLS.md`, `LOG.md`. A later sitting downgrades a claim that now looks shaky and says why. It does not silently replace it. Claims distinguish what the user said from what the agent inferred. Thin evidence stays labelled thin. Hurry by naming a specific cut. Ahead means say so and offer widening, not invented work. The other skills add a pace line only when the record shows they are materially off.

Shared references, loaded only when needed: record rules for all five; lenses for `study` and `studyread`, and for periphery when it has a lens; note-judgment for `studyread`, `studynotes`, and periphery. Gap and periphery procedures are separate files.

## Not done

No `SKILL.md` files yet. No installer yet. Next work is writing those in this folder, in the voice of the development bundle: short entrypoints, hard "do not" rules, modes loaded only when selected.
