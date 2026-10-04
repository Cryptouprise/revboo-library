# plan/: Revboo strategy and execution (start here)

> **Other AIs: start here.** This folder is the one place for *what we run next and how we make it*. Read it in this order, then do the next unchecked box in [TOP10.md](TOP10.md).

| File | What it is |
|---|---|
| [TOP10.md](TOP10.md) | The 10 library ads to run on Meta now, ranked, with the fix each needs and status checkboxes. **The work queue.** |
| [LAUNCH.md](LAUNCH.md) | Meta launch checklist + draft primary text / headline / CTA for every top-10 ad. |
| [TEARDOWN-REVIEW.md](TEARDOWN-REVIEW.md) | Honest review of the before/after "teardown" ads (hook, sound-off, captions, VO, pacing, audio, end card). |
| [PIPELINE.md](PIPELINE.md) | The repeatable edit pipeline: intake → Whisper → house captions → QA → covers → copy variants → library → FINALS. |
| [UPCOMING.md](UPCOMING.md) | What to build next: hooks, concepts, SuperMoney "One Letter" prospect work, best-of original ad, cover A/B tests. |

## Rules that override everything here
- Brand/caption rules: [../BRAND.md](../BRAND.md). Approved files: [../FINALS.md](../FINALS.md). Filing: [../README.md](../README.md), [../AGENTS.md](../AGENTS.md).
- Nothing in plan/ approves an ad. Only Chase approves; approval is recorded in FINALS.md / `catalog/registry.json`.
- No fake stats, no invented results, no "$2,000/month" or "20 ads" until Chase confirms. Only approved offer: **First 2 ads FREE. Delivered in 24 hours.**
- Use the latest version of each ad only. Never delete files or release assets; add new versions under new ids.
- No campaigns have been launched and no ad account is connected. LAUNCH.md is a checklist, not a record of spend.

## How to update
1. Tick a box in TOP10.md when a fix is done (link the new library id / release URL).
2. When Chase approves, move it into FINALS.md via `make_finals.py` and mark it **Run now** here.
3. Add new ideas to UPCOMING.md; promote to TOP10 only when a file exists in the library.
4. Commit as a normal commit, `git pull --rebase` before push, never force-push.

Last full review: Oct 4, 2026 (Grok Bot). Review working files (contact sheets, Whisper transcripts, loudness) on the box: `/workspace/revboo/review-oct4/`.
