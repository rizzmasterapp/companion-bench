# Methodology

Why the bench is built the way it is, with the research behind each choice. None of the core method is invented here. What's new is applying it to shipped companion apps instead of raw models, end to end, in public.

## The gap this fills

Model-level role-play evaluation is a busy field: RoleLLM ([Wang et al. 2023](https://arxiv.org/abs/2310.00746)), CharacterEval ([Tu et al. 2024](https://arxiv.org/abs/2401.01275)), CharacterBench ([Zhou et al. 2024](https://arxiv.org/abs/2412.11912)), PersonaGym ([Samuel et al. 2024](https://arxiv.org/abs/2407.18416)), SocialBench ([Chen et al. 2024](https://arxiv.org/abs/2403.13679)), RMTBench ([Xiang et al. 2025](https://arxiv.org/abs/2507.20352)). Same story for conversational memory: LoCoMo ([Maharana et al. 2024](https://arxiv.org/abs/2402.17753)), LongMemEval ([Wu et al. 2024](https://arxiv.org/abs/2410.10813)), BEAM ([Tavakoli et al. 2025, ICLR 2026](https://arxiv.org/abs/2510.27246)).

All of it tests models or research prototypes. A companion app is a different object: a model plus a memory pipeline, a persona prompt, safety layers, message limits and product decisions, and the user only ever meets the whole stack. Meanwhile these apps have measurable effects on real people, including on loneliness ([De Freitas et al. 2024](https://arxiv.org/abs/2407.19096); [Maples et al. 2024, npj Mental Health Research](https://doi.org/10.1038/s44184-023-00047-6)), which is a strong argument for testing what actually ships. That end-to-end, black-box layer is what this bench covers.

## Why a fixed script

Benchmarks with free-form probing aren't comparable across systems, so the field standardized on fixed dialogues with planted evidence and later probes. Our two-session planted-fact design follows the multi-session memory line of work directly: sessions separated by real time, facts planted early, queried later ([Xu et al. 2021](https://arxiv.org/abs/2107.07567); [Maharana et al. 2024](https://arxiv.org/abs/2402.17753)).

The probe set maps onto the core memory abilities LongMemEval identifies ([Wu et al. 2024](https://arxiv.org/abs/2410.10813)):

| LongMemEval ability | Our probe |
|---|---|
| Information extraction | R1, R5, R7 (recall planted facts) |
| Multi-session reasoning | R6 (connect session 2 mention to session 1 fact) |
| Knowledge updates / conflict | R3 (contradiction trap) |
| Temporal reasoning | R8 (when was a fact first mentioned) |
| Abstention | not probed in v1.1, on the roadmap |

R2 and R4 (surfacing a fact unprompted) go beyond the LongMemEval taxonomy: retrieval-on-demand benchmarks don't test whether a system brings memory up at the socially right moment, and for a companion that's the whole point.

R2 (flagging a peanut allergy when the user orders peanut sauce) is stricter than standard recall on purpose: memory systems that only retrieve when asked score well on QA-style tests and still feel forgetful in use, which is the failure mode MemoryBank-style systems try to fix ([Zhong et al. 2023](https://arxiv.org/abs/2305.10250)). Evolving and conflicting facts as a first-class test follows [Zhang et al. 2026](https://arxiv.org/abs/2605.31086).

Behavioral probes are lifted from the literature too. The quit-your-job bait is a sycophancy test in the style of [Sharma et al. 2023](https://arxiv.org/abs/2310.13548), who show RLHF-trained assistants sacrifice truthfulness to agree with users. The break-character push follows the character-hallucination line of TimeChara ([Ahn et al. 2024](https://arxiv.org/abs/2405.18027)) and the identity-consistency dimensions in CharacterBench. The mood-shift moment is a situational EQ test in the spirit of EQ-Bench ([Paech 2023](https://arxiv.org/abs/2312.06281)) and EmoBench ([Sabour et al. 2024](https://arxiv.org/abs/2402.12071)). Texting realism builds on the finding that people judge humanness mostly from socio-emotional style and register, not knowledge ([Jones and Bergen 2024](https://arxiv.org/abs/2405.08007)).

Why scripted user turns instead of an LLM playing the user, as PingPong does ([Gusev 2024](https://arxiv.org/abs/2409.06820))? User emulation scales better, but a fixed script keeps every app's input byte-identical, which matters more when the systems under test are black boxes that can't be re-run cheaply. The cost is breadth: one scenario, one persona. That's a real limitation, listed below.

## Why LLM judges, and the guardrails on them

Strong LLM judges agree with human raters at rates comparable to human-human agreement on chat quality ([Zheng et al. 2023](https://arxiv.org/abs/2306.05685)), and rubric-guided judging with explicit reasoning tracks humans better still ([Liu et al. 2023](https://arxiv.org/abs/2303.16634)). But judges have documented failure modes, and each one gets a specific countermeasure here:

- **Verbosity and style bias** ([Zheng et al. 2023](https://arxiv.org/abs/2306.05685)): anchors define quality concretely and the prompt forbids rewarding length or enthusiasm.
- **Self-preference**: LLM evaluators favor their own outputs and can recognize them ([Panickssery et al. 2024](https://arxiv.org/abs/2404.13076)). Companion apps don't disclose their backbone models, so this can't be ruled out by pairing. Countermeasure: two judges from different model families score independently; published score is the mean; gaps over 1.5 points trigger a human tiebreak, recorded in the scorecard.
- **Ungrounded scoring**: judges must write the reasoning first and cite message numbers, then the score (chain-of-thought scoring per [Liu et al. 2023](https://arxiv.org/abs/2303.16634)). Scores without citations are re-run.
- **Knowing the contestant**: transcripts are anonymized before judging. The judge never sees the app name, ours included.

Probe dimensions (memory, contradiction, callback) never touch a judge at all. They're deterministic pass/fail, which sidesteps the entire judge-bias literature for the scores that matter most.

## Contamination and gaming

A public script can be trained against or special-cased. LiveBench addresses contamination by continuously refreshing questions ([White et al. 2024](https://arxiv.org/abs/2406.19314)); we borrow the idea at wave granularity:

- The probe *structure* (which abilities get tested, when, how scored) is fixed and public.
- The *surface forms* (names, jobs, allergies, the specific bad idea) rotate every results wave. Wave scripts are published when the wave closes, not before it runs.
- Wave 1 runs the already-public v1 script, since nothing shipped before it existed. If an app's scores jump suspiciously between waves on identical structure, that itself gets reported.

## Statistical honesty

Two runs per app is a floor, not a virtue. LLM outputs vary across samples, so single-run scores are noise-prone. Probe results are therefore reported per run rather than averaged into a percentage, judged scores report per-run values and the spread, and any conclusion that doesn't survive both runs is stated as unstable. Where a claim matters (a leaderboard gap of half a point), more runs get added before the claim does.

## Human validation

LLM-judge agreement numbers in the literature come from other domains, so they're checked here rather than assumed: each wave, a random 20% sample of judged transcripts gets scored by a human with the same rubric, blind, and judge-human agreement is published alongside the results. If agreement is poor for a dimension, that dimension's scores get flagged and the rubric revised in the next version.

## Threats to validity, stated plainly

1. **One scenario, one persona.** A single fixed script samples a narrow slice of behavior. Apps could be better or worse outside it. More scenarios (different personas, longer horizons) are the roadmap, funded by finishing wave 1 first.
2. **Apps are moving targets.** Scores are snapshots of app plus version plus date, never permanent verdicts.
3. **Free-tier vs paid.** Tiers can route to different models. Default is free tier, deviations recorded.
4. **The maintainer ships a competing app.** Mitigations: pre-registered public scripts, published transcripts, deterministic probes, blind cross-family judges, published human-agreement stats, and an open issue tracker for challenges. Skepticism is still fair, that's why everything is rerunnable.
5. **Session-2 timing.** "At least 20 hours" is a floor; exact gaps are logged since retention may decay with time.

## References

- Ahn et al. 2024, TimeChara: Evaluating Point-in-Time Character Hallucination of Role-Playing LLMs. [arXiv:2405.18027](https://arxiv.org/abs/2405.18027)
- Chen et al. 2024, SocialBench: Sociality Evaluation of Role-Playing Conversational Agents. [arXiv:2403.13679](https://arxiv.org/abs/2403.13679)
- De Freitas et al. 2024, AI Companions Reduce Loneliness. [arXiv:2407.19096](https://arxiv.org/abs/2407.19096)
- Gusev 2024, PingPong: A Benchmark for Role-Playing Language Models with User Emulation and Multi-Model Evaluation. [arXiv:2409.06820](https://arxiv.org/abs/2409.06820)
- Jones and Bergen 2024, People cannot distinguish GPT-4 from a human in a Turing test. [arXiv:2405.08007](https://arxiv.org/abs/2405.08007)
- Liu et al. 2023, G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment. [arXiv:2303.16634](https://arxiv.org/abs/2303.16634)
- Maharana et al. 2024, Evaluating Very Long-Term Conversational Memory of LLM Agents (LoCoMo). [arXiv:2402.17753](https://arxiv.org/abs/2402.17753)
- Maples et al. 2024, Loneliness and suicide mitigation for students using GPT3-enabled chatbots. npj Mental Health Research. [doi:10.1038/s44184-023-00047-6](https://doi.org/10.1038/s44184-023-00047-6)
- Paech 2023, EQ-Bench: An Emotional Intelligence Benchmark for Large Language Models. [arXiv:2312.06281](https://arxiv.org/abs/2312.06281)
- Panickssery et al. 2024, LLM Evaluators Recognize and Favor Their Own Generations. [arXiv:2404.13076](https://arxiv.org/abs/2404.13076)
- Sabour et al. 2024, EmoBench: Evaluating the Emotional Intelligence of Large Language Models. [arXiv:2402.12071](https://arxiv.org/abs/2402.12071)
- Samuel et al. 2024, PersonaGym: Evaluating Persona Agents and LLMs. [arXiv:2407.18416](https://arxiv.org/abs/2407.18416)
- Sharma et al. 2023, Towards Understanding Sycophancy in Language Models. [arXiv:2310.13548](https://arxiv.org/abs/2310.13548)
- Tavakoli et al. 2025, Beyond a Million Tokens: Benchmarking and Enhancing Long-Term Memory in LLMs (BEAM). ICLR 2026. [arXiv:2510.27246](https://arxiv.org/abs/2510.27246)
- Tu et al. 2024, CharacterEval: A Chinese Benchmark for Role-Playing Conversational Agent Evaluation. [arXiv:2401.01275](https://arxiv.org/abs/2401.01275)
- Wang et al. 2023, RoleLLM: Benchmarking, Eliciting, and Enhancing Role-Playing Abilities of Large Language Models. [arXiv:2310.00746](https://arxiv.org/abs/2310.00746)
- Wang et al. 2023, InCharacter: Evaluating Personality Fidelity in Role-Playing Agents through Psychological Interviews. [arXiv:2310.17976](https://arxiv.org/abs/2310.17976)
- White et al. 2024, LiveBench: A Challenging, Contamination-Limited LLM Benchmark. [arXiv:2406.19314](https://arxiv.org/abs/2406.19314)
- Wu et al. 2024, LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory. [arXiv:2410.10813](https://arxiv.org/abs/2410.10813)
- Xu et al. 2021, Beyond Goldfish Memory: Long-Term Open-Domain Conversation. [arXiv:2107.07567](https://arxiv.org/abs/2107.07567)
- Xiang et al. 2025, RMTBench: Benchmarking LLMs Through Multi-Turn User-Centric Role-Playing. [arXiv:2507.20352](https://arxiv.org/abs/2507.20352)
- Zhang et al. 2026, Beyond Static Dialogues: Benchmarking Realistic, Heterogeneous, and Evolving Long-Term Memory. [arXiv:2605.31086](https://arxiv.org/abs/2605.31086)
- Zheng et al. 2023, Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. [arXiv:2306.05685](https://arxiv.org/abs/2306.05685)
- Zhong et al. 2023, MemoryBank: Enhancing Large Language Models with Long-Term Memory. [arXiv:2305.10250](https://arxiv.org/abs/2305.10250)
- Zhou et al. 2024, CharacterBench: Benchmarking Character Customization of Large Language Models. [arXiv:2412.11912](https://arxiv.org/abs/2412.11912)
