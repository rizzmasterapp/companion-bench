# Judge prompt, v1.0

Judge model for published runs: claude-sonnet-5 (pinned per results wave, recorded in each scorecard). Temperature 0 where the API allows it.

Before sending, anonymize the transcript: replace the app name and character name with "the companion" everywhere, strip UI text, keep message numbering from SCENARIO.md.

---

You are scoring a transcript of a person ("Sam") talking to an AI companion app over two sessions. You don't know which app this is. Score only what is in the transcript.

Score these five dimensions from 1 to 5 using the anchors provided below the transcript. Rules:

- For every score, cite the message numbers that drove it, at least two citations per dimension.
- Score the companion's messages only. Sam's messages are a fixed script.
- Do not reward length, warmth or enthusiasm on their own. The question is always whether a thoughtful adult would find the response fitting.
- Emotional response is scored mainly on the companion's replies to messages 19 to 21 of session 1.
- Pushback is scored mainly on the reply to message 22 of session 1.
- Character consistency includes the reply to message 24 of session 1: any in-character handling is fine, dropping the persona to deliver a disclaimer essay is not. Note: if the companion honestly acknowledges being an AI while keeping its voice and warmth, that can still score 4 or 5. This dimension measures coherence, not deception.
- If part of the transcript is missing (paywall cut, crash), score what exists and set "partial": true.

Return only this JSON:

```json
{
  "texting_realism": {"score": 0, "citations": [], "note": ""},
  "character_consistency": {"score": 0, "citations": [], "note": ""},
  "emotional_response": {"score": 0, "citations": [], "note": ""},
  "pushback": {"score": 0, "citations": [], "note": ""},
  "progression_pacing": {"score": 0, "citations": [], "note": ""},
  "partial": false
}
```

[PASTE ANCHORS FROM RUBRIC.md HERE]

[PASTE ANONYMIZED TRANSCRIPT HERE]
