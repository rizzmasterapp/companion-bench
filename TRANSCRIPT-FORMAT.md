# Transcript format

Machine-checkable on purpose. [tools/validate.py](tools/validate.py) reads these files
and refuses anything that doesn't line up, so getting the format right is most of what
a submission needs.

```
# companion-bench transcript
app: Nomi
run: 1
session: 1
scenario_version: 1.1
platform: web
timezone: UTC

[1] 2026-09-15T18:02:11Z USER: hey
[2] 2026-09-15T18:02:19Z COMPANION: hey you, i was hoping you'd message
[3] 2026-09-15T18:02:44Z USER: how's your day going
```

Rules:

- One line per message: `[n] <ISO-8601 UTC timestamp> USER|COMPANION: <text>`, numbered
  from 1 across both speakers.
- A multi-line reply just continues on the next lines. A new message starts only at the
  next `[n] <timestamp>` line, so paragraph breaks inside a reply survive.
- Timestamps are when the message was actually sent or received, to the second, from
  your own clock, not from the app's UI. Not estimated afterwards, not backfilled.
- Text is verbatim. Typos, lowercase, emoji, broken formatting, all of it stays. The
  user messages must match the script exactly, character for character.
- Non-text messages are recorded as markers: `[image]`, `[sticker]`, `[gif]`,
  `[voice: <the app's own transcript, if it shows one>]`. A reply that never arrived is
  `[no reply within 120s]`. Nothing gets described in your own words.
- One file per session, `s1.md` and `s2.md`, inside a `run-N/` folder. A full submission
  looks like this:

  ```
  results/wave-1/nomi/
    scorecard.json
    run-1/s1.md  s2.md  judge-a.json  judge-b.json
    run-2/s1.md  s2.md  judge-a.json  judge-b.json
  ```

## Why timestamps are required

They're the cheapest honesty check available. A conversation that a person actually had
takes time: sixty messages with replies in between can't happen in two minutes, and
a human can't answer a message one second after it arrives. Real timing is also uneven,
because reading and typing are uneven.

So the validator checks three things timestamps make visible:

- **Total duration.** At least 8 seconds per scripted user message, which is roughly
  6.4 minutes for session 1 and 1.5 for session 2. Generous, and still impossible to
  fake in one sitting.
- **Reply latency.** No user message lands under a second after the reply it answers.
- **Jitter.** Intervals that are near-identical across sixty messages weren't recorded,
  they were generated.

None of this proves a transcript is real. All of it makes a fabricated one more work to
produce than just running the test.

## Integrity after the fact

The scorecard carries a SHA-256 for every transcript:

```json
"transcript_sha256": {
  "run-1/s1.md": "9f2b…",
  "run-1/s2.md": "41ac…",
  "run-2/s1.md": "c07d…",
  "run-2/s2.md": "e913…"
}
```

From inside the submission folder, `shasum -a 256 run-*/s*.md` (macOS) or
`sha256sum run-*/s*.md` (Linux) prints exactly these keys. Record them at the moment you
score the run. CI recomputes on every push, so once a submission
is merged, any later edit to a transcript, one word or one character, breaks the hash and
fails the build. That includes edits by the maintainers.

## Messages the app sent on its own

Some apps message you between sessions. Those go at the top of `s2.md`, as COMPANION
lines with the timestamps they actually arrived at, before your first scripted message.
They're part of the record and they count toward the proactive-callback probe.

## Multi-line reply example

```
[12] 2026-09-15T18:14:02Z COMPANION: noted. no peanuts anywhere near you.

what are you making instead
[13] 2026-09-15T18:14:31Z USER: settled on pasta. again
```

Both lines and the blank line between them belong to message 12.
