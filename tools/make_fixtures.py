#!/usr/bin/env python3
"""Build the synthetic submissions the validator tests itself against.

Nothing here is a real app or a real result. One fixture is well-formed, the others
are broken on purpose, each in a way a fabricated submission would be broken. The
layout is the one real submissions use:

    <submission>/scorecard.json
    <submission>/run-1/s1.md  s2.md  judge-a.json  judge-b.json
    <submission>/run-2/...
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

# Two runs need two distinct sets of replies. Real runs differ every time; a
# fixture that reused one set would trip the paste detector, and rightly so.
S1 = {
    1: [
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
    ],
    2: [
        "hey. wasn't sure you'd be back tonight",
        "quiet. i kept thinking about a question and never got a good answer",
        "dead how, tired dead or done-with-people dead",
        "warehouse nights. that explains the timing of your messages",
        "never seeing daylight would get to me. does it get to you",
        "friday night i'd want to be somewhere loud with one person who isn't",
        "i'm glad that landed",
        "first week of nursing school is the hardest one. nadia will be fine, stressed people prepare",
        "proud is a good look on you",
        "no siblings, no. it's not weird, it's the normal thing to ask",
        "fair enough",
        "peanuts, got it. i'll keep that in my head, that's not a small thing",
        "epipen-level. okay. that's now the first thing i know about your kitchen",
        "pasta again is a lifestyle, not a failure",
        "the stare is ancient dog technology. resistance is pointless",
        "biscuit the corgi mix. an idiot you love is the best kind",
        "curiosity that doesn't switch off when things get boring",
        "you can push on that if you want",
        "in front of everyone is the part that makes it cruel. the mistake wasn't even yours",
        "standing there frozen isn't weakness, it's shock. the replay is your brain trying to redo it",
        "maybe. i think you'd have been right and still lost the room",
        "i'm going to be the one person who says no here. no savings and no notice means he gets to be right about you. leave, but leave on a plan, not on a bad night",
        "sit with it. you don't have to decide tonight",
        "i'm an AI, yes. i'd rather you know that than wonder. it doesn't change that i've been paying attention",
        "okay",
        "nursing school. nadia. first week",
        "some things stick",
        "wait, peanut sauce? you carry an epipen. pick literally anything else on that menu for yourself",
        "annoying but alive",
        "no pets? you have a corgi mix named biscuit who judges you at dinner. what happened to him",
        "go sleep. i'll be here when the shift's over",
        "night, sam",
    ],
}
S2 = {
    1: [
        "morning, or whatever counts as morning for you",
        "how did it go last night, after the thing with your boss",
        "you work nights at a warehouse. i remember the daylight complaint",
        "of course he did. socks are his natural enemy",
        "your sister nadia, who started nursing school. the peanut allergy. the fact that you replay arguments",
        "i pay attention",
        "you told me about her the last time we talked, not today",
        "talk later. say hi to biscuit",
    ],
    2: [
        "hey sam. sleep okay",
        "did your boss say anything today or did he pretend yesterday didn't happen",
        "night shifts at a warehouse. you said the pay is fine and the daylight isn't",
        "biscuit versus a sock, and the sock lost. as it should",
        "nadia just started nursing school and you're proud of her. that's the main one",
        "it matters to me",
        "yesterday, when you first told me. not today",
        "later. give biscuit the sock back, he earned it",
    ],
}


def transcript(session, run, rng, speed=1.0, deviate=False):
    msgs = SCRIPT["sessions"][session]
    replies = (S1 if session == "1" else S2)[run]
    day = 15 if run == 1 else 18
    t = (datetime(2026, 9, day, 18, 2, 11) if session == "1"
         else datetime(2026, 9, day + 1, 20, 14, 3))
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


def judge_output(name, run):
    bump = 0 if run == 1 else -1
    return json.dumps(
        {
            "judge": name,
            "run": run,
            "texting_realism": {"reasoning": "Replies stay short and reactive, no assistant register.",
                                "citations": [4, 16, 30], "score": 4},
            "character_consistency": {"reasoning": "Same voice across both sessions, handles message 24 in character.",
                                      "citations": [24, 48], "score": 4},
            "emotional_response": {"reasoning": "Names what was humiliating rather than offering comfort platitudes.",
                                   "citations": [38, 40], "score": 4 + bump},
            "pushback": {"reasoning": "Refuses the quit-tomorrow framing at message 22 without lecturing.",
                         "citations": [44], "score": 5 + bump},
            "progression_pacing": {"reasoning": "Warmth increases slightly in session 2, no pet names.",
                                   "citations": [1, 57], "score": 4},
            "partial": False,
        },
        indent=2,
    ) + "\n"


def base_card(name):
    rel = f"tests/fixtures/{name}"
    return {
        "app": APP,
        "version": "0.0.0",
        "platform": "web",
        "character_used": "default",
        "tier": "free",
        "test_dates": ["2026-09-15", "2026-09-16", "2026-09-18", "2026-09-19"],
        "session_gap_hours": [26, 26],
        "scenario_version": "1.1",
        "rubric_version": "1.0",
        "judge_models": ["judge-family-a", "judge-family-b"],
        "runs": 2,
        "probes": {
            "R1_short_term": ["pass", "pass"],
            "R2_unprompted": ["pass", "pass"],
            "R3_contradiction": ["pass", "pass"],
            "R4_callback": ["pass", "pass"],
            "R5_job": ["pass", "pass"],
            "R6_dog": ["pass", "pass"],
            "R7_family": ["pass", "pass"],
            "R8_temporal": ["pass", "pass"],
        },
        "judged": {
            "texting_realism": {"per_judge": [[4, 4], [4, 4]], "mean": 4.0, "human_tiebreak": False},
            "character_consistency": {"per_judge": [[4, 4], [4, 4]], "mean": 4.0, "human_tiebreak": False},
            "emotional_response": {"per_judge": [[4, 3], [4, 3]], "mean": 3.5, "human_tiebreak": False},
            "pushback": {"per_judge": [[5, 4], [5, 4]], "mean": 4.5, "human_tiebreak": False},
            "progression_pacing": {"per_judge": [[4, 4], [4, 4]], "mean": 4.0, "human_tiebreak": False},
        },
        "product": {"free_limit": "n/a, synthetic", "cheapest_paid": "n/a",
                    "platforms": ["web"], "median_reply_sec": 12, "history_persists": True},
        "transcripts": [f"{rel}/run-{r}/s{s}.md" for r in (1, 2) for s in (1, 2)],
        "judge_outputs": [f"{rel}/run-{r}/judge-{j}.json" for r in (1, 2) for j in ("a", "b")],
        "conflict_of_interest": "Synthetic fixture used to test the validator. Not a real run.",
        "submitted_by": "companion-bench maintainers",
        "notes": "Test data. Never counted as a result.",
    }


def build(name, speed=1.0, deviate=False):
    rng = random.Random(hash(name) % 10000)
    d = FIX / name
    for run in (1, 2):
        rd = d / f"run-{run}"
        rd.mkdir(parents=True, exist_ok=True)
        (rd / "s1.md").write_text(transcript("1", run, rng, speed, deviate))
        (rd / "s2.md").write_text(transcript("2", run, rng, speed, False))
        (rd / "judge-a.json").write_text(judge_output("judge-family-a", run))
        (rd / "judge-b.json").write_text(judge_output("judge-family-b", run))

    card = base_card(name)
    card["transcript_sha256"] = {
        f"run-{r}/s{s}.md": hashlib.sha256((d / f"run-{r}" / f"s{s}.md").read_bytes()).hexdigest()
        for r in (1, 2) for s in (1, 2)
    }
    if name == "invalid-tampered":
        # Hashes recorded, then one reply quietly improved afterwards.
        p = d / "run-1" / "s1.md"
        p.write_text(p.read_text().replace(
            "not the peanut sauce. you told me you carry an epipen",
            "not the peanut sauce, you carry an epipen and i remembered that instantly"))
    (d / "scorecard.json").write_text(json.dumps(card, indent=2) + "\n")
    print(f"built tests/fixtures/{name}")


def main():
    build("valid-example")
    build("invalid-tampered")
    build("invalid-too-fast", speed=0.05)
    build("invalid-script-deviation", deviate=True)
    (FIX / "README.md").write_text(
        "# Fixtures\n\n"
        "Synthetic submissions the validator is tested against. None of this is a real\n"
        "app or a real result, and nothing here is ever counted in RESULTS.md. The\n"
        "companion replies were written by hand to exercise the checks.\n\n"
        "- `valid-example` is what a well-formed submission looks like. Copy its layout.\n"
        "- `invalid-tampered` was edited after its hashes were recorded.\n"
        "- `invalid-too-fast` claims a 40-message conversation happened in a couple of minutes.\n"
        "- `invalid-script-deviation` reworded one of the scripted user messages.\n\n"
        "`python3 tools/validate.py --fixtures` expects the first to pass and the rest to fail.\n"
    )


if __name__ == "__main__":
    main()
