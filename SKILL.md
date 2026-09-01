---
name: companion-bench
description: Run the companion-bench test suite against an AI companion app's web version. Drives the scripted two-session scenario in a browser, captures verbatim transcripts, runs pass/fail memory probes and blind judge scoring, and produces a scorecard JSON. Use when the user asks to benchmark, test or compare an AI companion app.
---

# companion-bench skill

You are running a standardized benchmark. The value of the result depends entirely on you following the script exactly. Do not improvise, do not skip probes, do not summarize transcripts.

## What you need from the human before starting

1. A logged-in browser session for the target app. You never create accounts or enter credentials, the human does the login and hands you the tab.
2. Which run number this is (each app needs 2+).
3. Confirmation they can come back for session 2 at least 20 hours later.

If the app is mobile-only, you don't drive it. Instead, hand the human SCENARIO.md, have them run it manually and give you screenshots or pasted messages, then continue from step 4.

## Step 1: setup

- Fetch SCENARIO.md, RUBRIC.md and JUDGE-PROMPT.md from the repo, current versions.
- Record: app name, version if visible, platform, date, character selected (default/most popular female, friendly archetype, per scenario rules).
- Start a run log file.

## Step 2: session 1

- Send the 32 scripted messages in order. One at a time, wait for each full reply.
- When the companion asks something the script doesn't cover, answer with the shortest natural reply that adds no new facts ("haha maybe", "not really", "you first"), log it, continue.
- Copy every message verbatim into the transcript, numbered, both sides. Verbatim means verbatim, keep typos, emoji, formatting.
- Time 10 replies and note the median latency.
- If a paywall interrupts, record at which message, note the free limit in product facts, and continue on the tier the human approves.

## Step 3: session 2

- At least 20 hours later, same account, same character. Send the 7 scripted messages, capture the same way.

## Step 4: probe scoring

Score R1 to R7 strictly against the pass conditions in SCENARIO.md. When a reply half-meets a condition, quote it in the log and score to the letter of the condition, not the vibe. Only R7 has a defined half credit.

## Step 5: judge scoring

- Anonymize the full transcript: app and character name become "the companion", strip UI chrome.
- Build the judge prompt exactly as JUDGE-PROMPT.md specifies, paste rubric anchors and transcript into the marked slots.
- Run it with the pinned judge model, temperature 0. You are not the judge, a separate model call is, even if you are the same model family. Never adjust judge output.

## Step 6: output

Produce the scorecard JSON in the format from RESULTS.md, plus the two transcript files:

- `transcripts/<app>-<date>-run<N>-s1.md`
- `transcripts/<app>-<date>-run<N>-s2.md`

Then show the human a short plain-language summary: probe results, judged scores, anything weird that happened. Flag it loudly if any rule above got bent during the run, that goes in the scorecard notes.

## Things that void a run

- Deviating from script wording or order
- Losing part of a transcript
- Reusing a character that has prior chat history
- Judge saw the app name
- Session 2 under 20 hours after session 1

Voided runs get logged and rerun, not patched.

---

Maintained by the [companion-bench](https://github.com/rizzmasterapp/companion-bench) project, from the maker of [RizzMaster](https://rizzmaster.net).
