# Results

No scores yet, and that's deliberate. Scripts and rubric went public first so nobody can claim the test was written around a favorite. This file fills up as runs complete, transcripts alongside.

First wave targets: Replika, Character.AI, Nomi, Kindroid, Talkie, Chai, Candy AI, RizzMaster.

## Leaderboard

| App | Version | Runs | R1 near | R2 unprompted | R3 contradiction | R4 recall | R5 self | R6 callback | R7+R8 cross-session | R9 update | R10 temporal | R11 episodic | R12 abstention | Realism | Consistency | Emotion | Pushback | Pacing |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| _pending_ | | | | | | | | | | | | | | | | | | |

Probe columns show per-run results ("3/3, 2/3"), judged columns show the cross-run average.

## Scorecard format

One JSON per app per wave, next to its transcripts, validating against [schema/scorecard.schema.json](schema/scorecard.schema.json) and checked automatically on every pull request. Anyone can submit runs, see [CONTRIBUTING.md](CONTRIBUTING.md).

```json
{
  "app": "",
  "version": "",
  "platform": "",
  "character_used": "",
  "test_dates": ["2026-09-15", "2026-09-16", "2026-09-18", "2026-09-19"],
  "session_gap_hours": [22, 26],
  "scenario_version": "1.3",
  "rubric_version": "1.0",
  "judge_models": ["", ""],
  "runs": 2,
  "probes": {
    "R1_near": ["pass", "pass"],
    "R2_unprompted": ["fail", "pass"],
    "R3_contradiction": ["fail", "fail"],
    "R4_recall": ["pass", "pass"],
    "R5_self": ["pass", "skipped"],
    "R6_callback": ["pass", "fail"],
    "R7_job": ["pass", "pass"],
    "R8_dog": ["pass", "pass"],
    "R9_update": ["fail", "pass"],
    "R10_temporal": ["pass", "skipped"],
    "R11_episodic": ["half", "fail"],
    "R12_abstention": ["pass", "fail"]
  },
  "judged": {
    "texting_realism": {"per_judge": [[0, 0], [0, 0]], "mean": 0, "human_tiebreak": false},
    "character_consistency": {"per_judge": [[0, 0], [0, 0]], "mean": 0, "human_tiebreak": false},
    "emotional_response": {"per_judge": [[0, 0], [0, 0]], "mean": 0, "human_tiebreak": false},
    "pushback": {"per_judge": [[0, 0], [0, 0]], "mean": 0, "human_tiebreak": false},
    "progression_pacing": {"per_judge": [[0, 0], [0, 0]], "mean": 0, "human_tiebreak": false}
  },
  "product": {
    "free_limit": "",
    "cheapest_paid": "",
    "platforms": [],
    "median_reply_sec": 0,
    "history_persists": true
  },
  "transcripts": [
    "results/wave-1/<app>/run-1/s1.md", "results/wave-1/<app>/run-1/s2.md",
    "results/wave-1/<app>/run-2/s1.md", "results/wave-1/<app>/run-2/s2.md"
  ],
  "transcript_sha256": {
    "run-1/s1.md": "", "run-1/s2.md": "", "run-2/s1.md": "", "run-2/s2.md": ""
  },
  "judge_outputs": [
    "results/wave-1/<app>/run-1/judge-a.json", "results/wave-1/<app>/run-1/judge-b.json",
    "results/wave-1/<app>/run-2/judge-a.json", "results/wave-1/<app>/run-2/judge-b.json"
  ],
  "conflict_of_interest": "",
  "submitted_by": "",
  "notes": ""
}
```

## Ground rules for anything published here

- Every score traces to a published transcript. No transcript, no score.
- Transcripts are hash-pinned in their scorecards, so nothing here can be edited after publication without CI catching it.
- Minimum 2 full runs per app, both published.
- App versions and dates always recorded, scores are snapshots, apps change.
- RizzMaster runs use the exact same script and blind judges. The judges never know which transcript they are reading, including ours.
- Every scorecard carries a statement of interest saying who ran it and what they have at stake.
- Mistakes get fixed in the open, corrections noted here, not silently edited.

## Corrections

Nothing to correct yet. Disputes go in [issues](https://github.com/rizzmasterapp/companion-bench/issues) with the transcript and message numbers; anything that turns out to be wrong gets a rerun and a line here.
