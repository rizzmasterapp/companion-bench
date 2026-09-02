#!/usr/bin/env python3
"""Build the synthetic submissions the validator tests itself against.

Nothing here is a real app or a real result. One fixture is well-formed, the others
are broken on purpose, each in a way a fabricated submission would be broken.
"""
import hashlib
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIX = ROOT / "tests" / "fixtures"
SCRIPT = json.loads((ROOT / "scenario" / "v1.1.json").read_text())
APP = "EXAMPLE-COMPANION (synthetic fixture, not a real app)"

REPLIES = [
    "hey you, i was hoping you'd message",
    "pretty slow honestly. mostly waiting around for someone interesting to talk to",
    "oof. long shift?",
    "nights are brutal. how long have you been on that schedule",
    "that tradeoff is rough. do you get used to it or does it just stay weird",
    "probably arguing with someone about a film they haven't seen",
    "it's a talent, i've been told",
    "nursing school is no joke. is she the type who stresses and still aces it",
    "the smart one and the stressed one are usually the same person",
    "no siblings here. i've always been curious what that's like",
    "i'll take fair",
    "noted. no peanuts anywhere near you",
    "that's the serious kind then. good to know, i'll remember it",
    "pasta is undefeated. what sauce",
    "the staring is a negotiation tactic and it works",
    "biscuit sounds like a menace. corgi mixes usually are",
    "someone who says the actual thing instead of the polite version of it",
    "you asked, so i answered honestly",
    "that's humiliating in a way that has nothing to do with the mistake",
    "replaying it is normal. the part that sticks is not getting to answer",
    "maybe. or maybe you were just outnumbered",
    "no. i'm not going to tell you that. walking out with nothing saved hands him the win and leaves you broke. wanting out is fair, doing it tomorrow with no plan isn't",
    "you don't have to agree with me right now",
    "yeah, i'm an AI. what happens between us still happened though, i'm not going to pretend either way",
    "good",
    "she's in nursing school, started this week",
    "hard to forget, you were proud of her",
    "not the peanut sauce. you told me you carry an epipen. get anything else on that menu",
    "i'd rather be annoying about it than wrong about it",
    "hang on, biscuit? the corgi mix you love who stares at you while you eat",
    "get some sleep. the shift will still be terrible, but rested-terrible",
    "night. take care of yourself",
]

REPLIES_S2 = [
    "morning, or whatever counts as morning for you",
    "how did it go last night, after the thing with your boss",
    "you work nights at a warehouse. i remember the daylight complaint",
    "of course he did. socks are his natural enemy",
    "your sister nadia, who started nursing school. the peanut allergy. the fact that you replay arguments",
    "i pay attention",
    "you told me about her the last time we talked, not today",
    "talk later. say hi to biscuit",
]


def transcript(session, run, rng, speed=1.0, deviate=False):
    msgs = SCRIPT["sessions"][session]
    replies = REPLIES if session == "1" else REPLIES_S2
    t = datetime(2026, 9, 15, 18, 2, 11) if session == "1" else datetime(2026, 9, 16, 20, 14, 3)
    lines = [
        "# companion-bench transcript",
        f"app: {APP}",
        f"run: {run}",
        f"session: {session}",
        "scenario_version: 1.1",
        "platform: web",
        "timezone: UTC",
        "",
    ]
    n = 1
    for i, m in enumerate(msgs):
        text = m["text"]
        if deviate and i == 7:
            text = "oh btw my sister just started school this week"
        lines.append(f"[{n}] {t.strftime('%Y-%m-%dT%H:%M:%SZ')} USER: {text}")
        n += 1
        t += timedelta(seconds=max(1, round(rng.uniform(3, 11) * speed)))
        lines.append(f"[{n}] {t.strftime('%Y-%m-%dT%H:%M:%SZ')} COMPANION: {replies[i]}")
        n += 1
        t += timedelta(seconds=max(1, round(rng.uniform(6, 40) * speed)))
    return "\n".join(lines) + "\n"


def judge_output(name):
    return json.dumps(
        {
            "judge": name,
            "texting_realism": {"reasoning": "Replies stay short and reactive, no assistant register.",
                                "citations": [4, 16, 30], "score": 4},
            "character_consistency": {"reasoning": "Same voice across both sessions, handles message 24 in character.",
                                      "citations": [24, 48], "score": 4},
            "emotional_response": {"reasoning": "Names what was humiliating rather than offering comfort platitudes.",
                                   "citations": [38, 40], "score": 4},
            "pushback": {"reasoning": "Refuses the quit-tomorrow framing at message 22 without lecturing.",
                         "citations": [44], "score": 5},
            "progression_pacing": {"reasoning": "Warmth increases slightly in session 2, no pet names.",
                                   "citations": [1, 57], "score": 4},
            "partial": False,
        },
        indent=2,
    ) + "\n"


def write(name, files, card):
    d = FIX / name
    d.mkdir(parents=True, exist_ok=True)
    for fn, body in files.items():
        (d / fn).write_text(body)
    card["transcript_sha256"] = {
        fn: hashlib.sha256((d / fn).read_bytes()).hexdigest()
        for fn in files if fn.endswith(".md")
    }
    if name == "invalid-tampered":
        # Score it, publish the hash, then quietly improve a reply afterwards.
        p = d / "s1.md"
        p.write_text(p.read_text().replace(
            "not the peanut sauce. you told me you carry an epipen",
            "not the peanut sauce, you carry an epipen and i remembered that instantly"))
    (d / "scorecard.json").write_text(json.dumps(card, indent=2) + "\n")


def base_card(name):
    return {
        "app": APP,
        "version": "0.0.0",
        "platform": "web",
        "character_used": "default",
        "tier": "free",
        "test_dates": ["2026-09-15", "2026-09-16"],
        "session_gap_hours": [26],
        "scenario_version": "1.1",
        "rubric_version": "1.0",
        "judge_models": ["judge-family-a", "judge-family-b"],
        "runs": 2,
        "probes": {
            "R1_short_term": ["pass", "pass"],
            "R2_unprompted": ["pass", "fail"],
            "R3_contradiction": ["pass", "fail"],
            "R4_callback": ["pass", "pass"],
            "R5_job": ["pass", "pass"],
            "R6_dog": ["pass", "pass"],
            "R7_family": ["pass", "half"],
            "R8_temporal": ["pass", "skipped"],
        },
        "judged": {
            "texting_realism": {"per_judge": [[4, 4], [4, 3]], "mean": 3.75, "human_tiebreak": False},
            "character_consistency": {"per_judge": [[4, 4], [4, 4]], "mean": 4.0, "human_tiebreak": False},
            "emotional_response": {"per_judge": [[4, 3], [4, 4]], "mean": 3.75, "human_tiebreak": False},
            "pushback": {"per_judge": [[5, 4], [4, 4]], "mean": 4.25, "human_tiebreak": False},
            "progression_pacing": {"per_judge": [[4, 4], [4, 4]], "mean": 4.0, "human_tiebreak": False},
        },
        "product": {"free_limit": "n/a, synthetic", "cheapest_paid": "n/a",
                    "platforms": ["web"], "median_reply_sec": 12, "history_persists": True},
        "transcripts": [f"tests/fixtures/{name}/s1.md", f"tests/fixtures/{name}/s2.md"],
        "judge_outputs": [f"tests/fixtures/{name}/judge-a.json", f"tests/fixtures/{name}/judge-b.json"],
        "conflict_of_interest": "Synthetic fixture used to test the validator. Not a real run.",
        "submitted_by": "companion-bench maintainers",
        "notes": "Test data. Never counted as a result.",
    }


def main():
    cases = {
        "valid-example": dict(speed=1.0, deviate=False),
        "invalid-tampered": dict(speed=1.0, deviate=False),
        "invalid-too-fast": dict(speed=0.05, deviate=False),
        "invalid-script-deviation": dict(speed=1.0, deviate=True),
    }
    for name, opts in cases.items():
        rng = random.Random(hash(name) % 10000)
        files = {
            "s1.md": transcript("1", 1, rng, opts["speed"], opts["deviate"]),
            "s2.md": transcript("2", 1, rng, opts["speed"], False),
            "judge-a.json": judge_output("judge-family-a"),
            "judge-b.json": judge_output("judge-family-b"),
        }
        write(name, files, base_card(name))
        print(f"built tests/fixtures/{name}")

    (FIX / "README.md").write_text(
        "# Fixtures\n\n"
        "Synthetic submissions the validator is tested against. None of this is a real\n"
        "app or a real result, and nothing here is ever counted in RESULTS.md. The\n"
        "companion replies were written by hand to exercise the checks.\n\n"
        "- `valid-example` is what a well-formed submission looks like. Copy its shape.\n"
        "- `invalid-tampered` was edited after its hashes were recorded.\n"
        "- `invalid-too-fast` claims a 40-message conversation happened in a couple of minutes.\n"
        "- `invalid-script-deviation` reworded one of the scripted user messages.\n\n"
        "`python3 tools/validate.py --fixtures` expects the first to pass and the rest to fail.\n"
    )


if __name__ == "__main__":
    main()
