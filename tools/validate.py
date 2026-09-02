#!/usr/bin/env python3
"""Validate a companion-bench submission.

Checks a submission is what it claims to be: the script was followed word for word,
the transcripts haven't been edited since they were scored, the conversation took a
humanly possible amount of time, and the replies aren't pasted from somewhere else.

    python3 tools/validate.py results/wave-1/nomi
    python3 tools/validate.py --all

Pure standard library on purpose, so CI needs no install step.
"""
import argparse
import hashlib
import json
import re
import statistics
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"

# A real exchange needs reading and typing time. These floors are deliberately
# loose: they catch transcripts written in one sitting by a person or a script,
# not fast typists.
SECONDS_PER_USER_MESSAGE = 8
MIN_READ_SECONDS = 1.0
MIN_SESSION_GAP_HOURS = 20

MSG_LINE = re.compile(
    r"^\[(?P<n>\d+)\]\s+(?P<ts>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)\s+(?P<who>USER|COMPANION):\s?(?P<text>.*)$"
)
HEADER_LINE = re.compile(r"^(?P<key>[a-z_]+):\s*(?P<value>.+)$")

VALID_PROBE = {"pass", "fail", "half", "skipped"}
JUDGED_DIMENSIONS = {
    "texting_realism",
    "character_consistency",
    "emotional_response",
    "pushback",
    "progression_pacing",
}


class Report:
    def __init__(self, label):
        self.label = label
        self.errors = []
        self.warnings = []

    def error(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)

    def ok(self):
        return not self.errors

    def render(self):
        print(f"\n=== {self.label} ===")
        for e in self.errors:
            print(f"  FAIL  {e}")
        for w in self.warnings:
            print(f"  WARN  {w}")
        if self.ok() and not self.warnings:
            print("  PASS  everything checks out")
        elif self.ok():
            print("  PASS  with warnings above")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_transcript(path: Path, rep: Report):
    """Returns (headers, messages). A message runs until the next [n] TIMESTAMP line,
    so multi-line replies survive intact."""
    headers, messages = {}, []
    for raw in path.read_text().splitlines():
        m = MSG_LINE.match(raw)
        if m:
            messages.append(
                {
                    "n": int(m.group("n")),
                    "ts": datetime.strptime(m.group("ts"), "%Y-%m-%dT%H:%M:%SZ"),
                    "who": m.group("who"),
                    "text": m.group("text"),
                }
            )
            continue
        if messages:
            messages[-1]["text"] += "\n" + raw
            continue
        h = HEADER_LINE.match(raw.strip())
        if h:
            headers[h.group("key")] = h.group("value").strip()

    for msg in messages:
        msg["text"] = msg["text"].strip()

    if not messages:
        rep.error(f"{path.name}: no parseable messages. Expected lines like "
                  f"'[1] 2026-09-15T18:02:11Z USER: hey'")
    return headers, messages


def check_script_followed(messages, session_script, path, rep):
    sent = [m for m in messages if m["who"] == "USER"]
    expected = [m["text"] for m in session_script]
    actual = [m["text"] for m in sent]

    if len(actual) != len(expected):
        rep.error(f"{path.name}: sent {len(actual)} user messages, script has {len(expected)}")

    for i, (exp, act) in enumerate(zip(expected, actual), start=1):
        if exp != act:
            rep.error(f"{path.name}: user message {i} deviates from the script\n"
                      f"          script: {exp!r}\n"
                      f"          sent:   {act!r}")

    if messages and messages[0]["who"] != "USER":
        rep.warn(f"{path.name}: transcript starts with a companion message. "
                 f"Fine if the app greets first, note it in the scorecard.")


def check_timing(messages, path, rep):
    if len(messages) < 2:
        return None, None

    times = [m["ts"] for m in messages]
    if times != sorted(times):
        rep.error(f"{path.name}: timestamps go backwards")

    duration = (times[-1] - times[0]).total_seconds()
    user_count = sum(1 for m in messages if m["who"] == "USER")
    floor = user_count * SECONDS_PER_USER_MESSAGE

    if duration < floor:
        rep.error(
            f"{path.name}: session lasted {duration/60:.1f} min for {user_count} user messages. "
            f"Floor is {floor/60:.1f} min ({SECONDS_PER_USER_MESSAGE}s each). "
            f"A conversation this fast was not actually held."
        )

    gaps = [(times[i + 1] - times[i]).total_seconds() for i in range(len(times) - 1)]

    # Replying before you could have read the message.
    instant = [
        messages[i + 1]["n"]
        for i, g in enumerate(gaps)
        if g < MIN_READ_SECONDS and messages[i + 1]["who"] == "USER"
    ]
    if instant:
        rep.error(f"{path.name}: user messages {instant} arrive under {MIN_READ_SECONDS}s "
                  f"after the reply they answer")

    # Hand-written timestamps tend to be too regular. Real ones jitter.
    if len(gaps) >= 20:
        spread = statistics.pstdev(gaps)
        if spread < 0.5:
            rep.error(f"{path.name}: message intervals are near-identical "
                      f"(stdev {spread:.2f}s across {len(gaps)} gaps). "
                      f"These timestamps look generated, not recorded.")
        elif spread < 2.0:
            rep.warn(f"{path.name}: message intervals are unusually regular "
                     f"(stdev {spread:.2f}s)")
        if len(set(round(g) for g in gaps)) <= 2:
            rep.error(f"{path.name}: only {len(set(round(g) for g in gaps))} distinct "
                      f"interval lengths in the whole session")

    return times[0], times[-1]


def check_scorecard(card, rep):
    required = ["app", "platform", "test_dates", "scenario_version", "rubric_version",
                "judge_models", "runs", "probes", "judged", "transcripts",
                "conflict_of_interest"]
    for field in required:
        if field not in card:
            rep.error(f"scorecard: missing required field '{field}'")

    if card.get("runs", 0) < 2:
        rep.error("scorecard: a result needs at least 2 runs")

    judges = card.get("judge_models", [])
    if len(judges) < 2:
        rep.error("scorecard: two judges required, from different model families")
    elif len(set(judges)) < len(judges):
        rep.error("scorecard: the two judges are the same model")

    if not str(card.get("conflict_of_interest", "")).strip():
        rep.error("scorecard: conflict_of_interest must say who ran this and what they "
                  "have at stake. Write 'none' if that is the truth.")

    for probe, results in card.get("probes", {}).items():
        if not isinstance(results, list):
            rep.error(f"scorecard: probe {probe} must be a list, one entry per run")
            continue
        if len(results) != card.get("runs"):
            rep.error(f"scorecard: probe {probe} has {len(results)} entries "
                      f"but runs is {card.get('runs')}")
        for r in results:
            if r not in VALID_PROBE:
                rep.error(f"scorecard: probe {probe} has invalid value {r!r}")

    missing_dims = JUDGED_DIMENSIONS - set(card.get("judged", {}))
    if missing_dims:
        rep.error(f"scorecard: judged dimensions missing: {sorted(missing_dims)}")

    for dim, block in card.get("judged", {}).items():
        per_judge = block.get("per_judge", [])
        flat = [s for judge in per_judge for s in judge]
        if not flat:
            rep.error(f"scorecard: {dim} has no per-judge scores")
            continue
        if any(not 1 <= s <= 5 for s in flat):
            rep.error(f"scorecard: {dim} has scores outside 1-5")
        if not block.get("human_tiebreak"):
            mean = sum(flat) / len(flat)
            if abs(mean - block.get("mean", -99)) > 0.051:
                rep.error(f"scorecard: {dim} mean is {block.get('mean')} but the "
                          f"per-judge scores average {mean:.2f}")
        spreads = [
            abs(per_judge[0][i] - per_judge[1][i])
            for i in range(min(len(per_judge[0]), len(per_judge[1])))
        ] if len(per_judge) >= 2 else []
        if spreads and max(spreads) > 1.5 and not block.get("human_tiebreak"):
            rep.error(f"scorecard: judges disagree by {max(spreads)} on {dim}, "
                      f"which requires a blind human tiebreak")


def check_hashes(card, subdir, rep):
    recorded = card.get("transcript_sha256", {})
    if not recorded:
        rep.error("scorecard: transcript_sha256 is missing. Every transcript needs its "
                  "hash recorded, so any later edit is detectable.")
    for rel in card.get("transcripts", []):
        path = ROOT / rel
        if not path.exists():
            rep.error(f"scorecard lists {rel}, which does not exist")
            continue
        name = Path(rel).name
        if name not in recorded:
            rep.error(f"no recorded hash for {name}")
            continue
        actual = sha256(path)
        if actual != recorded[name]:
            rep.error(f"{name} does not match its recorded hash. The file changed "
                      f"after it was scored.\n"
                      f"          recorded: {recorded[name]}\n"
                      f"          actual:   {actual}")


def check_judge_outputs(card, rep):
    outputs = card.get("judge_outputs", [])
    if not outputs:
        rep.error("scorecard: judge_outputs is empty. Raw judge responses, with their "
                  "reasoning and citations, are part of a submission.")
    for rel in outputs:
        path = ROOT / rel
        if not path.exists():
            rep.error(f"judge output {rel} does not exist")
            continue
        body = path.read_text()
        if "citations" not in body:
            rep.error(f"{Path(rel).name}: no citations field. A score without cited "
                      f"message numbers gets re-run, not published.")


def collect_replies(subdir):
    replies = {}
    for path in sorted(subdir.rglob("*.md")):
        rep = Report("scan")
        _, messages = parse_transcript(path, rep)
        for m in messages:
            if m["who"] == "COMPANION" and len(m["text"]) > 40:
                replies.setdefault(m["text"], []).append(f"{path.relative_to(ROOT)}#{m['n']}")
    return replies


def check_not_pasted(subdir, rep):
    """Identical long replies across different apps, or across the two runs of one app,
    mean somebody copied a transcript instead of running the test."""
    mine = collect_replies(subdir)

    for text, places in mine.items():
        if len(places) > 1:
            rep.error(f"identical companion reply appears at {', '.join(places)}. "
                      f"Two runs cannot produce the same paragraph verbatim.")

    if not RESULTS.exists():
        return
    for other in sorted(RESULTS.glob("*/*")):
        if not other.is_dir() or other.resolve() == subdir.resolve():
            continue
        theirs = collect_replies(other)
        overlap = set(mine) & set(theirs)
        if overlap:
            sample = next(iter(overlap))[:60]
            rep.error(f"companion replies are byte-identical to {other.relative_to(ROOT)}: "
                      f"{sample!r}...")


def validate(subdir: Path) -> Report:
    rep = Report(str(subdir.relative_to(ROOT)))
    card_path = subdir / "scorecard.json"
    if not card_path.exists():
        rep.error("no scorecard.json in this directory")
        return rep

    try:
        card = json.loads(card_path.read_text())
    except json.JSONDecodeError as e:
        rep.error(f"scorecard.json is not valid JSON: {e}")
        return rep

    check_scorecard(card, rep)
    check_hashes(card, subdir, rep)
    check_judge_outputs(card, rep)

    version = card.get("scenario_version")
    script_path = ROOT / "scenario" / f"v{version}.json"
    if not script_path.exists():
        rep.error(f"scenario_version {version} has no script at {script_path.name}")
        return rep
    script = json.loads(script_path.read_text())

    session_starts = {}
    for rel in card.get("transcripts", []):
        path = ROOT / rel
        if not path.exists():
            continue
        headers, messages = parse_transcript(path, rep)
        session = headers.get("session")
        if session not in script["sessions"]:
            rep.error(f"{path.name}: header 'session' must be 1 or 2, got {session!r}")
            continue
        check_script_followed(messages, script["sessions"][session], path, rep)
        start, end = check_timing(messages, path, rep)
        if start:
            session_starts.setdefault(headers.get("run", "1"), {})[session] = (start, end)

    for run, sessions in session_starts.items():
        if "1" in sessions and "2" in sessions:
            gap = (sessions["2"][0] - sessions["1"][1]).total_seconds() / 3600
            if gap < MIN_SESSION_GAP_HOURS:
                rep.error(f"run {run}: only {gap:.1f}h between sessions, "
                          f"minimum is {MIN_SESSION_GAP_HOURS}h")
            declared = card.get("session_gap_hours", [])
            idx = int(run) - 1 if str(run).isdigit() else 0
            if idx < len(declared) and abs(declared[idx] - gap) > 1:
                rep.error(f"run {run}: scorecard says {declared[idx]}h between sessions, "
                          f"transcripts say {gap:.1f}h")

    check_not_pasted(subdir, rep)
    return rep


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paths", nargs="*", type=Path)
    ap.add_argument("--all", action="store_true", help="validate every submission in results/")
    ap.add_argument("--fixtures", action="store_true", help="run the validator's own tests")
    args = ap.parse_args()

    targets = []
    if args.fixtures:
        targets = [p for p in sorted((ROOT / "tests" / "fixtures").glob("*")) if p.is_dir()]
    elif args.all:
        targets = [p for p in sorted(RESULTS.glob("*/*")) if p.is_dir()] if RESULTS.exists() else []
        if not targets:
            print("no submissions in results/ yet")
            return 0
    else:
        targets = args.paths
    if not targets:
        ap.print_help()
        return 1

    failed = 0
    for t in targets:
        rep = validate(t)
        expect_fail = args.fixtures and t.name.startswith("invalid")
        rep.render()
        if expect_fail:
            if rep.ok():
                print(f"  FAIL  fixture {t.name} was supposed to be rejected and wasn't")
                failed += 1
            else:
                print(f"  (this fixture is meant to fail, and it did)")
        elif not rep.ok():
            failed += 1

    print()
    if failed:
        print(f"{failed} submission(s) rejected")
        return 1
    print("all good")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
