# BRAND.md: the Revboo brand guide

> **Other AIs: follow BRAND.md for all Revboo ads.** Use only approved files from [FINALS.md](FINALS.md) (filing rules: [README.md](README.md), [AGENTS.md](AGENTS.md)). If this guide and an older note (PLAYBOOK, older ads, `manifest.json`'s `font: Anton`) disagree, **this guide wins**.

Revboo (**revboo.video**) is a done-for-you weekly video ad service. Every Revboo ad looks, reads and sounds like the reference cut below.

**Reference (source of truth):** the Chase-approved **Furnace – Captioned Paid Ad** (RB-005, `furnace-captioned-9x16-v1` in FINALS.md). Build scripts: `/workspace/revboo/edits/fire-money-captioned/work/` (`capslib.py`, `render.py`, `plan.py`, `plan45.py`, `qa_sheet.py`, `thumbs.py`, `hook.py`, `master_audio.sh`). The other sources are the Style C styleframe scripts (`/workspace/revboo/styleframes/work/sf.py`, `styles.py`, `anim.py`) and the best-of covers (`/workspace/revboo/edits/best-of/work/thumbs.py`). Every number below is copied from those scripts.
**Reusable code:** [`tools/house_captions.py`](tools/house_captions.py) (see [Caption helper](#caption-helper-toolshouse_captionspy)).

---

## 1. Words

| Use | Copy (word for word) |
|---|---|
| Tagline 1 (contrarian line) | **"Don't fire your media buyer. Give them better ads."** |
| Tagline 2 (brand line) | **"Revboo. The revenue boost your ads can't afford to miss."** |
| Offer (the only approved offer) | **"First 2 ads FREE. Delivered in 24 hours."** In Style C captions it's set mixed case: `First 2 ads *free*.` / `Delivered in 24 hours.` |
| End-card line (Furnace) | "Done-for-you video ads. Delivered weekly." Sound-off hold line: "Get more out of your ad budget." |
| Site / wordmark | **revboo.video**, spelled "Revboo" with two o's at the end and one "o" in ".video". AI generations have rendered it "REVBOOO" and "Donefor-your", so read every end card letter by letter. |

- **Captions match the actual VO.** Check it with Whisper (small.en + large-v3) before captioning. If the VO says a wrong word, flag it (the Furnace VO said "your **abs**", and that take is rejected). Never caption what the VO *should* have said.
- **No invented facts:** no fake stats, percentages, client counts, results, testimonials or prices. Research numbers can go in primary text only, with a citation, and never on screen.

## 2. Banned

- **All-caps Anton "meme" captions** (Anton, stroked/outlined text, word-by-word pop/karaoke, shouting caps). This replaces the older PLAYBOOK guidance that used Anton.
- **Fake stats or numbers** of any kind (see above).
- **Unconfirmed pricing: "$2,000/month" and "20 ads"** (Muse cover #03). Chase has not confirmed them. Don't use them anywhere until he does.
- Captions over faces, people, on-screen text or the key action. Text in the top 12% or bottom 20% of a 9:16 frame.
- More than one orange word in a caption, or none.
- Watermarks (CapCut AI and others) and garbled AI lettering on screen.
- The fire-logo end clip on client ads (see section 7).

## 3. Colors

| Role | Hex | RGB | Source |
|---|---|---|---|
| **Revboo orange**: the accent word, cover accent, orange rule, ".video" | **#FF4B0A** | 255, 75, 10 | `ORANGE` in capslib.py, sf.py, best-of thumbs.py |
| Caption white | **#FFFFFF** | 255, 255, 255 | capslib.py `WHITE` |
| Headline/wordmark warm white (styleframe + thumbnails) | **#FAF8F5** | 250, 248, 245 | styles.py / best-of thumbs.py `WHITE` |
| Cover subline | **#EBE8E4** | 235, 232, 228 | best-of thumbs.py |
| Shadow | #000000 | soft, see section 5 | capslib.py |
| End-card background (measured) | ≈ **#030205** near-black with orange embers | | Furnace end card at 0:16.5 |
| Logo orange *as encoded in video* (reference only) | ≈ #ED5614 (Furnace end card), ≈ #FC4E00 (fire-logo end clip) | | measured medians. Anything you render uses #FF4B0A. |
| Styleframe shadow fill (bottom gradient) | #050506 (0.02, 0.02, 0.025) | | styles.py `style_C` |

Palette rule: white type, **one** orange accent, everything else is the footage. No other brand colors, no colored caption boxes.

## 4. Fonts

All type is **Inter Tight** (variable): `/usr/share/fonts/truetype/sand-box/google/Inter Tight/InterTight-VariableFont_wght.ttf`, with the weight set via `set_variation_by_axes([wght])`.

| Use | Weight | Size (1080-wide frame) | Tracking / leading |
|---|---|---|---|
| Captions | **ExtraBold 800** | **60-64 px** (Furnace: 62, 62, 60, 64, 60, 64) | -0.02 em, line height 1.12 |
| Hook-cover headline (Furnace hook-cover test) | 800 | 74 px, subline 46 px | -0.02 / -0.015 em |
| Cover headline | 800 | **106 px (9:16), 112 px (4:5)** (best-of thumbs 118-150 px, auto-fit to 936 px wide) | -0.025 em, line height 1.04 (best-of: -4/128 em) |
| Cover subline | SemiBold 600 | 0.36 × headline size | |
| Wordmark "Revboo" + ".video" | 700 + 600 | 38 px (thumbs), 34 px (styleframe) | |
| Styleframe big type (Style C) | 800 | 128 px, 132 px line step | -4 px |

Never use Anton, condensed display fonts, serif fonts or all caps in Revboo ads. Write sentence case: "Don't *fire* your media buyer.", not "DON'T FIRE YOUR MEDIA BUYER".

## 5. HOUSE CAPTION STANDARD (Style C)

1. **Look:** white, **mixed/sentence case**, Inter Tight ExtraBold, 60-64 px, tracking -0.02 em, line height 1.12. Soft shadow only: the text mask blurred 9 px at 62% plus blurred 22 px at 35%, offset 3 px down. No boxes, bars, strokes or emoji.
2. **Exactly one orange (#FF4B0A) accent word per line of copy**, i.e. per caption. A caption that wraps onto two rows still has only one orange word (Furnace: "Don't *fire* your / media buyer."). Pick the word that carries the meaning (*money, feeding, fire, ads, budget, free*). The helper refuses to render a caption with zero or two.
3. **Motion:** fade in over **0.30 s** with ease-out cubic (`1-(1-u)^3`) while **rising 26 px** into place; fade out over the last **0.20 s**. No other animation: no pops, bounces, scale or per-word reveals. (The Style C styleframe test used the same 26 px slide over 0.7 s with staggered line starts at 0.15, 0.35 and 0.60 s, and a slow 3.5% push over 3 s. Use that only for title cards.)
4. **Timing:** about **2.2-3 s per caption**, cut on the VO, with about 0.05-0.2 s between captions (Furnace: 0-2.25, 2.32-4.6, 7.25-9.45, 9.50-11.75, 11.95-14.95, 15.15-17.45 s). If the VO goes faster, sync to the VO and say so.
5. **Safe zones (9:16, 1080x1920):** nothing in the **top 12%** (y < 230) or the **bottom 20%** (y > 1536), counting the 26 px rise. Furnace caption rows: y = 250-300 (top band) and y = 1190 (end-card space). **4:5 (1080x1350):** 5% margins (68 px); re-place each caption per shot (Furnace 4:5 y = 80 / 180 / 1070 with per-shot crops y0 = 420 / 170 / 210 / 120).
6. **Clean zones only.** Captions **never** cover a face, a person or torso (including the BIG SALE cardboard cutout and blurred foreground figures), on-screen text, or the key action (the money, the fire, a product being used). Furnace keep-out boxes: face +20% on each side, +35% above, +10% below; torso ±1.7 face widths from the face center down to the frame bottom; OCR text +14 px; manual boxes for props; fire/explosion pixels may not exceed 2% of the caption box.
7. **If the action fills the frame, no caption.** Skip the line rather than cover the shot. The VO and the next clean shot carry it.
8. **Sound-off readable:** the ad must make sense muted. Every spoken selling line is on screen (or covered by its visual), and the end card holds a sound-off line (Furnace: +2.5 s hold with "Get more out of your ad *budget*.").
9. **QA before delivery:** the overlap check prints `OK` for every caption, the 4 fps QA contact sheet (green caption boxes, red faces/torsos/people, blue text) shows no overlaps, and the OCR read-back matches.

## 6. Picture: grade, vignette, grain

- **Furnace (reference): no added grade.** It keeps the native filmic Seedance look. Don't regrade footage that already looks like film. Captions are composited straight onto the source.
- **Style C styleframe grade** (`sf.py` / `styles.py style_C`, for flat or bright sources and title cards): exposure -0.25 stops, saturation 0.78, filmic S-curve contrast 1.2 with blacks lifted to 0.025 and whites at 0.96, shadows tinted (0.93, 0.98, 1.03) and highlights (1.04, 1.0, 0.95) (cool shadows, warm highlights). Spot lift +18% on the subject. Bottom gradient y 880→1450 to 80% near-black and top gradient 35%→0 over y 0-420 (only where type goes). **Vignette** strength 0.45, power 2.2, center at y = 0.42H. **Grain** 0.03 (noise at 1/1.6 resolution, stronger in the mids), plus 0.008 fine grain on the final composite.
- **Best-of cover grade** (`best-of/work/thumbs.py`): saturation 0.8-1.05, contrast 1.12-1.18, output range 0.02-0.98, shadows tinted (0.93, 0.98, 1.06) and highlights (1.03, 1.0, 0.97). Gaussian legibility band behind the text at 55%. **Vignette** 0.40, power 2.2. **Grain** σ = 5 (8-bit). Text shadow blur 14 px at 70%, 8 px down.
- **Never** put grade, vignette or grain on the logo/end card. Keep it as delivered.

## 7. Logo, end card and the fire-logo end clip

- **End card:** Chase's Revboo logo (orange "R" swoosh mark + white "Revboo" wordmark + ".video") on near-black with embers, exactly as in the source. Don't recolor, stretch, regrade or retype it. One caption may sit in the empty space below it (Furnace: y ≈ 1190).
- **Fire-logo end clip:** `/workspace/revboo/edits/monday-drop/v3work/endclip.mp4` (720x1280, 30 fps, 4.07 s, with its own audio). Use it **only on Revboo-branded ads** (ads selling Revboo itself, including Revboo's attorney-targeted ads). **Never on client ads** (ads made for a client brand: The Assist/Andy, Infinite AI, Solar Freedom, SuperMoney, any prospect sample).
  - It has a **CapCut AI watermark** at the top left. Crop it off: `crop=684:1216:18:58,scale=1080:1920:flags=lanczos` (the best-of crop). Keep the clip's own audio and fade it out over its last 0.3 s.
  - Go into it with a logo-to-logo match dissolve (Monday Drop v3, PI Scroll Past, Best-Of).

## 8. Cover / thumbnail style

- **A real frame from the ad** (not a generated poster), chosen for one emotion or one absurd object.
- **Hook: 3-6 words on 2 short lines, exactly one orange word.** Take it from the ad itself ("Stop feeding the *furnace*.", "Still paying for *this* guy?", "Don't fire your media *buyer*.", "Your audience is *yawning*.").
- **Small subline** under it (0.36 × headline size, weight 600, #EBE8E4), e.g. "Give them better ads." / "New ads. Every week."
- **"Revboo .video" wordmark** bottom left ("Revboo" 38 px weight 700 white + ".video" weight 600 orange; x = 76, y = H-150 at 9:16 or H-74 at 4:5). Optional 130x12 px orange rule above the headline.
- Furnace cover layout: headline right-aligned 48 px from the right edge (9:16: y = 1298 at 106 px; 4:5: crop from y 300, text y = 1010 at 112 px). Legibility gradient darkens from 62% to 86% of the height by up to 55% (mirror it at the top when the text sits up there). Text in a clean zone, never over a face, and inside the center 3:4 area so the profile-grid crop keeps it.
- Deliver **9:16 (1080x1920) and 4:5 (1080x1350)**: `covers/<ad>-cover-9x16.png` / `-4x5.png`, listed in `covers.json`.

## 9. Audio and voice

- **Master to -14 LUFS integrated, about -1 dBTP** (Furnace measures -14.1 LUFS, -1.3 dB peak). Method (`master_audio.sh`): static gain from the measured LUFS, then `alimiter=limit=0.85:attack=1:release=60:level=disabled`, 48 kHz 24-bit, then re-measure (up to 3 passes, within 0.3 LU). Set the gain from LUFS, never from peak.
- **Voice: MAI-Voice-2.1, voice "Grant"**, for any new or replacement Revboo VO. Same-voice word fixes are allowed only when noted (Furnace "ads" was spliced from 0:02, pitch-matched, with 8 ms crossfades), and Chase must hear them.
- Video caption text is always a transcript of the final VO.

## 10. Delivery specs (Furnace)

- 9:16 master 1080x1920, 24 fps, H.264 CRF 15 `-preset slow`, yuv420p, `+faststart`, AAC 48 kHz (~200-256 kbps).
- 4:5 feed cut 1080x1350: a per-shot reframe with captions re-placed (not a center crop of the captioned 9:16).
- Small web copy 720x1280 at 5-6 MB or less; 9:16 + 4:5 covers. Optional hook-cover A/B test: a 1.25 s opening card (3% push-in, text fades out over the last 0.15 s).
- File with `build.py add` (README). Only Chase's approval puts it in FINALS.md.

## Caption helper (`tools/house_captions.py`)

The Furnace build packaged as one importable file. Its `render()` output is byte-identical to the Furnace `capslib.render`, and `cover()` reproduces the approved Furnace covers pixel for pixel. Run `python3 tools/house_captions.py` to print the full docs.

```python
import sys; sys.path.insert(0, '/workspace/revboo/library/tools'); import house_captions as hc
det = hc.detect('src_916.mp4', 'detect.json')          # faces (YuNet) + people (YOLOv8n) + on-screen text (RapidOCR), every 0.25 s
caps = [
  dict(id='C1', t0=0.00, t1=2.25, text='Before you throw more *money* at your ads,', size=62, maxw=900, align='center', x=None, y=250),
  dict(id='C4', t0=7.25, t1=9.45, text="Don’t *fire* your|media buyer.", size=60, maxw=420, align='left', x=44, y=300, lines=True),
]
assert not hc.check_all(caps, det, src='src_916.mp4', manual=None)   # every caption must print OK (manual=fn(t)->[(label,x0,y0,x1,y1)] for props)
hc.run('src_916.mp4', 'cap916_silent.mp4', 1080, 1920, caps)        # 4:5: W,H=1080,1350 + crop_fn=lambda t: y0, captions with 4:5 y
hc.master_audio('mix_raw.wav', 'mix_master.wav', dur)              # -14 LUFS / ~-1 dBTP
# ffmpeg -i cap916_silent.mp4 -i mix_master.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest final.mp4
print(hc.qa_sheet('final.mp4', 'contact.png', 'qa.png', 1080, 1920, caps, det))   # [] = no overlaps
hc.ocr_verify('final.mp4', caps, 1080)
hc.cover('frame.png', 'Stop feeding|the *furnace*.', 'cover-9x16.png', 0, 1920, 1298, size=106,
         sub='Give them better ads.', wordmark=True)                # sub/wordmark/rule optional (best-of style)
```
CLI: `python3 tools/house_captions.py detect SRC.mp4 OUT.json` · `python3 tools/house_captions.py preview "Give them|better *ads*." out.png 64`.
Needs: Pillow, numpy, OpenCV, rapidocr_onnxruntime, onnxruntime, ffmpeg, and the models in `/workspace/revboo/tools/models/` (YuNet, YOLOv8n). Mark the accent word with `*asterisks*`; `|` plus `lines=True` sets manual line breaks; use typographic apostrophes (’).

## Checklist before anything ships
- [ ] Only approved inputs (FINALS.md). VO transcribed and correct. Captions = VO.
- [ ] Inter Tight 800, mixed case, white + exactly one orange word per caption; 0.30 s fade-in with 26 px rise; 2.2-3 s each.
- [ ] Nothing in the top 12% / bottom 20%; no caption on a face, person, on-screen text or the key action; none on full-frame action. Overlap check, QA sheet and OCR read-back are clean.
- [ ] Taglines and the offer word for word; no stats, prices or "$2,000 / 20 ads"; "revboo.video" spelled right.
- [ ] -14 LUFS / about -1 dBTP. End clip only on Revboo-branded ads, watermark cropped.
- [ ] 9:16 + 4:5 + small copy + 9:16/4:5 covers (3-6 word hook, one orange word, subline, Revboo .video).
