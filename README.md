# 15 YEARS OF US

Working repository for a 15th wedding anniversary film — a short documentary
assembled from a family photo archive, scored to "Just Breathe" (Pearl Jam).

## Status: PHASE 1 (archive analysis) — in progress

The archive is **not** final. Physical photographs from 2003–2013 are still
being digitized, so no photo selection here should be treated as locked.

## Source archive

Google Drive: `15 YEARS OF US`
- `01- DIGITAL PHOTOS 2013-2026` — 304 photos (phone cameras, mostly EXIF-dated)
- `02 - OLD PHOTOS 2003-2013` — 110 photos (scans of physical prints)

The Drive archive is treated as **read only**. Nothing in it is renamed,
moved, edited, or deleted by any of this tooling.

## Layout

- `analysis/` — inventory, candidate pools, best-of collections, storyboard, reports
- `pipeline/` — the scripts that produce them

## Pipeline

| script | what it does |
|---|---|
| `extract.py` | EXIF (date, camera, lens, GPS) plus measured sharpness/brightness/contrast and three perceptual hashes |
| `cluster.py` | exact duplicates (MD5), near-duplicates (perceptual hash distance), burst detection, era assignment |
| `contactsheet.py` | labeled contact sheets for visual review |
| `build_inventory.py` | merges measured facts + visual annotations into `ARCHIVE_INVENTORY.csv` |

## Dating: an important caveat

Every photo in `02 - OLD PHOTOS` was digitized with Google PhotoScan, so its
EXIF timestamp is **the moment it was scanned, not when it was taken**. Taken at
face value this files the entire 2003–2013 era under "today" and inverts the
film's chronology. The pipeline detects these and marks them
`UNKNOWN (scanned print - date TBD)` for visual dating instead.

Confidence is recorded on every date as HIGH / MEDIUM / LOW / UNKNOWN. Nothing
is guessed silently.
