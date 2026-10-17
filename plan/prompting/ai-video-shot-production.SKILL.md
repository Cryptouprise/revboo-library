---
name: ai-video-shot-production
description: Use when producing AI-generated video shots (Kling, Veo, Seedance, Grok Imagine, Hailuo, etc.) for an ad or film and the first drafts need to be near-final. Runs the reference-frame, prompt-swarm, native-screen and QA loop that prevents bad hands, garbled text, pasted-on screens and the wrong subject.
---
# AI video shot production (reference frame → prompt swarm → render → QA)

## Inputs to collect per shot
- The **exact subject** the requester named (a real product, car or person). Write it verbatim. Never substitute an invented lookalike. If it conflicts with a brand or legal rule, stop and ask the requester.
- One line: **the point of the shot** (which script beat it serves).
- Target model and budget. Check the balance first and never top up without approval.

## Steps
1. **Collect real references.** Get 3-6 real photos of the named subject (official or press images, or the requester's own). These drive the start frame and are the QA comparison set.
2. **Build a locked start frame** with an image model (Nano Banana Pro, Seedream or Flux Kontext):
   - Use the formula `[references] + [relationship instruction] + [new scenario]`, at the final aspect ratio and lens.
   - Say what must stay identical. Do one narrow edit per pass.
   - Blank all plates, badges, signage and screens unless a real asset is meant to be there.
   - Hands are anatomically clean and placed on an object, or out of frame.
   - Leave caption-safe space.
   - Get approval on the still before spending video money.
3. **Plan any screen insert before rendering.**
   - **Method A:** bake the real UI into the start frame and keep the device nearly still for ≤5 s.
   - **Method B:** render the screen dark and glossy so it keeps its real reflections. Then planar-track 4 corners, warp the UI, and match exposure, black level, grain, blur and motion blur. Re-apply the plate's glare and reflections on top in screen/add mode, and mask fingers above the UI.
   - Never use a bare white paste screen.
4. **Prompt swarm.** Run a cheap or free LLM to write N candidate prompts per the playbook rules, then a second cheap critic call to score each one against the pre-render checklist. Add a deterministic lint, keep the best, fix what it flags, and repeat until it passes. Each prompt has:
   - **Source lock:** keep the subject exactly as in the start frame, plus 2-3 identity features. Don't re-describe or contradict the frame.
   - **One action** written as start state → end state, with a time ("at ~2 s").
   - **One camera move:** shot size, angle and speed, with the other axes locked ("no zoom, no cuts").
   - **Blank surfaces** described positively ("panels stay blank").
   - **Model syntax:** Hailuo `[brackets]`, Seedance `@Image` roles, a short negative field only on Kling or Veo, positive-only phrasing on Grok and Seedance.
   - No quality-word stacks. Under ~120 words. Clip length 5-8 s.
5. **Pre-render gate.** Every item must pass:
   - real subject
   - locked frame
   - hands rule: hands big and still, or medium-wide doing one ≤2 s task, or cropped out
   - crowd rule: 1-2 people; any crowd soft or silhouetted in the background
   - no AI text
   - screen method
   - one action
   - camera specified
   - point stated
   - model fit
   - budget
   - caption-safe framing
6. **Render cheap, then hero.** Block timing on a draft tier (lite/mini/turbo, low resolution), then render the hero tier once. Use an end frame when the shot must land on something specific, and colour-match it to the start frame. For continuity, chain shots from the last frame of the approved previous clip.
7. **Post-render QA.** Make a contact sheet at one frame every 0.5 s, and step through action beats at full resolution. Check:
   - hands and fingers
   - faces and identity drift
   - morphing and physics
   - AI text
   - logos and badges
   - subject vs. the real references at start, middle and end
   - screen insert: pinned, reflective, matched
   - caption placement
   - audio
   - whether the point of the shot was delivered
   Any fail means a post fix (crop, trim, object removal, track and inpaint, composite) or a re-roll, then QA again.
8. **Finish in post.** All type in real fonts. Screen UI composited. Invented plates and logos removed. Log the model, cost and failed checks for next time.

## Model routing (rule of thumb)
| Model | Best for |
|---|---|
| Kling 3.0 Pro | product or vehicle hero motion from a start frame |
| Veo 3.1 | realistic people, faces, dialogue |
| Seedance 2.x | action, multi-reference consistency, hands with a pose reference |
| Hailuo | exact camera commands, in-frame brand assets |
| Grok Imagine lite | cheap blocking |
| Nano Banana Pro / Seedream / Flux Kontext | start frames and bounded edits |
