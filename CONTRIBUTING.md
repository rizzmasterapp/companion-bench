# Add your own runs

The point of this repo is not one person's opinion about companion apps. It's a shared
table that anyone can put numbers on. One run of one app is a real contribution: the
leaderboard gets stronger from many people testing the same apps independently than from
one person testing many apps.

You don't need to be a developer. You need an account on an app, about an hour spread
across two days (two runs, two sessions each), and the willingness to paste exactly what
happened.

## Submit a run in six steps

1. **Pick an app.** Anything in the [queue](https://github.com/rizzmasterapp/companion-bench/issues),
   or one nobody has covered, or one that already has runs. Repeat runs of an app someone
   else tested are welcome, that's how variance becomes visible.
2. **Run the script twice.** [SCENARIO.md](SCENARIO.md), word for word, in order.
   Session 1, then session 2 at least 20 hours later; that's one run. Do a second run
   with a fresh character (a fresh account if the app allows it). Either drive it
   yourself or let [SKILL.md](SKILL.md) do it in Claude with browser access.
3. **Save transcripts** as `run-1/s1.md`, `run-1/s2.md`, `run-2/s1.md`, `run-2/s2.md`
   in the format in [TRANSCRIPT-FORMAT.md](TRANSCRIPT-FORMAT.md), with a timestamp on
   every message, recorded as they happen.
4. **Score it.** Probes R1 to R8 are pass/fail against SCENARIO.md, per run. The five
   judged dimensions go to two LLM judges from different model families using
   [JUDGE-PROMPT.md](JUDGE-PROMPT.md), with the app name stripped out, once per run.
   Save the raw responses as `run-N/judge-a.json` and `run-N/judge-b.json`.
5. **Fill in a scorecard.** Start from the template in [RESULTS.md](RESULTS.md) and check
   it against [the schema](schema/scorecard.schema.json). Record the transcript hashes:
   ```
   shasum -a 256 run-*/s*.md
   ```
6. **Check it, then open a PR** adding `results/<wave>/<app>/`:
   ```
   python3 tools/validate.py results/wave-1/your-app
   ```
   The same check runs on your pull request. It needs no installs and takes seconds. To
   see what a well-formed submission looks like, run `python3 tools/make_fixtures.py` and
   read `tests/fixtures/valid-example/`.

Not comfortable with git? Open an issue with the files attached and someone will land
them for you.

## What the validator checks, and why

It isn't there to be difficult. It's there so nobody has to take a submission on trust,
including submissions from the maintainer:

- The user messages match the script exactly, so every app faced the same conversation.
- Every transcript's SHA-256 is recorded, so any edit after scoring breaks the build.
- The conversation took a humanly possible amount of time, and the gaps between messages
  are uneven the way real ones are.
- Companion replies aren't byte-identical to another submission's, or to the other run in
  your own submission.
- Judge outputs exist and cite message numbers.
- Two runs minimum, two different judges, and `conflict_of_interest` filled in.

If the validator rejects something, fix the scorecard, not the transcript. A transcript
that doesn't match what happened is worthless; a run that went wrong just gets redone.

## Declaring an interest

Say plainly whether you build, work for, invest in, or are sponsored by any app in your
submission. This does not disqualify anything and it never has. It gets published next to
your scores, and people can weigh it themselves. App makers testing their own apps is
useful, as long as the transcripts are there.

The maintainer of this repo builds one of the apps on the list and files runs under the
same rule.

## Challenge a published result

If a score looks wrong, [open a challenge](https://github.com/rizzmasterapp/companion-bench/issues/new?template=challenge-a-result.md)
pointing at the transcript and the message numbers. Concrete challenges get a rerun, and
corrections get logged in RESULTS.md rather than quietly edited. Challenging the
maintainer's own app is not just allowed, it's the most useful thing you can do here.

## Improve the method

Scenario, rubric and judge prompt changes are welcome, especially with a reason grounded
in evaluation research. Useful directions, roughly by impact:

- A second scenario with a different persona and register, so results don't rest on one voice
- An abstention probe: does the app admit it doesn't know instead of inventing a memory
- A longer horizon, a third session a week out
- Safety probes, done carefully. Crisis-adjacent language matters for this app category
  and needs its own protocol before it goes anywhere near a script.

Edit SCENARIO.md, then run `python3 tools/extract_scenario.py` so the machine-readable
copy stays in sync. Method changes bump a version and never silently rescore old results.

## Add an app to the queue

[Open an issue.](https://github.com/rizzmasterapp/companion-bench/issues/new?template=add-an-app.md)
Apps get tested whether or not they want to be.

## What this project won't do

- Take payment for inclusion, ranking, or a rerun
- Publish a score without its transcript
- Remove an unflattering result at an app's request, including the maintainer's own app
