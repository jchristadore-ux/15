# 15 YEARS OF US

Working repository for a 15th wedding anniversary film — a short documentary
assembled from a family photo archive, scored to "Just Breathe" (Pearl Jam).

## Status: FINAL CUT LOCKED

**109 photographs · 12 text cards · 8 min 47 s.** Everything needed to build the
film is in `final/`.

The wedding album is **deliberately not used**. It is a separate annual
tradition; this film is about everything around it. There is no wedding chapter
and none is needed — the marriage is carried by a date card, the house, and the
years on either side of it.

| Deliverable | What it is |
|---|---|
| `final/FINAL_STORYBOARD.md` | The selection and the cut, chapter by chapter, with timecodes |
| `final/CANVA_BUILD_INSTRUCTIONS.md` | How to build it in Canva tonight |
| `final/CANVA_PRODUCTION_MANIFEST.csv` | 122 rows, in build order — one per screen |
| `final/FINAL_PHOTO_MANIFEST.csv` / `.json` | Every photograph, fully specified |
| `final/FINAL_HERO_CANDIDATES.csv` | Top 5 for the final frame — his call, not mine |

Both manifests share one numbering scheme: sequence 001–122 counts every screen
in the film, photographs and text cards alike.

## Source archive

Google Drive: `15 YEARS OF US`
- `01- DIGITAL PHOTOS 2013-2026` — 304 photos (phone cameras, mostly EXIF-dated)
- `02 - OLD PHOTOS 2003-2013` — 110 photos (scans of physical prints)

The Drive archive is treated as **read only**. Nothing in it is renamed,
moved, edited, or deleted by any of this tooling.

## Layout

- `final/` — the locked cut: storyboard, build instructions, manifests
- `analysis/` — Phase 1 inventory, candidate pools, best-of collections, reports
- `pipeline/` — the scripts that produce them

## Pipeline

| script | what it does |
|---|---|
| `extract.py` | EXIF (date, camera, lens, GPS) plus measured sharpness/brightness/contrast and three perceptual hashes |
| `cluster.py` | exact duplicates (MD5), near-duplicates (perceptual hash distance), burst detection, era assignment |
| `contactsheet.py` | labeled contact sheets for visual review |
| `build_inventory.py` | merges measured facts + visual annotations into `ARCHIVE_INVENTORY.csv` |
| `curate_final.py` | holds the locked edit decision list and emits everything in `final/` |

## Dating: an important caveat

Every photo in `02 - OLD PHOTOS` was digitized with Google PhotoScan, so its
EXIF timestamp is **the moment it was scanned, not when it was taken**. Taken at
face value this files the entire 2003–2013 era under "today" and inverts the
film's chronology. The pipeline detects these and marks them
`UNKNOWN (scanned print - date TBD)` for visual dating instead.

Confidence is recorded on every date as HIGH / MEDIUM / LOW / UNKNOWN. Nothing
is guessed silently.
