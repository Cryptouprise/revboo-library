# Revboo Video Library

Live page: https://cryptouprise.github.io/revboo-library/

Chase's finished ads and reusable clips, filed by brand (Revboo, Legal/PI, The Assist, Infinite AI, Solar Freedom, Generic/Other). Everything on the page comes from `manifest.json`. Each brand gets a tab (link straight to one with `#brand=The%20Assist`), with its own Finished Ads and Clips. "All" shows everything newest first.

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
- Web copies go in `library/media/finals/<id>.mp4` (**under 6 MB**; existing chat copies are copied as-is, otherwise a two-pass H.264 re-encode sized to fit) or `library/media/clips/<id>.mp4` (720p-ish H.264, faststart, **under ~1.5 MB**). Posters go in `library/media/posters/<id>.jpg`.
- Originals stay where they are. `source` in the manifest records the original path.
- Keep the repo under ~150 MB. Use smaller targets (`max_mb`) for batches of near-identical variants.

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
4. `git add -A && git commit -m "Add <name>" && git push`. GitHub Pages updates in about a minute.
5. Verify: `curl -sI https://cryptouprise.github.io/revboo-library/media/finals/<id>.mp4` returns 200, and the video appears under the right brand tab.

Without the box: drop the mp4 and a poster jpg into `media/`, add one entry to `manifest.json` with `brand`, `date`, `datetime`, `duration`, `video` and `poster`, then commit.
