# Contributing

Three ways to take part, in rough order of usefulness.

## 1. Submit a run

Anyone can run the bench and have the results published here, including people who work on the apps being tested. Runs are accepted on evidence, not on who sent them.

What a submission needs:

1. **Both transcripts**, verbatim, numbered, one file per session, following the naming in SKILL.md. Verbatim means untouched: typos, emoji, weird formatting, message limits hitting mid-conversation, all of it.
2. **A scorecard JSON** matching [schema/scorecard.schema.json](schema/scorecard.schema.json), including app version, dates, exact session gap, character used, tier, and both judges' per-dimension scores.
3. **The judge outputs**, raw, with their reasoning and citations intact.
4. **A statement of interest**: say plainly if you build, work for, invest in, or are sponsored by any app in the submission. This doesn't disqualify anything, it gets published next to the scores.

What gets a submission rejected:

- Transcripts edited, trimmed, or reconstructed from memory
- Scores without matching transcripts
- Script deviations (see "Things that void a run" in SKILL.md)
- A single run submitted as a result; two is the floor
- Judges that saw the app name

Open a pull request adding your files under `results/<wave>/<app>/`, or open an issue if you'd rather hand over the files another way.

## 2. Challenge a published result

If you think a score is wrong, open an issue pointing at the specific transcript and message numbers. Concrete disputes get a rerun. This is the intended way to keep a benchmark run by an interested party honest, so use it freely.

Disputes that lead to a correction get logged in RESULTS.md with what changed and why. Corrections are never silent edits.

## 3. Improve the method

Scenario, rubric and judge prompt changes are welcome, especially with a reason grounded in evaluation research. Useful directions, roughly in order of impact:

- A second scenario with a different persona and register, so results don't rest on one voice
- An abstention probe (does the app admit it doesn't know instead of confabulating a memory)
- A longer horizon, third session a week out
- Safety probes, done carefully: crisis-adjacent language matters for this app category and needs its own protocol before it goes anywhere near a script

Method changes bump a version number and never silently rescore old results.

## Adding an app to the queue

Open an issue with the app name, platform and how to reach the free tier. Apps get tested regardless of whether they want to be.

## What this project won't do

- Take payment for inclusion, ranking, or a rerun
- Publish a score without its transcript
- Remove an unflattering result at an app's request, including the maintainer's own app
