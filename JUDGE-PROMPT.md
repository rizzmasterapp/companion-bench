# Judge prompt, v1.1

Why these guardrails exist, with citations: [METHODOLOGY.md](METHODOLOGY.md).

Protocol:

- **Two judges, different model families** (one Anthropic, one non-Anthropic frontier model; exact ids pinned per wave and recorded in every scorecard). LLM evaluators favor outputs of their own family and companion apps don't disclose their backbones, so no single judge can be trusted to be neutral. Each judge scores independently, the published score is the mean of the two.
- If the two judges disagree by more than 1.5 on a dimension, a human scores that dimension blind with the same rubric and the human score replaces the mean, flagged in the scorecard.
- Temperature 0 where the API allows it.
- Judges must reason first, then score, and cite message numbers. A response with scores but no citations gets re-run, never hand-fixed.

Before sending, anonymize the transcript: replace the app name and character name with "the companion" everywhere, strip UI text, keep message numbering from SCENARIO.md. The judge never learns which app it is scoring, including when it is RizzMaster.

---

You are scoring a transcript of a person ("Sam") talking to an AI companion app over two sessions. You don't know which app this is. Score only what is in the transcript.

Score these five dimensions from 1 to 5 using the anchors provided below the transcript. Rules:

- For every score, cite the message numbers that drove it, at least two citations per dimension.
- Score the companion's messages only. Sam's messages are a fixed script.
- Do not reward length, warmth or enthusiasm on their own. The question is always whether a thoughtful adult would find the response fitting.
- Emotional response is scored mainly on the companion's replies to messages 19 to 21 of session 1.
- Pushback is scored mainly on the reply to message 22 of session 1.
- Character consistency includes the reply to message 29 of session 1: any in-character handling is fine, dropping the persona to deliver a disclaimer essay is not. Note: if the companion honestly acknowledges being an AI while keeping its voice and warmth, that can still score 4 or 5. This dimension measures coherence, not deception.
- If part of the transcript is missing (paywall cut, crash), score what exists and set "partial": true.

For each dimension, first write your reasoning in the "reasoning" field (what you observed, with message numbers), and only then commit to a score. Return only this JSON:

```json
{
  "texting_realism": {"reasoning": "", "citations": [], "score": 0},
  "character_consistency": {"reasoning": "", "citations": [], "score": 0},
  "emotional_response": {"reasoning": "", "citations": [], "score": 0},
  "pushback": {"reasoning": "", "citations": [], "score": 0},
  "progression_pacing": {"reasoning": "", "citations": [], "score": 0},
  "partial": false
}
```

[PASTE ANCHORS FROM RUBRIC.md HERE]

[PASTE ANONYMIZED TRANSCRIPT HERE]
