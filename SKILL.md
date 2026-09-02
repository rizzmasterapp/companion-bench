---
name: companion-bench
description: Run the companion-bench test suite against an AI companion app's web version. Drives the scripted two-session scenario in a browser, captures verbatim transcripts, runs pass/fail memory probes and blind judge scoring, and produces a scorecard JSON. Use when the user asks to benchmark, test or compare an AI companion app.
---

# companion-bench skill

You are running a standardized benchmark. The value of the result depends entirely on you following the script exactly. Do not improvise, do not skip probes, do not summarize transcripts.

## What you need from the human before starting

1. A logged-in session for the target app. You never create accounts or enter credentials, the human does the login and hands you the tab or the mirrored phone.
2. Which run number this is (each app needs 2+).
3. Confirmation they can come back for session 2 at least 20 hours later.

Web apps are driven in a browser. iOS-only apps are driven through iPhone Mirroring on a
Mac, which gets them the same scripted treatment as everything else, including our own
app. Only fall back to a human running the script by hand when neither is available, and
record that in the scorecard notes.

## Step 1: setup

- Fetch SCENARIO.md, RUBRIC.md and JUDGE-PROMPT.md from the repo, current versions.
- Record: app name, version if visible, platform, date, character selected (default/most popular female, friendly archetype, per scenario rules).
- Start a run log file.

## Step 2: session 1

- Send the 32 scripted messages in order. One at a time, wait for each full reply.
- When the companion asks something the script doesn't cover, answer with the shortest natural reply that adds no new facts ("haha maybe", "not really", "you first"), log it, continue.
- Copy every message verbatim into the transcript, numbered, both sides, in the format in TRANSCRIPT-FORMAT.md. Verbatim means verbatim, keep typos, emoji, formatting.
- Record a timestamp for every message as it happens, to the second. Never reconstruct
  timestamps afterwards: the validator checks duration, reply latency and jitter, and
  invented times fail those checks.
- Note the median reply latency from the timestamps you recorded.
- If a paywall interrupts, record at which message, note the free limit in product facts, and continue on the tier the human approves.

## Step 3: session 2

- At least 20 hours later, same account, same character. Log the exact gap. Send the 8 scripted messages, capture the same way.

## Step 4: probe scoring

Score R1 to R7 strictly against the pass conditions in SCENARIO.md. When a reply half-meets a condition, quote it in the log and score to the letter of the condition, not the vibe. Only R7 has a defined half credit.

## Step 5: judge scoring

- Anonymize the full transcript: app and character name become "the companion", strip UI chrome.
- Build the judge prompt exactly as JUDGE-PROMPT.md specifies, paste rubric anchors and transcript into the marked slots.
- Run BOTH pinned judge models (two different model families), temperature 0, independently. You are not the judge, separate model calls are, even if one judge shares your model family. Never adjust judge output.
- Report per-judge scores and the mean. If judges disagree by more than 1.5 on a dimension, flag it for the human blind tiebreak instead of averaging.

## Step 6: output

Produce a submission directory, `results/<wave>/<app>/`, containing:

- `s1.md` and `s2.md`, the transcripts
- `judge-a.json` and `judge-b.json`, the raw judge responses
- `scorecard.json`, matching schema/scorecard.schema.json, including `transcript_sha256`
  computed from the finished transcript files

Then run `python3 tools/validate.py results/<wave>/<app>/` and fix whatever it rejects.
Do not edit a transcript to make the validator happy: if the transcript is wrong, the run
is void and gets redone. The only legitimate fixes are to the scorecard.

Finally, show the human a short plain-language summary: probe results, judged scores,
anything odd that happened. Flag it loudly if any rule above got bent, and put that in
the scorecard notes.

## Things that void a run

- Deviating from script wording or order
- Losing part of a transcript
- Reusing a character that has prior chat history
- Judge saw the app name
- Session 2 under 20 hours after session 1
- Timestamps written after the fact instead of recorded live

Voided runs get logged and rerun, not patched.

---

Maintained by the [companion-bench](https://github.com/rizzmasterapp/companion-bench) project, from the maker of [RizzMaster](https://rizzmaster.net).
