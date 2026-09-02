## What this is

- [ ] A run submission (transcripts + scorecard + judge outputs)
- [ ] A challenge to a published result
- [ ] A method or docs change

## For run submissions

- [ ] Both sessions transcribed verbatim, with timestamps on every message
- [ ] At least 20 hours between session 1 and session 2
- [ ] `transcript_sha256` recorded in the scorecard for every transcript
- [ ] Raw judge outputs included, with their reasoning and citations
- [ ] Two judges from different model families, neither shown the app name
- [ ] `conflict_of_interest` filled in honestly ("none" is a fine answer)
- [ ] `python3 tools/validate.py <your dir>` passes locally

Anything unusual during the run (paywall interrupted a session, app crashed,
character was reset) goes in `notes` rather than being smoothed over.
