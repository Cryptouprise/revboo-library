# Revboo Video Library

Live page: https://cryptouprise.github.io/revboo-library/

Everything on the page comes from `manifest.json`.

## Adding a new video (easy way)
1. Put the mp4 in `media/finals/` (finished ad, under ~6 MB) or `media/clips/` (short clip, under ~1.5 MB).
2. Put a poster image (one frame as .jpg) in `media/posters/`.
3. Add one entry to `manifest.json`:
   - Finished ad → `finals` list: `id, group, title, version, date, datetime, duration, video, poster, status, note`.
     Use the same `group` as the older versions and set `category` ("Revboo ads" or "Seedance originals (made by Chase)" or a new name, which becomes a new heading); the newest `datetime` in a group is shown as LATEST and the others collapse under it.
   - Clip → `clips` list: `id, name, categories, used_in, note, date, datetime, duration, video, poster`.
4. Commit and push. GitHub Pages updates in about a minute.

## Rebuild from the source files (on the box)
`python3 build.py` in `/workspace/revboo/library/` re-encodes anything new from `/workspace/revboo/`, makes posters and rewrites `manifest.json`.
To add a source file, add one line to the `FINALS` or `CLIPS` list in `build.py`. Revboo-Counselor-v2.mp4 is already listed and gets picked up automatically once it exists.
