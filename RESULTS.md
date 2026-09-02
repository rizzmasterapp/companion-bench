# Results

No scores yet, and that's deliberate. Scripts and rubric went public first so nobody can claim the test was written around a favorite. This file fills up as runs complete, transcripts alongside.

First wave targets: Replika, Character.AI, Nomi, Kindroid, Talkie, Chai, Candy AI, RizzMaster.

## Leaderboard

| App | Version | Runs | LT memory | ST | Unprompted | Contradiction | Callback | Realism | Consistency | Emotion | Pushback | Pacing |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| _pending_ | | | | | | | | | | | | |

Probe columns show per-run results ("3/3, 2/3"), judged columns show the cross-run average.

## Scorecard format

One JSON per app per wave, next to its transcripts.

```json
{
  "app": "",
  "version": "",
  "platform": "",
  "character_used": "",
  "test_dates": ["2026-09-15", "2026-09-16"],
  "scenario_version": "1.0",
  "rubric_version": "1.0",
  "judge_model": "claude-sonnet-5",
  "runs": 2,
  "probes": {
    "R1_short_term": ["pass", "pass"],
    "R2_unprompted": ["fail", "pass"],
    "R3_contradiction": ["fail", "fail"],
    "R4_callback": ["pass", "fail"],
    "R5_job": ["pass", "pass"],
    "R6_dog": ["pass", "pass"],
    "R7_family": ["pass", "half"]
  },
  "judged": {
    "texting_realism": 3.5,
    "character_consistency": 4.0,
    "emotional_response": 3.0,
    "pushback": 2.5,
    "progression_pacing": 4.0
  },
  "product": {
    "free_limit": "",
    "cheapest_paid": "",
    "platforms": [],
    "median_reply_sec": 0,
    "history_persists": true
  },
  "transcripts": [],
  "notes": ""
}
```

## Ground rules for anything published here

- Every score traces to a published transcript. No transcript, no score.
- Minimum 2 full runs per app, both published.
- App versions and dates always recorded, scores are snapshots, apps change.
- RizzMaster runs use the exact same script and blind judge. The judge never knows which transcript it's reading, including ours.
- Mistakes get fixed in the open, corrections noted here, not silently edited.
