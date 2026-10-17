# Revboo shot checklist

Every shot passes **all of part A** before any money is spent on video, and **all of part B** before Chase sees it. Nothing ships with "it's just a draft."
The IDs (A1…, B1…) are what `tools/prompt_swarm.py` scores against. Background and the reasons behind each rule are in [`PROMPT-PLAYBOOK.md`](PROMPT-PLAYBOOK.md).

## A. Pre-render (prompt + start frame), all must be YES
| ID | Check | Pass means |
|---|---|---|
| **A1** | **Real subject, as Chase named it** | The prompt names the exact subject Chase asked for (e.g. "the real next-gen Tesla Roadster, white"), with 2-3 real identity features. No invented substitute or lookalike. If the named subject conflicts with a brand/legal rule in another doc, the shot is **blocked until Chase decides**. |
| **A2** | **Locked reference frame** | There's an approved start frame built from real reference photos of the subject, and the path is recorded. The prompt says to keep the subject exactly as in the start frame, and it does **not** re-describe or contradict the frame. Hero shots are never text-to-video. |
| **A3** | **Hands rule** | Hands are either (a) out of frame, (b) still and holding or resting on something, or (c) in a medium-or-wider shot doing one short (≤2 s) task with a stated start and end position. No hand close-up in motion, no hands touching between people, no typing. No "perfect hands" wording. |
| **A4** | **Crowd rule** | 1 person ideal, 2 max interacting. Any crowd is background-only: soft focus, silhouette or distant, doing one uniform simple action, no physical contact with the hero. |
| **A5** | **No AI text** | The prompt asks for no readable text, letters, numbers, logos, plates or UI from the model. Surfaces are described positively as blank or featureless. All copy is planned as a post composite in real fonts. Real in-frame brand assets are allowed only if flagged for frame-by-frame QA. |
| **A6** | **Screen-insert method** | Any phone, TV or panel screen has a stated method. **A**: the real ad is baked into the start frame and the phone is near-static. **B**: a dark glossy screen with reflections, to be planar-tracked, with glare re-applied, grain and blur matched, and fingers above the UI. Never a bare white "paste" screen without reflections re-applied. N/A only if there's no screen. |
| **A7** | **One action** | Exactly one primary action, written as start state → end state, with a rough time ("at ~2 s"). No chained multi-step choreography. |
| **A8** | **Camera specified** | Shot size + angle + one move (or locked-off) + speed + end framing, with the other axes locked ("no zoom, no cuts"). For 9:16: "vertical frame, subject upright, horizon level". |
| **A9** | **Point of the shot stated** | One line saying why the shot exists (the script beat or caption it supports). Every element of the prompt serves that point, and nothing else is in it. |
| **A10** | **Model fit and prompt hygiene** | The model is chosen per the routing table (PLAYBOOK §9). The syntax fits that model: Hailuo brackets, Seedance `@Image` roles, Kling/Veo short negative field, positive-only phrasing for Grok/Seedance. No "4K masterpiece" stacks. Length is reasonable (under ~120 words for i2v). Duration is 5-8 s unless there's a reason. |
| **A11** | **Budget preflight** | Cost estimated (PLAYBOOK §1/§9) and balance checked. Blocking on the draft tier comes before the hero tier. Never top up without Chase's OK. |
| **A12** | **Caption-safe composition** | The frame leaves space where captions go (keep text out of the top ~200 px and bottom ~300 px of 1080×1920, and off faces), and the subject isn't placed under the caption zone. |

## B. Post-render QA, all must be YES
Make the sheet first: `ffmpeg -i clip.mp4 -vf "fps=2,scale=270:-2,drawtext=text='%{pts\:hms}':x=5:y=5:fontcolor=white:fontsize=14,tile=6x5" -frames:v 1 qa_sheet.jpg` (one frame every **0.5 s**). For hands and faces, also step through the frames at full resolution around every action beat.

| ID | Check | Fail examples, and the fix |
|---|---|---|
| **B1** | **Hands and fingers** (every 0.5 s + action beats at full res) | 4 or 6 fingers, fused fingers, a melting wrist, a hand vanishing into an object. **Fix:** crop or reframe; trim to before the action; re-roll wider or with a hand-pose ref. |
| **B2** | **Faces** | Identity drift on a head turn, warped eyes or teeth, plastic skin (Kling on people). **Fix:** re-roll on Veo/Seedance with refs, or cut before the turn. |
| **B3** | **Morphing / physics** | The object changes shape, wheels or doors change, limbs pass through objects, something teleports. **Fix:** shorter clip, slower move, add an end frame. |
| **B4** | **Text** | Any AI-generated letters on signs, screens, plates or clothing. **Fix:** FLUX Video Edit removal, track + blur/inpaint, or re-roll with blank surfaces. Our post text: spelled right and readable ≥2.2 s. |
| **B5** | **Logos and badges** | Invented or wrong brand marks (Apple-style logos, Mercedes-like stars, a fake "R"). The Revboo logo reads exactly. **Fix:** template-track + inpaint, or FLUX Video Edit. |
| **B6** | **Subject consistency** | Side-by-side against the real reference photos at 0 s, mid and end: it's still the subject Chase named, in every frame. A wrong car or product = automatic re-roll. |
| **B7** | **Screen insert** | The UI stays pinned to the corners (no slide >2 px), has reflections and glare, matches the scene's exposure, black level, grain and blur, has motion blur on fast moves, and fingers sit above it. Looks like it was shot, not pasted. |
| **B8** | **Caption placement** | Captions sit in the safe zone, off faces, hands and the subject's key detail, and don't collide with the platform UI. |
| **B9** | **Audio** | No AI gibberish voices or music in the clip (unless planned); SFX land on the action; no clipping; mix level per PLAYBOOK. Real or approved VO only. |
| **B10** | **Point delivered** | The shot does its stated job (A9) inside the cut window, and the action lands where the edit needs it. |

**Scoring rule:** any part-A NO = rewrite the prompt or frame (no render). Any part-B NO = fix in post or re-roll, then re-run part B. Log the result in the credit log with the model, cost and which checks failed.
