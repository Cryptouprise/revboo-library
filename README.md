# Revboo Video Library

Live page: https://cryptouprise.github.io/revboo-library/

> ## ★ Approved – Ready to Run = the source of truth for what runs
> Chase approved 10 ads on Oct 4, 2026 (1:33 PM MT). The **★ Approved section is the source of truth for what runs**: top of the [live page](https://cryptouprise.github.io/revboo-library/#approved), top of [FINALS.md](FINALS.md), checklist in [plan/TOP10.md](plan/TOP10.md).
> Stored in `catalog/registry.json` → `approved_ranking` (ordered list: `rank` 1-10, `star`, `concept_id`, `asset_ids`, `cover_ids`, `fix_in_progress`, `note`). Each ranked concept also has `approved_rank`, `approved_star: "★"`, `approval_status`, `approved_asset_ids` and `approved_asset_id`; each approved file has an `Approved` revision record with `approval` {by, at, sha256}. `catalog/shortlist.json` mirrors the ranks (starred) for Creative Command.
> **Keep it sorted by `rank`.** To replace an approved pick (e.g. a fixed version of 4, 5, 6, 8, 9 or 10): add the new file (`build.py add`), register it under the same concept with an `Approved` revision record (Chase's approval), swap it into that rank's `asset_ids` plus the concept's `approved_asset_id`/`approved_asset_ids` and the shortlist entry, keep the old file, then run `python3 tools/validate_catalog.py` and `python3 make_finals.py`. Never add a rank without Chase's approval.

> **Strategy & execution: start in [plan/](plan/README.md)** (Top 10 to run on Meta, teardown review, edit pipeline, upcoming concepts, Meta launch checklist + copy).
>
> **Other AIs: follow [BRAND.md](BRAND.md) for all Revboo ads** (colors, fonts, the house caption standard, covers, end card, audio, banned styles; caption helper `tools/house_captions.py`).
>
> **Other AIs: only use files listed in [FINALS.md](FINALS.md)** (machine-readable: `finals.json`). Everything else in this library is unreviewed or rejected; ask Chase before using it. Files marked `status: rejected` (red REJECTED chip) must never be used. Approved cover images live in `covers/` (listed in `covers.json`). Regenerate FINALS with `python3 make_finals.py` after Chase approves something.

Chase's finished ads and reusable clips, filed by brand (Revboo, Legal/PI, The Assist, Infinite AI, Solar Freedom, Generic/Other). Everything on the page comes from `manifest.json`. Videos are stored as assets on this repo's GitHub Releases (`media-v1`, …), not in git; posters are in `media/posters/`. See "Where files go" below. Each brand gets a tab (link straight to one with `#brand=The%20Assist`), with its own Finished Ads and Clips. "All" shows everything newest first.

## Filing rules (video library): read this first

Every video Chase makes or sends is filed automatically in the library: `/workspace/revboo/library/` on the box, live at https://cryptouprise.github.io/revboo-library/ (repo `Cryptouprise/revboo-library`). Don't ask Chase where something goes. File it using these rules.

### 1. Brand (top-level `brand` field; use exactly one of these values)
| Brand | What goes here |
|---|---|
| **Revboo** | Promos for Revboo itself (revboo.video), including Chase's Seedance originals for Revboo and Revboo brand cards and clips. |
| **Legal/PI** | Anything aimed at attorneys or PI firms, including Revboo ads that target attorneys (e.g. *PI Attorneys*, *Your Move, Counselor*) and the clips made for them (`revboo/pi/`, `revboo/pi2/`). |
| **The Assist** | Andy / LeadRoller / The Assist newsletter ads (`outreach/andy-board/…`). Other ads made for Andy's board (e.g. the Trovy UGC) also go here. |
| **Infinite AI** | myinfinite.ai AI sales employee videos (control tower, hero VSL, UGC demos; `infinite-media/`, `uploads/ai-department-*`). |
| **Solar Freedom** | breakyoursolarcontract.com ads. |
| **Generic/Other** | Anything else. |

If a video fits two brands, the more specific audience wins: an attorney-targeted Revboo ad is **Legal/PI**, not Revboo.

`build.py` guesses the brand from the path and filename when you don't pass one. These rules are checked in order and the first match wins:
1. Legal/PI: attorney, lawyer, counsel, legal, injury, or a `pi`/`pi2` folder or name part.
2. The Assist: assist, andy, leadroller, newsletter, trovy.
3. Infinite AI: infinite, ai-department, control-tower, imagine-sales, speed-to-lead, lead-response.
4. Solar Freedom: solar, breakyoursolar, scrc.
5. Revboo: revboo, chase-asset, `/refs/`.
6. Otherwise: Generic/Other.

Check a guess with `python3 build.py guess FILE`. Pass `--brand` to override it.

### 2. Finished ad or clip?
- **Finished ad** (`finals` in manifest.json): a complete, publishable spot. Versions of the same ad share one `group`. The newest is shown as LATEST and older ones collapse under it. `category` becomes a sub-heading inside the brand tab (e.g. "Seedance originals (made by Chase)", "Assist remakes (text motion)").
- **Clip** (`clips`): a raw, reusable source shot (Kling/Grok/Seedance generations, Chase's cards). Give it a plain-English name ("Courthouse attorney – golden hour"), one or more categories (Cars/Engine, Phones & Scrolling, People/Reactions, Legal/PI, Products, Brand cards & Logo, Transitions/FX), the ads that use it (`used_in`), and a ⚠ `note` for anything to fix before reuse (garbled text, plates, watermarks).
- **Skip** intermediate renders, previews, audio files, test outputs, broken segments, contact sheets, and exact duplicates (check with `md5sum`).

### 3. Where files go
- Web copies are made in `library/media/finals/<id>.mp4` (**under 6 MB**; existing chat copies are copied as-is, otherwise a two-pass H.264 re-encode sized to fit) or `library/media/clips/<id>.mp4` (720p-ish H.264, faststart, **under ~1.5 MB**). Posters go in `library/media/posters/<id>.jpg`.
- **Video storage = GitHub Release assets, not git.** `build.py` uploads each new web copy to a release on `Cryptouprise/revboo-library` (tag `media-v1`; when a release reaches 900 assets it starts `media-v2`, and so on) and points the manifest's `video` at `https://github.com/Cryptouprise/revboo-library/releases/download/<tag>/<id>.mp4`. The page plays these inline with no login. `media_release.json` (committed) records the tag, size and sha256 of every uploaded file. It needs `gh` logged in as Cryptouprise.
- `media/finals/` and `media/clips/` are **gitignored**. The local copies stay on the box; never `git add` mp4s. Posters (small jpgs) are still committed and served by Pages.
- Asset names are `<id>.mp4`, so ids must be unique across finals and clips (lowercase, digits, dashes). A release asset is never overwritten: to replace a video, add it under a new id or `--version`.
- Never delete or rename release assets or the `media-v*` releases. The live page streams from them.
- Originals stay where they are. `source` in the manifest records the original path.
- Size targets still apply (fast loading), but the repo no longer grows with videos. GitHub's only limit is 2 GB per file.

### 4. Dates
- `date` = the source file's modification time, formatted like "Sep 28, 2026". `datetime` = full ISO time, used for newest-first sorting.
- Use an override only when Chase gives a real creation date or the filename proves one, e.g. Higgsfield `hf_YYYYMMDD_HHMMSS` names are UTC and must be converted to MT (`date_override`, or `--date "Sep 27, 2026"`).
- Note: many files were restored onto the box at 03:03 on Sep 28, 2026, so their mtime is that restore time.

### 5. Adding a video (the whole procedure)
1. `cd /workspace/revboo/library`
2. For a finished ad: `python3 build.py add /path/to/file.mp4 --title "Ad Name" [--version v2] [--group "Ad Name"] [--brand "Legal/PI"] [--category "…"] [--note "…"] [--date "Sep 28, 2026"]`
   For a clip: `python3 build.py add /path/clip.mp4 --type clip --title "Rain street – night" --categories "Legal/PI,Cars/Engine" --used-in "PI Attorneys" [--brand …]`
   This makes the web copy and poster, files the video under its brand (guessed if `--brand` is omitted), saves it in `extra_sources.json`, and rewrites `manifest.json`.
   For permanent or curated entries you can instead add a line to `FINALS`/`CLIPS` in `build.py` and run `python3 build.py`.
3. Glance at the poster. If it lands on a flash frame, re-add with `--poster-time`, delete the old jpg, and rebuild.
4. `git add -A && git commit -m "Add <name>" && git push` (this commits `manifest.json`, `media_release.json`, `extra_sources.json` and the poster; mp4s are gitignored). GitHub Pages updates in about a minute.
   `add` (and a plain `python3 build.py`) uploads any new web copy to the release before writing `manifest.json`. If the upload fails it prints a WARNING and the video will not play on the site; fix `gh` and run `python3 build.py sync`. Use `--no-upload` only for offline tests.
5. Verify: `curl -sIL https://github.com/Cryptouprise/revboo-library/releases/download/media-v1/<id>.mp4` ends in `200` (after a 302 redirect; content-type `application/octet-stream` is expected and plays fine), and the video appears and plays under the right brand tab.

Without the box: upload the mp4 to the latest `media-v*` release on GitHub (Releases → edit → attach), commit a poster jpg to `media/posters/`, and add one entry to `manifest.json` with `brand`, `date`, `datetime`, `duration`, `video` (the release download URL) and `poster`, then commit. Also add the file to `media_release.json` so `build.py` knows it is uploaded.


## Shared agent catalog and revision rules

All agents: read [AGENTS.md](AGENTS.md) and [the shared workflow](docs/AGENT_WORKFLOW.md). These add permanent concept IDs, creator/editor tags, and explicit approval records. Where the older filing rules call an export final, that does not establish launch approval. Use [the agent catalog](agents.html) to filter by creator, editor, collection or ID; the original gallery and release links remain valid. Copy [this handoff prompt](docs/AGENT_HANDOFF_PROMPT.txt) into another AI. Run `python3 tools/validate_catalog.py` before committing catalog changes.


[Creative Command dashboard](command.html) combines the catalog, extensible agent tags, private reporting import, Muse handoff and strategy comparison. No ad accounts connected or campaigns launched. See [Muse analytics contract](docs/MUSE_ANALYTICS.md).


## Free Ads
Creative Command has a **Free Ads** shortcut for complimentary prospect concepts, HVAC demonstration skits. SuperMoney and HVAC Samples retain their own brand filters. This label is a purpose tag, independent of creator, advertiser, format and approval. Older Ken-labelled narration exports retain their original labels; the label alone does not verify voice identity.


### Stars and content
Creative Command now has ★ buttons, a Starred view, favorites-first ordering, notes, ordering controls and Copy/Download/Import shortlist. Your chosen version stays attached to its concept. Browser picks save locally; copy the shortlist into any AI to discuss the same exact exports. Ask an authorized agent to sync the shortlist to catalog/shortlist.json to share it through GitHub. No campaign launch is implied.

RevBoo teardowns are tagged RevBoo Ads plus Content. They are not Free Ads. Content filtering reuses the same concept/version records. See docs/AGENT_WORKFLOW.md for the cross-agent shortlist contract.
