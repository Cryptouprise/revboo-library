# Revboo prompt playbook: first drafts that are near-final

Researched **Sat Oct 17, 2026** (America/Denver). Research only: **$0 spent on video or images.**
Companion files: [`SHOT-CHECKLIST.md`](SHOT-CHECKLIST.md) (the gate every shot must pass) and `/workspace/revboo/tools/prompt_swarm.py` (writes N prompts and scores them against the checklist).

**Why this exists.** Chase rejected drafts for four recurring failures: **mangled hands**, **garbled AI text**, **phone screens that look pasted on**, and **the wrong subject** (a made-up car instead of the real Tesla Roadster he asked for). Each one is a *process* failure, not a model failure. Every model below fails the same way when it has to guess. The fix is the same every time: **take the guessing away** with a locked start frame, one action per shot, specified camera, framing that keeps hands big or still, and every word or screen added in post.

---

## 0. The 10 rules (read these if nothing else)

1. **Subject = exactly what Chase named.** If he says "the real Tesla Roadster," the start frame is built from **real reference photos of that car**, never from a text description. If a brand/legal rule in another plan doc conflicts (e.g. `FLYING-CAR-CONCEPTS.md` says "No Tesla anything"), **stop and ask Chase**. Never quietly swap in an invented lookalike.
2. **Never text-to-video a hero shot.** Make a **locked start frame** first (Nano Banana Pro / Seedream / Flux Kontext, from real refs), get it approved, then image-to-video. The image fixes identity, layout and light; the prompt only describes motion. (Kling, Veo, Grok, Seedance and Higgsfield all say the same.)
3. **In image-to-video, don't re-describe the image.** Describe **what changes**: one subject + **one action with a start and end state** + **one camera move**. Re-describing it, or contradicting it, makes the model redraw the frame, and redrawing is where morphing starts.
4. **Hands: big and busy, or small and still.** Give the hand a job ("grips the wheel," "rests flat on the counter"). Keep hand motion under ~2 s. Use medium shots or wider, with at most 1-2 people. Crop hands out when the shot doesn't need them. Never write "perfect hands"; quality words don't constrain anything.
5. **AI never renders words.** No readable text, logos, plates, UI or captions from the video model. Prompt blank surfaces and add all type in post with real fonts (Anton etc.). Readable text in the *start frame* (from a real asset) is allowed only on a small, slow-moving surface, and must pass QA.
6. **Screens: plan the insert before you render.** Either (a) build the real ad into the start frame and keep the phone nearly still, or (b) render a **dark/neutral, glossy screen with real reflections** and composite the UI with a 4-corner planar track, preserving the plate's glare and reflections on top, then matching blur, grain and black level. Bright white "keying" screens are what made the inserts look pasted on.
7. **Specify the camera every time.** Shot size, lens feel, one move, speed and an end framing ("slow push-in from medium to close-up, no zoom, no cuts"). If you don't, the model picks, and it changes the subject's scale and detail mid-shot.
8. **One shot = one action = one point.** Write down why the shot exists (the beat in the script). Anything that doesn't serve that point gets cut from the prompt. Long prompts split the model's attention, and hands and faces are the first things to degrade.
9. **Negative prompts only where they're a real parameter** (Kling `negative_prompt`, Veo `negativePrompt`). Keep them short. Everywhere else (Seedance, Grok, Hailuo, image models) write the **positive** state ("empty, blank, matte white panel," not "no text").
10. **QA every 0.5 s before Chase sees anything.** Contact sheet at 2 fps. Check hands, faces, morphing, text, logos, subject identity, caption zones and audio. A draft that fails one item is fixed or re-rolled, never shipped with "it's a draft."

---

## 1. Model-by-model prompt structure

Prices are OpenRouter per-second rates as listed **today** (`GET /api/v1/videos/models`, via `tools/orvideo.py --models`). They are normalised to a **5 s clip** so the models compare directly. Veo only renders 4, 6 or 8 s.

### 1.1 Kling 3.0 (Pro / Std / Turbo / Omni)
- **Official structure:** *Subject + Movement, Background + Movement* for i2v. Image-to-video doesn't need a scene description, only who moves and how ([Kling i2v guide](https://kling.ai/quickstart/image-to-video-guide)). For t2v, a "script + shot list" hybrid works: **genre, scene, subject, action (in sequence), camera, audio** ([Kling 3.0 Omni tutorial](https://www.youtube.com/watch?v=WmC1nqz10Qk)).
- **What 3.0 adds** ([Kling VIDEO 3.0 guide](https://kling.ai/quickstart/klingai-video-3-model-user-guide)): 3-15 s, start + end frame, **Element binding** (bind 2-4 reference images of a character or object to the start frame for consistency), multi-shot / custom multi-shot, and native audio. It also has "native-level text" that *preserves* text from the source image. Use that only for real assets you put in the frame, and QA it.
- **Multi-shot API syntax:** `shot 1, 2, <prompt>; shot 2, 3, <prompt>;` (up to 6 shots, each ≥1 s, durations sum to the total, ≤512 chars per shot) ([API doc](https://kling.ai/document-api/api/video/3-0-omni/image-to-video.md)). Revboo cuts its own edits, so **prefer single shots**; use multi-shot only for match-cut coverage of the same action.
- **Camera phrasing that works** ([Kling 3.0 camera masterclass](https://www.youtube.com/watch?v=TKkg-8P7jTM)): name the move, then **lock the other axes**: "camera rises vertically, boom up… *no pan, no tilt, no zoom*"; "very fast optical zoom with an abrupt stop on the face, *camera position fixed, no dolly*"; "full 360° stabilized orbit at constant radius and speed, *no zoom*". For a reveal of something specific, supply an **end frame** instead of describing it.
- Avoid "cinematic, 4K, masterpiece" stacks (no effect). Generate a fast move slower and speed it up in the edit.
- **Revboo notes (from our tests):** best for **car/product hero motion**. It keeps product design exactly from the start frame, and timed physical gags land at 2-4 s. It looks **plastic on people**. It invents plates and badges, so blank them in the start frame and verify. First/last frames from an image editor can colour-shift: match the end frame to the start.
- **Negative prompt:** supported (`negative_prompt`). Keep it short: `distorted hands, extra fingers, morphing, text, letters, watermark, logo`.
- **Turbo:** Higgsfield's fast 1080p draft tier (3-15 s, start image). Use it for blocking and timing tests, then do finals on Pro ([Higgsfield Kling help](https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-use-kling)). It isn't on OpenRouter; it costs Higgsfield credits.
- **Cost / 5 s:** Pro **$0.56** ($0.84 with audio). Std **$0.42** ($0.63). Kling.ai direct: 6 credits/s at 720p without audio.

### 1.2 Veo 3.1 (full / Fast / Lite)
- **Official formula:** `[Cinematography] + [Subject] + [Action] + [Context] + [Style & Ambiance]` ([Google Cloud Veo 3.1 guide](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1)).
- **Three reference modes:** (1) image-to-video from a start frame; (2) **first + last frame**, where you describe the transition and the audio; (3) **ingredients**: up to 3 reference images of a subject, object or style. Ingredients guide appearance, **not** the first frame, and lock duration to 8 s on preview ([Gemini API Veo](https://ai.google.dev/gemini-api/docs/veo), [Vertex references](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/generate-videos-from-references)). If you send both frames and references, the frames win ([Vercel AI Gateway](https://vercel.com/docs/ai-gateway/modalities/video-generation/reference-to-video)).
- **Timestamp prompting** for timed beats: `[00:00-00:02] … [00:02-00:04] …`.
- **Audio:** dialogue in quotes; `SFX:` and `Ambient noise:` lines. Best lip-sync and dialogue of the set.
- **Negatives:** Veo has a `negativePrompt` param, but Google recommends describing what you *want* ("a desolate landscape with no buildings" beats "no man-made structures").
- **Revboo notes:** best realism and sharpness in our test (people and skin). Lite was the worst we tested; use it only for blocking.
- **Cost / 5 s equivalent:** Veo 3.1 1080p **$1.00** without audio / $2.00 with audio. Fast 720p **$0.40** / $0.50. Lite 720p $0.15 / $0.25. Durations are 4, 6 or 8 s only.

### 1.3 Seedance 2.0 (and 2.5 / Fast / Mini)
- **Modes:** References, Start/End frame, Text-to-video ([Runway: Creating with Seedance 2.0](https://help.runwayml.com/hc/en-us/articles/50488490233363-Creating-with-Seedance-2-0)). Runway also notes **t2v avoids some moderation on realistic humans**.
- **Give every reference one job:** `@Image1 is the product reference; preserve shape, label, logo and color exactly. @Image2 is only the background mood. @Video1 for camera movement only.` An **unlabeled reference leaks** colour, background and styling. **4-5 assets beats 9.** Put the asset that needs the most precise match earliest in the prompt ([Runway Seedance 2.0 prompt guide](https://runway.com/resources/seedance-2-0-prompt-guide), [Seedance complete guide](https://docs.seedance.tv/en/seedance-2-complete-prompting-guide), [awesome-seedance guide](https://github.com/EvoLinkAI/awesome-seedance-2-guide/blob/main/README.md)).
- **One primary camera move per shot.** For longer clips, use time blocks (`0-5s: …; 5-10s: …`).
- **Product pattern** ([prompt examples](https://github.com/Emily2040/seedance-2.0/blob/main/references/prompt-examples.md)): `[product] [does one thing]. Camera: slow dolly-in from medium hero to macro detail. Lighting: narrow strip light glides across… Sound: … Constraints: no text overlays, no logo changes.`
- **Hands:** Higgsfield calls Seedance 2.0 the most reliable for hands and faces **when you add a reference image of the exact hand position** ([Higgsfield hands guide](https://higgsfield.ai/blog/ai-video-hands-faces)). There's no negative-prompt field, so write positive anatomy ("relaxed hand, five fingers resting on the rail").
- **Audio refs:** trim reference audio to whole seconds with no tail (@Kiber_Alla, [X](https://x.com/Kiber_Alla/status/2078814921756754352)).
- **Creator consensus (X):** "Kling 3.0 for static shots, Seedance 2.0 for action and multiple angles" (@hanifproduktif, [X](https://x.com/hanifproduktif/status/2041495051956896191)). "Seedance hits harder and keeps the face; Kling moves the body more naturally. Show the force, don't name it" (@alessia_orbit, [X](https://x.com/alessia_orbit/status/2108917079411683406)). 2.5 brings smoother lip-sync, more natural hands and better product consistency than 2.0 (@jessica_coderx, [X](https://x.com/jessica_coderx/status/2083246424452710747)).
- **Cost / 5 s (720p):** 2.0 **~$0.76**, Fast ~$0.45, Mini ~$0.38 (480p ~$0.17), 2.5 ~$1.16 (480p ~$0.52). Seedance bills per token: W×H×24×s/1024.

### 1.4 Grok Imagine (Video 1.5 / 1.5-lite)
- **Official i2v rules** ([Replicate readme, xAI](https://replicate.com/xai/grok-imagine-video-1.5/readme), [xAI docs](https://docs.x.ai/developers/model-capabilities/video/image-to-video)):
  - Don't re-describe the image, and don't contradict it.
  - Be specific about motion ("racing past at high speed," not "passing").
  - Anchor the subject with one feature ("the man in the red jacket").
  - Use **one subject + one action + one camera move**, and always give a shot type and a camera move.
  - **Negative prompts don't work**; describe what you want instead.
  - **5-8 s is the stable sweet spot**; 15 s artifacts more.
- **Layered prompt** ([community guide](https://github.com/seaimagineai/awesome-grok-imagine-prompts/blob/main/docs/guides/en-US.md), [Vogue AI](https://vogueai.net/blog/grok-imagine-1-5-image-to-video-prompt-guide)): `[Mode/length/aspect] [Source lock: preserve subject, crop, materials, light] [Action beats 1-3] [Camera: one move, no cuts] [Physics/secondary motion] [Audio]`. Name what must stay fixed: face, label, UI screen, hands, empty text area.
- **Reference-to-video:** image + `last_frame` / `keyframes` / `reference_images` (refs cited as `<IMAGE_0>`…).
- **Cost / 5 s:** 1.5 at 720p **$0.70** (1080p $1.25) + $0.01 per input image. 1.5-lite at 720p **$0.15** (cheap blocking pass). The original grok-imagine-video at 720p is $0.35.

### 1.5 Hailuo (MiniMax 2.3 / 3 / 3 Max)
- **Bracket camera commands** give the most accurate camera control ([MiniMax API t2v](https://platform.minimax.io/docs/api-reference/video-generation-t2v), [i2v](https://platform.minimax.io/docs/api-reference/video-generation-i2v)):
  - `[Truck left/right] [Pan left/right] [Push in] [Pull out] [Pedestal up/down] [Tilt up/down] [Zoom in/out] [Shake] [Tracking shot] [Static shot]`
  - Up to 3 commands inside one bracket run at once (`[Pan left,Pedestal up]`).
  - Commands in sequence run in order ("…[Push in], then …[Static shot]").
- First + last frame is on Hailuo-02 ([fl2v](https://platform.minimax.io/docs/api-reference/video-generation-fl2v)). Turn off `prompt_optimizer` when you need your exact prompt used.
- **Revboo notes:** H3 was a close second to Veo in our test (2K, audio, strong text and brand rendering). Text rendering is still **not** a licence to let it write our copy.
- **Cost / 5 s:** Hailuo 3 **$0.65** (2K, audio; extra reference images $0.04 each after 5). 3 Max at 768p $0.40 (no audio). 2.3 is $0.41 (16:9 only).

### 1.6 Start-frame image models (Higgsfield / OpenRouter): Nano Banana, Seedream, Flux Kontext
- **Nano Banana Pro / 2** ([Google Cloud Nano Banana guide](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana)):
  - With references, the formula is `[Reference images] + [Relationship instruction] + [New scenario]`. It takes up to 14 refs.
  - Start with a strong verb, use positive framing ("empty street," not "no cars"), and give camera, lens and lighting in photo terms.
  - For edits, **say exactly what stays the same**.
  - It can render text well (quoted strings, a named font), but for Revboo, still add final copy in post. In-frame text only on real assets you supply.
- **Seedream 5.0 Pro** ([fal guide](https://fal.ai/learn/tools/how-to-use-seedream-5-0-pro-v2), [PiAPI](https://piapi.ai/blogs/seedream-5-pro-api-guide)): up to 10 refs, one role each. Example: "Use Image 1 as the exact product reference. Preserve shape, label, logo, proportions. Use Image 2 only for material… do not add text, people, or extra products." Bounded edits: "Change only X. Preserve everything else."
- **Flux Kontext** ([BFL single-reference editing](https://docs.bfl.ml/guides/prompting_editing_single_reference)): **one narrow edit per pass**. Name the target, state the change, and list what to preserve ("…keeping the car's exact body lines, wheels, paint and camera angle unchanged"). Use the subject's name, not "it/she," and iterate in small steps.
- **Start-frame recipe** (consensus across Google, Kling, techhalla, Charlie Curran workflows):
  1. Character/object **reference sheet** on white: multiple angles, **no hands** on props (@pt5films, [X](https://x.com/pt5films/status/2066967482573984247)).
  2. Location plate.
  3. Compose the **start frame** from those refs at the final aspect ratio.
  4. Optionally make an **end frame** by editing the start frame (then colour-match it).
  5. i2v.
  - Make **varied camera angles as stills** first, then animate each one ([camera masterclass](https://www.youtube.com/watch?v=TKkg-8P7jTM)).
- **Approximate cost per still (OpenRouter):**

  | Model | Cost per still |
  |---|---|
  | Nano Banana Pro (`google/gemini-3-pro-image`) | ~$0.13 at 1-2K (~$0.24 at 4K) |
  | Nano Banana 2 (`google/gemini-3.1-flash-image`) | ~$0.07 |
  | Gemini 2.5 Flash Image | ~$0.04 |
  | Seedream 5.0 Pro / 4.5 | ~$0.03-0.04 |
  | FLUX.2 Pro | ~$0.03 |

  On Higgsfield they cost credits (check `balance`; never buy).

---

## 2. Image-to-video from locked reference frames
1. **Lock the subject first.** Collect 3-6 **real** photos of the named subject (official press images, Chase's own photos, product shots). These are references for the start frame, and they're the comparison set at QA.
2. **Build the start frame** with Nano Banana Pro / Seedream:
   - Use the refs + the relationship instruction + the scene, at the final aspect ratio and lens.
   - Blank all plates, badges and signage unless they're real and approved.
   - Hands are either placed on an object or out of frame.
   - Screens are dark glass (or carry the real ad, see §6).
3. **Approve the frame** before spending video money. This is the cheapest place to fix a wrong subject: a $0.04-0.13 still beats a $0.56-2.00 clip.
4. **Animate:** the prompt is *motion only*. Template:
   `[Source lock: keep the <named subject> exactly as in the start frame: <2-3 identity features>]. [One action, start state → end state, timed: "at ~2 s"]. [Camera: one move + speed + end framing; lock other axes]. [Light/atmosphere change, if any]. [Audio, if any]. [Positive blank-surface clause: "all panels, plates and screens stay blank and featureless"].`
5. Use **an end frame** whenever the shot has to finish on something specific (a reveal, a logo position, a parked car). Colour-match it to the start frame.
6. **Continuity between shots:** take the next start frame from the **last frame of the approved previous clip** (we did this in Tube Man and it held). Or bind the subject as a Kling Element / Seedance `@Image1` with a written role.

## 3. Character and object consistency
- **Identity comes from images, not adjectives.** A text description of "a woman with dark hair" can produce hundreds of valid faces ([Higgsfield](https://higgsfield.ai/blog/ai-video-hands-faces)). Use start frames + Kling Elements (2-4 refs) / Seedance `@ImageN` (one role each) / Veo ingredients (≤3) / Higgsfield Soul ID (20+ photos, Chase's clone).
- **Name 2-3 stable static features** every time you mention the subject ("the white wedge-shaped two-door, black roof, aero wheels"). Use the same words in every shot.
- **Products and cars:** "preserve shape, proportions, color, wheels, light signature, and badge placement exactly." Keep the rotation or reveal slow (camera orbit ≤ 90° per 5 s). A fast spin is where proportions morph.
- **Change one variable per iteration** (camera *or* light *or* action) so you know what broke it.

## 4. Hands (the #1 complaint)
Sources: [Higgsfield hands guide](https://higgsfield.ai/blog/ai-video-hands-faces), [vflow hand-deformation notes](https://vflow.live/fix/hand-deformation/), [AI Tools Guidebook](https://aitoolsguidebook.com/en/articles/ai-video-hands-disappear-during-motion/), r/KlingAI_Videos.
- **Why they break:** a lot of joint detail in few pixels that changes every frame. Under-specified gestures. Overloaded prompts.
- **Framing:**
  - **Medium shot or wider** for any hand *motion*.
  - Close-ups of hands only when the hand is **still** or holding something rigid, and the hand fills a large part of the frame.
  - **Avoid the in-between** (hands small and moving at waist height in a medium-wide).
- **Crop strategy:** if the beat doesn't need hands, frame chest-up with hands below the frame line, in pockets, behind the wheel rim, or occluded by a counter. You can also render 16:9 and **crop to 9:16 away from the hands** in post.
- **Give every hand a job:** grips, holds, rests flat, taps once. Describe the **start and end positions**, not the gesture path ("right hand starts resting on the wheel, ends lifting the phone to chest height").
- **Short:** keep continuous hand action to ≤2 s; cut on it.
- **Few people:** 1 person is ideal, 2 at most interacting. Never two people's hands touching in a small frame (handshakes go wide, or reuse a library clip like `hf-contract-keys-handshake-kitchen`).
- **Static poses beat gestures:** arms folded, hands on hips, hands on the wheel at 10 and 2.
- **Start frame:** the hands in the start frame must already be anatomically perfect. The model rarely *repairs* hands; it breaks clean ones less often.
- **Reference:** on Seedance, add a reference image of the exact hand pose.
- **Never** write "perfect/detailed/beautiful hands." Negative field (Kling/Veo only): `extra fingers, fused fingers, distorted hands`.
- **Phones in hands:** the hand holds the phone *by the edges*, thumb only. One tap or one flick, timed. Not typing.

## 5. Crowds
- Crowds multiply every failure (hands, faces, merging bodies). Prefer:
  - **Silhouettes, backlight, shallow depth of field.** Background people soft and out of focus; only the hero is sharp.
  - **Distance:** a wide shot where people are small and mostly static. Or a tight over-the-shoulder with the crowd as bokeh.
  - **Uniform simple action** for everyone ("all heads tilt up at once"). No individual gestures.
  - **Phones raised in a crowd:** backlit screens as light points, no readable screens, seen from behind.
  - Compositing for real: add crowds in layers or reuse library crowd plates; hybrid live-action + gen-AI crowd adds are a proven pro workflow (@martinleblanc, [X](https://x.com/martinleblanc/status/2070430506865271122)).
- Put the hero's face and hands in front, sharp; the crowd never interacts physically with the hero.

## 6. Text and native-looking screens
### 6.1 Text: never let AI render it
- All copy, captions, UI labels, prices, plates and logos are **added in post** with real fonts (Revboo: Anton for kinetic type; brand reads exactly "Revboo" / "revboo.video").
- Video prompts describe **blank** surfaces positively: "blank matte white sign," "plain unmarked license plate area painted body color," "screen shows soft abstract color with no interface."
- Text on objects in the scene (a sign, a tombstone, a T-shirt) is tracked and composited (LK optical flow + partial affine; see main `PLAYBOOK.md` §5). Fake plates or badges the model invents: FLUX Video Edit removal ($0.03/s) or track + blur.
- Exception: real brand assets *in the start frame* that Kling 3.0 / Hailuo preserve. Allowed only on a slow-moving, large surface, and **must pass QA frame-by-frame**. If any frame warps, fall back to a composite.

### 6.2 Phone and screen inserts that look native (fix for "pasted on")
What makes an insert look fake (r/vfx rules of thumb, [Lowepost Mocha course](https://lowepost.com/courses/after-effects/visual-effects/screen-replacement-in-after-effects-mocha-r42/), [r/AfterEffects screen tracking](https://www.reddit.com/r/AfterEffects/comments/1qbpq74/made_a_tutorial_for_screen_tracking_after_using/)):
- The UI is brighter and sharper than the scene, with no reflections, no grain and a different black level.
- It slides against the phone (track drift).
- There's no motion blur, and fingers sit *under* it.

**Method A: bake the ad into the start frame (preferred for short, near-static shots).**
1. Take the real ad/UI screenshot.
2. Nano Banana Pro / Seedream edit: "Display the attached screen artwork edge-to-edge on the phone screen, unaltered, with natural glass reflection and slight screen glow; keep the hand, phone and scene unchanged."
3. Check the frame at 100%.
4. Animate with **minimal phone motion** (a slight handheld drift, or a slow push-in) for ≤5 s. Kling 3.0 / Hailuo preserve in-frame text best.
5. QA every frame for UI morphing. Fall back to Method B on any warp.

**Method B: composite on a real plate (any motion, any length).**
1. Prompt the screen **off or dark**: "phone screen is off: glossy black glass reflecting the room lights." Or use a uniform mid-grey/green glow if you need a key. Avoid pure white: it clips, destroys reflections and spills onto the thumb. Our old white-screen method tracked well but looked pasted.
2. **4-corner planar track:** Mocha-style, or our `remake/quad2.fit_quads` edge-line fit (robust when a thumb covers an edge). Don't use bezel LK homography (it drifted 35-70 px).
3. Warp the UI with a rounded-rect mask. Then match the scene:
   - **Exposure / white balance:** sample the scene, and keep the UI peak about 10-20% below the brightest scene highlight.
   - **Black level:** lift the UI blacks to the plate's screen black.
   - **Grain and noise:** match.
   - **Softness:** match the plate's focus at the screen depth.
   - **Motion blur:** from the tracked corner velocity.
   - **Light spill:** a faint glow on the thumb and face.
4. **Put the reflections back on top:** extract the plate's screen luma (glare, room reflections, fingerprints) and add it over the UI in screen/add mode at 15-40%. Animated glare that moves with the phone is the single biggest "native" cue.
5. **Occluders above:** thumb and finger mask (skin-aware) so the finger sits on top of the UI. Add a tiny contact shadow on tap.
6. **Perspective check:** the UI's vanishing lines must match the phone body. For rotating phones, use a 3D layer with a camera solve, not a corner pin ([r/AfterEffects](https://www.reddit.com/r/AfterEffects/comments/1pca587/how_to_replace_a_screen_on_a_rotating_phone_in/)).
- **Big screens (car side panel, billboard, stage screen):** same method. Prompt "dark glossy display panel," track 4 corners, add reflections back.

## 7. Camera language (cheat sheet)
| Intent | Prompt phrase (lock other axes) |
|---|---|
| Intimacy / reveal detail | "slow push-in from medium to close-up, no zoom, no pan" |
| Show scale | "crane up / boom up revealing X, no pan, no tilt" (give an end frame for complex reveals) |
| Energy | "handheld, slight shake, following at walking pace" (Hailuo: `[Shake]`, `[Tracking shot]`) |
| Control / product | "locked-off static shot" (Hailuo `[Static shot]`) or "slow lateral slider left to right" |
| Hero car | "low-angle tracking shot alongside at road speed, stabilized, no zoom" |
| Punch | "fast optical crash zoom to extreme close-up, abrupt stop, camera position fixed" (render 3 s, speed up in the edit) |
| Transition | "extremely fast whip pan with heavy motion blur, sharp settle" (cut point) |
| Orbit | "90° stabilized orbit at constant radius, no zoom" (≤90° per 5 s for products, to avoid morphing) |
Always add shot size (wide / medium / close-up / ECU), angle (eye-level / low / high), and for 9:16 "vertical frame, subject upright, horizon level" (an early t2v test laid the car sideways).

## 8. Negative prompts
| Model | Negative support | What to do |
|---|---|---|
| Kling 3.0 | `negative_prompt` param | Short list: `extra fingers, fused fingers, distorted hands, morphing, warped face, text, letters, subtitles, watermark, logo, license plate characters` |
| Veo 3.1 | `negativePrompt` param | Same short list; also describe the positive state in the prompt |
| Seedance | none | Positive constraints ("panels stay blank," "five relaxed fingers") |
| Grok Imagine | ignored | Positive only |
| Hailuo | none | Positive only; disable `prompt_optimizer` if it adds detail |
| Image models | none / weak | Positive framing ("empty street," "blank sign") |
Never stack 30 negatives: a long list adds the very words you're negating to the prompt context.

## 9. Which model for which shot (Revboo routing)
| Shot type | First choice | Why | Draft tier |
|---|---|---|---|
| Real car / product hero motion (i2v) | **Kling 3.0 Pro** ($0.56/5 s) | Keeps product geometry from the start frame; timed actions land | Kling Std ($0.42) / Turbo (Higgsfield) |
| Realistic people, faces, skin, dialogue | **Veo 3.1** ($1.00/5 s, 1080p, no audio) | Best realism, lip-sync | Veo Fast 720p ($0.40) |
| Action, multi-angle, multi-reference consistency, hands with a pose ref | **Seedance 2.0** (~$0.76) / 2.5 (~$1.16) | Ref roles, strong identity, hands with a ref | Seedance Mini 480p (~$0.17) |
| Exact camera-command control, 2K, in-frame brand assets | **Hailuo 3** ($0.65) | Bracket commands, text preservation | Hailuo 3 Max 480p ($0.25) |
| Fast cheap blocking / timing tests | **Grok Imagine 1.5-lite** ($0.15) | Cheapest, any duration from 1 s | — |
| Atmos / ambient B-roll with SFX | Grok Imagine 1.5 ($0.70) | Native ambience and sound effects | 1.5-lite |
| Start frames | **Nano Banana Pro** (~$0.13) | Best reference fidelity and edit control | Seedream 5.0 (~$0.03) |
| Bounded edits to a start frame | **Flux Kontext / Seedream** | One narrow edit, preserves the rest | — |
| Remove an invented plate/badge from a clip | FLUX Video Edit ($0.15/5 s) | Clean object removal | — |
Budget rule: **block on the draft tier first, then spend once on the hero tier**. Check `orvideo.py --balance` first, and never top up without Chase's OK.

## 10. Prompt templates
**i2v hero (Kling/Grok/Seedance):**
```
Keep the <REAL SUBJECT, e.g. white next-gen Tesla Roadster> exactly as in the start frame: <3 identity features>.
<One action: start state → end state, "at about 2 s">.
Camera: <shot size>, <one move + speed>, ending on <framing>; no zoom, no cuts<, no pan>.
<Light/atmosphere change>. All plates, panels and screens stay blank and featureless.
```
**Phone beat (Method B plate):**
```
Medium close-up, eye level, vertical frame. A man holds a phone at chest height by its edges, thumb resting on the glass; the screen is off, glossy black glass reflecting warm room lights.
At about 1.5 s his thumb makes one short upward flick, then rests. Camera: locked-off static shot, shallow depth of field. No other movement.
```
**Hailuo:** `The white sports car idles on wet asphalt, then its headlights snap on at about 2 s [Static shot], then [Push in] slowly to the front light bar.`

## Sources (index)
- Kling: [3.0 guide](https://kling.ai/quickstart/klingai-video-3-model-user-guide) · [i2v guide](https://kling.ai/quickstart/image-to-video-guide) · [3.0 API i2v](https://kling.ai/document-api/api/video/3-0-omni/image-to-video.md) · [Kling blog: animate a picture](https://kling.ai/blog/how-to-animate-a-picture) · YouTube: [Omni cinematic tutorial](https://www.youtube.com/watch?v=WmC1nqz10Qk), [camera masterclass](https://www.youtube.com/watch?v=TKkg-8P7jTM), [Kling vs Seedance vs Veo](https://www.youtube.com/watch?v=-MluR9dqt5w)
- Veo: [Google Cloud prompting guide](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1) · [Gemini API Veo](https://ai.google.dev/gemini-api/docs/veo) · [references](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/generate-videos-from-references) · [first/last frame](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/generate-videos-from-first-and-last-frames)
- Seedance: [Runway help](https://help.runwayml.com/hc/en-us/articles/50488490233363-Creating-with-Seedance-2-0) · [Runway prompt guide](https://runway.com/resources/seedance-2-0-prompt-guide) · [seedance.tv guide](https://docs.seedance.tv/en/seedance-2-complete-prompting-guide) · [awesome-seedance-2-guide](https://github.com/EvoLinkAI/awesome-seedance-2-guide/blob/main/README.md) · [prompt examples](https://github.com/Emily2040/seedance-2.0/blob/main/references/prompt-examples.md)
- Grok Imagine: [xAI i2v docs](https://docs.x.ai/developers/model-capabilities/video/image-to-video) · [Replicate 1.5 readme](https://replicate.com/xai/grok-imagine-video-1.5/readme) · [community guide](https://github.com/seaimagineai/awesome-grok-imagine-prompts/blob/main/docs/guides/en-US.md) · [Vogue AI i2v guide](https://vogueai.net/blog/grok-imagine-1-5-image-to-video-prompt-guide)
- Hailuo: [t2v API](https://platform.minimax.io/docs/api-reference/video-generation-t2v) · [i2v API](https://platform.minimax.io/docs/api-reference/video-generation-i2v) · [first/last frame](https://platform.minimax.io/docs/api-reference/video-generation-fl2v) · [MiniMax video guide](https://github.com/MiniMax-AI/skills/blob/main/skills/frontend-dev/references/minimax-video-guide.md)
- Image models: [Nano Banana guide](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana) · [Seedream 5.0 Pro (fal)](https://fal.ai/learn/tools/how-to-use-seedream-5-0-pro-v2) · [Seedream API examples](https://piapi.ai/blogs/seedream-5-pro-api-guide) · [Flux Kontext editing](https://docs.bfl.ml/guides/prompting_editing_single_reference)
- Hands / artifacts: [Higgsfield hands & faces](https://higgsfield.ai/blog/ai-video-hands-faces) · [vflow hand deformation](https://vflow.live/fix/hand-deformation/) · [AI Tools Guidebook](https://aitoolsguidebook.com/en/articles/ai-video-hands-disappear-during-motion/) · [r/KlingAI_Videos hands](https://www.reddit.com/r/KlingAI_Videos/comments/1i4rr05/kling_hands/) · [r/aivideos Kling 3.0 consistency](https://www.reddit.com/r/aivideos/comments/1rxo19n/how_to_maintain_character_consistency_in_kling_30/)
- Screens: [r/vfx screen compositing rules](https://www.reddit.com/r/vfx/comments/169ogp2/what_are_the_rules_of_thumb_for_tv_phone_screen/) · [r/AfterEffects screen tracking](https://www.reddit.com/r/AfterEffects/comments/1qbpq74/made_a_tutorial_for_screen_tracking_after_using/) · [rotating phone](https://www.reddit.com/r/AfterEffects/comments/1pca587/how_to_replace_a_screen_on_a_rotating_phone_in/) · [Lowepost Mocha](https://lowepost.com/courses/after-effects/visual-effects/screen-replacement-in-after-effects-mocha-r42/)
- X creators: [@hanifproduktif workflow](https://x.com/hanifproduktif/status/2041495051956896191) · [@alessia_orbit Seedance vs Kling](https://x.com/alessia_orbit/status/2108917079411683406) · [@pt5films ref sheets](https://x.com/pt5films/status/2066967482573984247) · [@Kiber_Alla audio refs](https://x.com/Kiber_Alla/status/2078814921756754352) · [@jessica_coderx Seedance 2.5 vs 2.0](https://x.com/jessica_coderx/status/2083246424452710747) · [@techhalla one-reference workflow](https://x.com/techhalla/status/2066429770196209781) · [@EHuanglu shot-list image](https://x.com/EHuanglu/status/2054932203495440860) · [@martinleblanc hybrid crowds](https://x.com/martinleblanc/status/2070430506865271122)
- Prices: OpenRouter `GET /api/v1/videos/models` (checked Oct 17, 2026) and `research/openrouter-video-menu.md`.
