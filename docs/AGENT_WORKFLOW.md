# RevBoo shared production and filing contract · v1

## One home, every agent
Repository: https://github.com/Cryptouprise/revboo-library
Media browser: https://cryptouprise.github.io/revboo-library/

Read this file and current `catalog/registry.json` at the start of work. An agent must have its own authorized GitHub connection or authenticated `gh`; this document does not grant access, share credentials, or make Claude/Grok inherit ChatGPT permissions.

`catalog/registry.json` owns concept IDs, revision links and approval pointers. `manifest.json` owns playable gallery URLs and existing release IDs. Link these through `asset_id`; do not rename legacy IDs or URLs. The registry initializes existing entries without claiming playback QA. Update both in the same change when adding gallery media. A private ChatGPT index is a convenience snapshot, not a second source of truth.

## Names and categories
Permanent concept IDs: RB-001 (RevBoo), PI-001 (legacy Legal/PI collection), AS-001 (Assist), IA-001 (Infinite AI), SF-001 (Solar Freedom), GE-001 (other), CLIP-001 (source clip). Existing assignments never change. Add a client prefix through a small reviewed registry change; never put new clients under the wrong advertiser just to fit an old collection.

Export pattern: `RB-001__ad-autopsy__A__v04__9x16.mp4`.
- A is an intentional test branch, such as a different hook or offer. Revisions within A increment v04 to v05.
- Alternate aspect ratios share concept and branch/revision, but have distinct asset IDs.
- A new concept gets a new concept ID. A typo fix, speed change or crop does not.
- Release ID: `rb-001-a-v04-9x16`. Each exported version has a unique immutable release ID.
- Titles are plain English; preserve previous filenames as searchable aliases.

Every asset needs a category. Ads: Comedy/skit, UGC/presenter, Teardown, Motion graphics, B-roll/VO, Product/UI demo, Brand promo, or Other (explain). Clips: use README's established categories (Cars/Engine, Phones & Scrolling, People/Reactions, Legal/PI, Products, Brand cards & Logo, Transitions/FX). Category is separate from brand, audience, and asset kind. Legacy categories are retained until reviewed.

## Required records
Use `catalog/intake-template.json` for every new asset. Fill:
- concept_id, asset_id, title, kind (ad/clip), collection, advertiser, audience, category, aliases;
- branch, revision, format, parent_asset_id, request, change_log, created_by, created_at;
- master reference and SHA-256, preview URL, native/export dimensions, duration;
- exact script/verified transcript, hook, offer, CTA, voice/model and reusable source asset IDs;
- workflow status, QA results and remaining issues, approval evidence, rights/reuse limits;
- cost estimate/actual by video/audio/edit/review; unknown is null, not zero;
- live platform IDs and measurement window only when actually launched.
Keep credentials, client private URLs, private scripts and sensitive IDs out of this public repository. For unpublished client work, keep the complete record/media in the user's approved private storage and supply a redacted handoff until public publication is authorized.

## Find before creating
Search title, concept ID, aliases, notes and verified transcripts. Inspect the actual requested source. Hash local files to catch exact duplicates; matching names alone do not prove equality. Reuse a registered concept. Do not guess two unrelated videos are versions of one another. A missing local path is not proof the master is lost; resolve recorded persistent references.

## Concurrency and ID reservations
1. Fetch current main. Work on your own branch `agent/<agent>/<task>-<unique-suffix>`.
2. Existing concept: reference its permanent ID. New concept: prepare a reservation-only registry change using the next unused ID for that prefix, title and agent. Its assets list may be empty while reserved.
3. Merge reservations one at a time against current main, then refresh. Until merged, the proposed numeric ID is provisional. Do not upload a release using an unreserved ID.
4. If another agent took the number, select the next unused one and resolve before uploading. Never renumber an already registered concept. A branch name is not a lock.
5. Before final merge, fetch/rebase against current main, resolve registry/manifest changes and run the validator. Use non-force pushes. Never replace someone else's file with a stale full copy. No automatic conflict overwrite.
These are cooperative rules plus validation; branch protection/merge queue has not been configured. The validator catches structural collisions, not all semantic or simultaneous editing errors.

## Revision and approval
Resolve exact parent. Record what changes and what is protected (voice, shots, music, captions). Preserve approved elements; regenerate only failing shots. Keep immutable attempts and total costs.
Statuses: Inbox → Draft → Review → Approved → Live; also Archived and Rejected. Latest is not Approved. Existing entries are Review unless explicitly rejected; legacy final labels remain historical metadata only.
An approved pointer names the exact asset ID/hash, approver and timestamp. Approval does not transfer to an edit. Live requires platform ID and launch record. Do not invent approval or report technical checks as full audiovisual QA. Inspect complete speech, voice identity, lip sync, motion, numbers, offer, CTA, mobile text and ending; record checks actually completed.

## Upload through the existing pipeline
Only after access, public-publication authorization and ID reservation are established:

```bash
# In an up-to-date authorized checkout; use your own credentials.
gh auth status
python3 build.py add /absolute/path/RB-001__ad-autopsy__A__v04__9x16.mp4 --id rb-001-a-v04-9x16 --title "Ad Autopsy" --group "Ad Autopsy" --version "A v04 / 9:16" --brand "Revboo" --category "Teardown" --note "Review cut; CTA revised; launch QA pending."
```

For a reusable clip, use `--type clip`, `--categories` and `--used-in` per README. Never automatically publish a private client draft. The legacy builder rebuilds metadata from its source configuration; use the production checkout containing the existing masters/configuration, and inspect the diff for dropped entries. If originals are missing, use the documented manual release intake instead of rebuilding away the catalog.

`build.py` can print an upload WARNING without successful publication. Inspect output, release record, size/hash and final URL; success of the shell command alone is insufficient. No overwrite flags. GitHub Release MP4s are immutable; keep originals privately in durable storage and label compressed previews as previews.

Update registry concept.assets and revision_records using the template; retain manifest id/group/categories, record reuse links. Run:

```bash
python3 tools/validate_catalog.py
```

Commit only intended metadata/posters and open a PR. Never `git add` MP4s, keys, private client records or unrelated files. Publish/merge only within user authorization. Verify the preview plays with sound after deployment; preserve unverified items as such. Return concept ID, version, playable URL, changes and QA/approval state.

## Agent without upload access
Prepare a handoff bundle: video master, preview/poster if generated, intake JSON, source references, script, change log, QA and costs. Use a provisional UUID if no shared ID is reserved. Say “Prepared, not uploaded.” Give the bundle to an authorized agent/human; do not ask for credentials in chat or pretend you uploaded.

## Reuse and reporting
Record source clip IDs under each ad and reverse used_in references under clips. Confirm brand/voice/rights constraints before reuse. Store measured performance against the exact live asset; ideas and technical QA are not evidence of winning performance.

## Agent tags and attribution
Use Created by and Last edited by with a consistent readable agent name: ChatGPT, Claude, Grok, Human, Unknown, or any additional AI. Agent names are extensible; do not force new agents into an existing name. Keep the model/version in a separate field. Record agent_tags for all contributors and an append-only history of timestamp, agent, action and parent asset ID. An editor must not overwrite the original creator. Imported legacy work stays Unknown unless source evidence identifies the creator. Tags describe provenance, not model quality. Filter by agent while preserving one shared collection; do not fork a separate catalog per agent.

## Muse and media operations
Read docs/MUSE_ANALYTICS.md for launch handoffs, exact creative-to-ad mapping, metric definitions, data imports and decision logs. Tag Muse (or another operator) in operated_by separately from created_by/last_edited_by. Marketing account data stays private; no account credentials or performance rows in this public repository.

## Grouped versions and edit requests
Creative Command shows one card per registered concept, with a version selector and all-version history. Search retains the full matching concept family. A selected preview is not launch approval. “Request an edit” includes the immutable source asset, concept ID, version, URL, time range, requested change and protected elements. The player can capture its current timestamp. Requests are copied/downloaded locally; no task is submitted automatically. The receiving agent must resolve this exact source, make a new revision and keep the old export. Deep links use command.html?asset=<exact-asset-id>.
