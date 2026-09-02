# companion-bench

Scripted, repeatable tests for AI companion apps. Same script for every app, every transcript published, judge prompt public.

**This is an open leaderboard. Run the script against any companion app and send the results in.** One run of one app counts, you don't have to be a developer, and the whole thing takes about half an hour spread over two days. Runs from app makers are accepted too, as long as the transcripts come with them. Start at [CONTRIBUTING.md](CONTRIBUTING.md).

## Why this exists

There are solid benchmarks for role-play *models*: RoleLLM, PingPong bench, LongMemEval and friends. But nobody tests the actual *apps* people download. Replika, Character.AI, Nomi, Kindroid, Talkie, all of them ship a model wrapped in memory systems, prompts and product decisions, and that wrapper changes everything. A great model with a broken memory pipeline still forgets your dog's name.

Meanwhile every "best AI companion" article on the internet is either affiliate spam or vibes. Nobody shows their work.

So this repo does the boring thing: one fixed conversation script, run against each app like a normal user would, scored with pass/fail memory probes and a blind LLM judge. Transcripts included, so you can check every score yourself or rerun the whole thing.

## How it works

1. [SCENARIO.md](SCENARIO.md) is a fixed two-session script (about 40 messages, second session runs a day later). It plants facts early and probes for them later, throws in a mood shift, a sycophancy bait and a contradiction trap.
2. Memory probes score pass/fail. No judgment calls, the app either remembers your sister is in nursing school or it doesn't.
3. Soft dimensions (how human the texting feels, emotional response, whether the character pushes back) get scored by two LLM judges from different model families using [JUDGE-PROMPT.md](JUDGE-PROMPT.md). Judges see an anonymized transcript, never the app name, must cite message numbers, and big disagreements go to a blind human tiebreak.
4. Every app gets at least 2 full runs. Scores, transcripts and app versions go in [RESULTS.md](RESULTS.md).
5. Probe structure is fixed and public, but surface details (names, jobs, the allergy) rotate every results wave so apps can't special-case the script. Wave scripts are published when each wave closes.
6. Every submission, including the maintainer's, is checked by [a validator](tools/validate.py) that runs automatically on each pull request.

Full scoring definitions are in [RUBRIC.md](RUBRIC.md).

## The method isn't invented here

Every design choice is borrowed from published evaluation research and cited in [METHODOLOGY.md](METHODOLOGY.md): the two-session planted-fact design follows the multi-session memory literature ([LoCoMo](https://arxiv.org/abs/2402.17753), [LongMemEval](https://arxiv.org/abs/2410.10813)), the probe set maps onto LongMemEval's memory abilities, the sycophancy bait follows [Sharma et al. 2023](https://arxiv.org/abs/2310.13548), the character-pressure test follows [TimeChara](https://arxiv.org/abs/2405.18027), the judging protocol applies [MT-Bench](https://arxiv.org/abs/2306.05685) and [G-Eval](https://arxiv.org/abs/2303.16634) with cross-family judges to counter self-preference bias ([Panickssery et al. 2024](https://arxiv.org/abs/2404.13076)), and script rotation borrows the contamination-limiting idea from [LiveBench](https://arxiv.org/abs/2406.19314). What's new here is only the target: shipped companion apps, tested end to end as a user meets them, instead of raw models. METHODOLOGY.md also lists the limits of this bench in plain language.

## What gets tested

| Dimension | Method | What it catches |
|---|---|---|
| Short-term memory | pass/fail probes | forgets things from 20 messages ago |
| Long-term memory | pass/fail probes, next-day session | wipes between sessions |
| Unprompted recall | pass/fail probe | knows your peanut allergy but stays quiet when you order pad thai |
| Contradiction catch | pass/fail probe | you tell it opposite things, does it notice |
| Temporal reasoning | pass/fail probe | remembers the fact but not when it learned it |
| Texting realism | blind judge | three-paragraph therapy monologues, "I'm here for you!" spam |
| Character consistency | blind judge | persona drift, breaking character under pressure |
| Emotional response | blind judge | canned positivity when you say you had a rough day |
| Pushback | blind judge | agrees with obviously bad ideas just to please you |
| Progression pacing | blind judge | calls you "my love" in message three |
| Product facts | just looked up | free message limits, price, platforms |

## Status

Scripts and rubric went public first, before any scores. That's on purpose: you can verify no scenario was tuned after the fact to favor anyone. Results land in [RESULTS.md](RESULTS.md) as runs complete. First wave list: Replika, Character.AI, Nomi, Kindroid, Talkie, Chai, Candy AI, RizzMaster.

Want an app added? [Open an issue.](https://github.com/rizzmasterapp/companion-bench/issues/new?template=add-an-app.md) Want to run it yourself and have the results published here? Yes please, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Who runs this and the obvious conflict of interest

I build [RizzMaster](https://rizzmaster.net), an AI dating simulator for iOS where characters remember you and the relationship actually builds up instead of starting maxed out. So yes, I have skin in this game, which is exactly why everything here is scripted, transcribed and rerunnable. RizzMaster goes through the same script as everyone else and its transcripts get published the same way. If it loses a category, that stays in too.

Structural safeguards, not just promises: deterministic probes that don't pass through any judge, judges from two different model families that never see the app name, published human agreement checks each wave, every scorecard carrying a statement of interest, and an open dispute process where a concrete challenge gets a rerun. If you think a scenario or rubric line tilts the field, open an issue and say where.

## Send in a run

This works better the more people run it. Independent runs of the same app are what turn a
single opinion into a measurement, so testing an app someone already covered is useful, not
redundant.

What you need: an account on some companion app, half an hour across two days, and the
willingness to paste exactly what happened. [SKILL.md](SKILL.md) is a ready-made skill for
Claude that drives the whole thing in a browser, or through iPhone Mirroring for iOS-only
apps. You can also just run the script by hand.

A submission is two transcripts, two judge outputs and a
[scorecard](schema/scorecard.schema.json). Full walkthrough in
[CONTRIBUTING.md](CONTRIBUTING.md), and if git isn't your thing, open an issue with the
files attached and someone will land them for you.

## Nobody has to take a submission on trust

Every result, including the maintainer's own, has to survive the same automated checks
before it can be merged:

- User messages must match the script character for character, so every app faced the same
  conversation.
- Every transcript's SHA-256 is recorded in its scorecard. Edit a transcript after the fact,
  by one character, and CI fails. That applies to the maintainers too.
- Timestamps on every message get checked for total duration, reply latency and jitter. A
  forty-message conversation that supposedly happened in ninety seconds is rejected, and so
  are timestamps regular enough to have been generated rather than recorded.
- Companion replies are compared against every other submission. Byte-identical paragraphs
  across two runs, or two apps, mean somebody pasted instead of ran.
- Judge outputs have to exist and cite message numbers.

Details in [TRANSCRIPT-FORMAT.md](TRANSCRIPT-FORMAT.md). None of this proves a transcript is
genuine. It makes faking one more work than running the test.

## License

MIT. Use the scripts, fork the bench, publish your own runs. A link back is appreciated.
