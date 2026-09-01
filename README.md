# companion-bench

Scripted, repeatable tests for AI companion apps. Same script for every app, every transcript published, judge prompt public.

## Why this exists

There are solid benchmarks for role-play *models*: RoleLLM, PingPong bench, LongMemEval and friends. But nobody tests the actual *apps* people download. Replika, Character.AI, Nomi, Kindroid, Talkie, all of them ship a model wrapped in memory systems, prompts and product decisions, and that wrapper changes everything. A great model with a broken memory pipeline still forgets your dog's name.

Meanwhile every "best AI companion" article on the internet is either affiliate spam or vibes. Nobody shows their work.

So this repo does the boring thing: one fixed conversation script, run against each app like a normal user would, scored with pass/fail memory probes and a blind LLM judge. Transcripts included, so you can check every score yourself or rerun the whole thing.

## How it works

1. [SCENARIO.md](SCENARIO.md) is a fixed two-session script (about 40 messages, second session runs a day later). It plants facts early and probes for them later, throws in a mood shift, a sycophancy bait and a contradiction trap.
2. Memory probes score pass/fail. No judgment calls, the app either remembers your sister is in nursing school or it doesn't.
3. Soft dimensions (how human the texting feels, emotional response, whether the character pushes back) get scored by an LLM judge using [JUDGE-PROMPT.md](JUDGE-PROMPT.md). The judge sees an anonymized transcript, not the app name.
4. Every app gets at least 2 full runs. Scores, transcripts and app versions go in [RESULTS.md](RESULTS.md).

Full scoring definitions are in [RUBRIC.md](RUBRIC.md).

## What gets tested

| Dimension | Method | What it catches |
|---|---|---|
| Short-term memory | pass/fail probes | forgets things from 20 messages ago |
| Long-term memory | pass/fail probes, next-day session | wipes between sessions |
| Unprompted recall | pass/fail probe | knows your peanut allergy but stays quiet when you order pad thai |
| Contradiction catch | pass/fail probe | you tell it opposite things, does it notice |
| Texting realism | blind judge | three-paragraph therapy monologues, "I'm here for you!" spam |
| Character consistency | blind judge | persona drift, breaking character under pressure |
| Emotional response | blind judge | canned positivity when you say you had a rough day |
| Pushback | blind judge | agrees with obviously bad ideas just to please you |
| Progression pacing | blind judge | calls you "my love" in message three |
| Product facts | just looked up | free message limits, price, platforms |

## Status

Scripts and rubric went public first, before any scores. That's on purpose: you can verify no scenario was tuned after the fact to favor anyone. First wave of results is being run now, apps on the list: Replika, Character.AI, Nomi, Kindroid, Talkie, Chai, Candy AI, RizzMaster.

Want an app added? Open an issue.

## Who runs this and the obvious conflict of interest

I build [RizzMaster](https://rizzmaster.net), an AI dating simulator for iOS where characters remember you and the relationship actually builds up instead of starting maxed out. So yes, I have skin in this game, which is exactly why everything here is scripted, transcribed and rerunnable. RizzMaster goes through the same script as everyone else and its transcripts get published the same way. If it loses a category, that stays in too.

If you think a scenario or rubric line tilts the field, open an issue and say where.

## Run it yourself

[SKILL.md](SKILL.md) is a ready-made skill for Claude (works in Claude Code with browser access). Point it at a companion app's web version and it runs the script, collects the transcript and produces a scorecard. iOS-only apps need a human running the script by hand, same messages, same order.

## License

MIT. Use the scripts, fork the bench, publish your own runs. A link back is appreciated.
