# Flagship finals v3: Monday Night + The Set (DRAFTS pending Chase's approval)

Status: **Draft.** Do not run. These go under Revboo > Finals only after Chase approves; until then they're listed under Drafts & Mockups (Flagship v3).
Rendered Oct 17, 2026, 10:30 AM MT (Monday Night) and 10:46 AM MT (The Set). Scripts: `plan/FLAGSHIP-SCRIPTS-V2.md`. Planet Ad was dropped and archived.

| | Monday Night | The Set |
|---|---|---|
| Asset id | `rb-018-a-v03-9x16` | `rb-019-a-v03-9x16` |
| Master (box) | `edits/flagship-finals/monday-night-final.mp4` | `edits/flagship-finals/the-set-final.mp4` |
| Length | 56.1 s | 59.8 s |
| Also on box | `-720p`, `-4x5` (1080x1350), `-4x5-720p` | same |
| Loudness | -14.2 LUFS, peak -1.2 dBFS | -14.1 LUFS, peak -1.3 dBFS |

## What changed from draft v2
- **Real ads on phones.** Reels-style mock ad screens built in post (a tired "BIG SALE" ad, slick fresh competitor ads, Revboo-made fresh ads) with readable text, composited onto every phone/screen with Lucas-Kanade tracking + corner-pin (skin-protected where fingers cross the screen). New UI inserts: VS, scroll, chaos-of-tools, and a 2x2 "winner" grid.
- **Regenerated weak shots only** (Higgsfield Kling v3.0): both crew shots (faces off-frame / from behind), plus avatar base clips.
- **Avatar cut-ins** (Higgsfield Sync Lipsync 3): sideline reporter for Monday Night's "making video is slow" line; a "Revboo producer" intro for The Set.
- **Captions:** Monday Night's busy trophy and confetti captions moved and frosted; every very bright caption zone gets a frosted backing; The Set's closing caption moved off the owner's face. House Style C, one caption at a time, one accent word.
- **Upscale:** every generated shot ByteDance-upscaled; masters 1080x1920.
- **4:5 cut:** per-segment crop that keeps each caption inside the frame; UI-insert segments are scaled to fit on a blurred fill.

## QA (Oct 17)
- Frame sheets at 1 s plus a frame check of every caption window; no garbled text (the TV-scene EXIT sign is blurred).
- Whisper (small.en) transcript matches the script; no VO overlaps; one bed under the VO, -14 LUFS.

## Spend
Finals work: **100.17 Higgsfield credits (~$4.41)**: 4 Kling v3.0 clips 31.5, 2 lipsyncs 39.9, 19 upscales 19.52, 12 images 9.25. No OpenRouter spend. Draft v2 voices were reused.

## Remaining flaws
- Composited screens can float slightly at the edges on fast hand moves.
- In 4:5, the UI-insert segments are pillarboxed (scaled to fit on a blurred fill).

## v4 QA-fix pass (Oct 17, 11:45 AM MT). Still DRAFTS pending Chase's approval
Asset ids `rb-018-a-v04-9x16` (Monday Night, 56.1 s) and `rb-019-a-v04-9x16` (The Set, 59.8 s). The masters overwrite `edits/flagship-finals/*-final*.mp4`. The v3 cut is kept as `*-final-v1*.mp4`. Working notes: `edits/flagship-finals/work/FIX-PROGRESS.md`.

**The Set:** the crew intro was re-rendered from behind, so no crew faces the camera. The clean mock-ad UI was redrawn (@brightkilnco, @morningleaf.co, 'Sponsored', clean icons, safe margins so "this changed my mornings" and "kiln" are no longer clipped) and applied to the two-phones shot and the winner grid. The media buyer was re-rendered as a static shot (empty folder, hands below the desk), and so was the shredder (locked camera, no hands). The owner's coffee shot was trimmed to the clean sip.
**Monday Night:** the opening line-up was cropped to remove the left player. The tired player was zoomed so his hands are out of frame. The owner was re-rendered with arms crossed and the cash untouched, and the jersey logo was inpainted out. The reporter was re-rendered with a lapel mic and lip-synced again. The crew runners are now a wide shot from behind with empty hands. The bucket was replaced by a confetti-card shower. The trophy shot was tightened, with its background blurred. New captions: "Making video is *slow*." and "Nobody's got *time*."
**Spend:** 82.3 Higgsfield credits: 8 Kling v3.0 pro clips (70.0, including one rejected shredder retry) and 1 Sync Lipsync (12.3). No OpenRouter spend.
**Remaining flaws:** a faint smoothed patch where the crest was removed; the confetti subject is small; in The Set intro a crew member is seen in rear 3/4 profile for about 1 s; Apple-style logos on the laptops in the crew/owner shot (carried over from v3); the shredder shot is a minimal static hold.
