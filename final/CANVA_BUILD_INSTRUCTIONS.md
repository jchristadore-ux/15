# CANVA BUILD INSTRUCTIONS — 15 YEARS OF US

Everything you need to assemble the film tonight.
Build order, durations and transitions are in **`CANVA_PRODUCTION_MANIFEST.csv`**
— 122 rows, in order, one row per screen. Build top to bottom and do not
re-sequence.

Both CSVs share **one numbering scheme**: sequence 001–122 counts every screen in
the film, photographs and text cards alike. Sequence 030 is the same screen in
`CANVA_PRODUCTION_MANIFEST.csv`, in `FINAL_PHOTO_MANIFEST.csv`, and in this
document. `FINAL_PHOTO_MANIFEST.csv` also carries a `photo_index` column
("12 of 110") if you want to know how far through the photographs you are.

**Design direction: cinematic, warm, timeless, simple.
There are no graphics in this film. The photographs are the design.**

No hearts, no frames, no borders, no floral dividers, no ribbons, no wedding
templates, no script fonts. If it looks like a template, delete it.

---

## 0. Before you open Canva

**This is already done for you.** A new folder has been created in your Drive:

> **`15 / 03 - FINAL CUT (upload in this order)`**
> https://drive.google.com/drive/folders/1jq9mtGKL8DoYQD_yCm_5KUAyeTlpXJ7h

It contains all **110 slots as copies, already renamed in build order**:

```
001_ch1_2000_couple_HERO.jpg
003_ch1_2000_couple.jpg
...
110_ch7_2023_HER-ALONE_HERO.jpg
...
119_ch7_2022_couple_FINAL-FRAME.jpg
```

Each name carries `sequence _ chapter _ year _ who`, and `_HERO` on the 34
frames that get the long holds. Download the whole folder as one zip and upload
it to Canva in one go — it will sort into build order by itself. Numbers are
**not** contiguous (002, 013, 033… are the text cards), which is correct.

**Your originals were not touched.** These are copies; nothing in
`01- DIGITAL PHOTOS` or `02 - OLD PHOTOS` was renamed, moved or modified. The
reprise frame appears twice on purpose, as `001_` and `099_…_REPRISE`, so you can
place every file in order without thinking about it.

Two things still to do by hand:

1. **Fix four rotated scans**, in any image viewer. They were scanned the
   wrong way up and Canva will not fix them for you:

   | seq | file | fix |
   |---|---|---|
   | 021 | `808238949.072203.jpg` | rotate — scanned sideways |
   | 029 | `808239361.376166.jpg` | rotate 180° — the *409 TAYLOR* wall, scanned upside down |
   | 030 | `808239495.070762.jpg` | rotate 180° — the graduation frame, scanned upside down |
   | 034 | `808239734.733836.jpg` | rotate and straighten — the house |

   (In the new folder these are `021_…`, `029_…`, `030_…` and `034_…`.)

2. **Apply the old-photograph grade** to the 35 scans — see §7. Everything with
   a `ch1` or `ch2` prefix, plus `034`, is a scan.

---

## 1. Canvas

| | |
|---|---|
| Design type | **Video** |
| Dimensions | **1920 × 1080 px** (16:9) |
| Frame rate | 30 fps (Canva default) |
| Total pages | 122 (110 photo slots + 12 text cards) |
| Target runtime | 8:47 |
| Export | MP4, 1080p |

Do not build in 4K. The archive's smallest selected file is 880 px wide and
upscaling will show.

---

## 2. Background treatment

Set every page background to **`#0E0C0B`** — a warm near-black, not pure black.

Pure `#000000` reads as "empty" on a TV; a warm charcoal reads as "cinema." It
also matters because 64 of your 110 slots are vertical photographs that will not
fill the frame, so this colour is on screen constantly.

Set it once on page 1, then use **Copy style → apply to all pages**, or just
duplicate page 1 as your template before you start placing.

---

## 3. Fonts

Two fonts. Both are in Canva's free library.

| Use | Font | Weight |
|---|---|---|
| Emotional lines, closing cards | **Cormorant Garamond** | Light |
| Dates, chapter markers | **Montserrat** | Light, ALL CAPS |

Cormorant Garamond is a high-contrast serif — it reads as timeless rather than
as "wedding". Montserrat in all-caps with wide letterspacing handles the dates
without looking like a document.

**Never use:** Great Vibes, Dancing Script, Brittany, or anything else
handwritten. They are the single fastest way to make this look like a template.

### Font sizing

| Element | Font | Size | Letterspacing | Colour |
|---|---|---|---|---|
| Dates (`March 15, 2002.` / `August 13, 2011.`) | Montserrat Light, caps | 58 px | +240 | `#E8E2D9` |
| Statement lines (`Then everything changed.`) | Cormorant Garamond Light | 96 px | +40 | `#F2EDE4` |
| Multi-line card (`Before the house.` …) | Cormorant Garamond Light | 78 px | +40 | `#F2EDE4` |
| Closing cards (`I'D STILL CHOOSE YOU.`) | Montserrat Light, caps | 68 px | +300 | `#F2EDE4` |
| Final card, line 1 | Cormorant Garamond Light | 92 px | +40 | `#F2EDE4` |
| Final card, line 2 (`15 years down…`) | Montserrat Light, caps | 42 px | +260 | `#B9AE9E` |

Line spacing on all multi-line cards: **1.6**.

Off-white (`#F2EDE4`), never pure white — it sits in the same warm family as the
photographs and does not glare.

---

## 4. Text placement

**No text is burned over any photograph in this film.** Every word appears on its
own full-screen card. This is deliberate: 12 cards across 8:47 is sparse enough
that each one registers, and the photographs are never competing with a caption.

On every card:
- Text block **centred horizontally**, sitting on the **optical centre** —
  roughly 46% down the frame, not 50%. Dead centre reads as slightly low.
- Keep all text inside a 200 px margin on every edge.
- One idea per card. Never two.

---

## 5. Photo placement

Three layouts, specified per-row in the `layout` column of the manifest.

### `FULL_BLEED_LANDSCAPE` — 40 slots
Scale to cover the full 1920 × 1080. Crop from the edges, never from a face.
Check every one: several scans have a white print border that must be cropped
out entirely.

### `FULL_BLEED_SOFT_CROP` — 6 slots
Nearly square. Scale to fill height, accept the side crop, keep the subject
centred.

### `VERTICAL_CENTERED_ON_BLURRED_FILL` — 64 slots
See below. This is the most important treatment in the build.

---

## 6. Vertical photo treatment

**Nearly 60% of this film is vertical**, including the final frame. Getting this
right is the difference between "a slideshow" and "a film."

Do **not** stretch vertical photos, and do **not** put them on flat black — a
tall photo floating on a black rectangle looks like a phone screenshot.

For each vertical slot:

1. **Place the photo twice on the page.**
2. **Back copy:** scale it up until it covers the full 1920 × 1080 (it will crop
   hard — that is fine, it is only a texture). Then **Edit image → Blur → about
   70**.
3. **Darkening layer:** draw a rectangle over the blurred copy covering the whole
   page, fill `#0E0C0B`, opacity **45%**. This stops the background competing
   with the real photo.
4. **Front copy:** the sharp original, scaled to **1080 px tall** (full frame
   height), centred horizontally. Nothing cropped.
5. Optional and worth it on hero frames: a **soft shadow** on the front copy —
   Canva's *Shadows → Glow*, colour `#000000`, blur high, transparency ~60. It
   lifts the photo off its own background.

Build this once, then **duplicate that page** as your template for all 64
vertical slots and swap the two images each time. Do not rebuild it 64 times.

### Ten frames that will go soft at full height

Most of the archive is big enough. These ten are not, and — awkwardly — several
of them are Chapter 7 heroes with the longest holds in the film, where softness
shows most:

| seq | pixels | hold | fix |
|---|---|---|---|
| 044 | 960×1280 | 4.0s | scale to 950 px tall, not 1080 |
| 046 | 960×1280 | 5.0s | scale to 950 px tall |
| 059 | 1334×1000 | 3.5s | fine at full height |
| 060 | 712×1062 | 3.0s | scale to 850 px tall |
| 061 | 1172×1334 | 4.5s | fine at full height |
| 074 | 648×1334 | 1.8s | short hold, leave it |
| 101 | 1165×769 | 2.5s | short hold, leave it |
| **113** | 648×1334 | 4.5s | **scale to 900 px tall** |
| **114** | 960×1280 | 6.0s | **scale to 950 px tall — this is a hero** |
| **117** | 880×1168 | 7.0s | **scale to 900 px tall — this is a hero** |

The rule: when a photograph is smaller than the frame, **do not stretch it to
fill the height**. Let it sit smaller on its own blurred backdrop. A slightly
smaller sharp photograph always looks better than a full-height blurry one, and
on the blurred-fill layout nobody can tell the difference in size.

None of these are worth cutting. They are all in the film because of what is in
them, not how they were shot.

---

## 7. Old photograph treatment (the 35 scans)

The scanned prints are from 2000–2013 and carry heavy flash and colour casts —
several have a strong red/magenta shift from on-camera flash. Left untouched next
to modern phone photos they look broken rather than old.

Apply to **every** file from `02 - OLD PHOTOS 2003-2013`, via **Edit image →
Adjust**:

| Setting | Value |
|---|---|
| Saturation | **−12** |
| Warmth | **+6** |
| Contrast | **+8** |
| Highlights | **−10** (recovers blown flash) |
| Vignette | **12** |

Five scans need more than the standard grade — these are the ones Phase 1 flagged
individually:

| seq | file | problem | extra correction |
|---|---|---|---|
| 012 | `808238395.515276.jpg` | blown-out flash (the kiss on the floor) | Highlights −25, Contrast +12 |
| 018 | `808239196.086460.jpg` | faded, colour-shifted print | Saturation −5 only, Warmth +12, Contrast +15 |
| 026 | `808239217.875130.jpg` | heavy red cast on his face | Saturation **−22**, Warmth −4 |
| 028 | `808239347.782889.jpg` | very heavy red flash cast | Saturation **−25**, Warmth −6 |
| 034 | `808239734.733836.jpg` | washed out and hazy (the house) | Contrast +22, Warmth +10 |

Sequence 018 is *faded*, not oversaturated — pulling colour out of it will make
it worse, which is why it goes the other way.

**Do not sepia them. Do not add a film-grain overlay. Do not add fake dust or
light leaks.** The goal is that a 2003 print and a 2026 phone photo feel like
they belong in the same film — one gentle unifying grade, not a filter.

**Four frames are already black and white in the original. Leave them alone —
do not "fix" any of them to colour:**

| seq | file | what it is |
|---|---|---|
| 030 | `808239495.070762.jpg` | his graduation |
| 054 | `IMG_0053(2).JPG` | all four of you, first time, hospital |
| 062 | `IMG_1158.JPG` | first day of school, the sisters hugging |
| 104 | `IMG_5913.JPG` | three sisters, looking back across the field |

Those four are spread evenly through the film — roughly one per act — which is
why they read as a deliberate choice rather than an accident. Do not add any
more black and white.

---

## 8. Zoom and pan

Use **Canva → Animate → Photo animations → Zoom**, set as slow as Canva allows.

| Where | Movement |
|---|---|
| Hero frames (marked `hero = YES`) | Very slow push **in**, ~5% over the hold |
| Standard frames | Very slow push **in**, ~3%, or static |
| **Chapter 5 — the chaos montage** | **Static. No movement at all.** |
| Text cards | Static |
| **Final frame** | Slow push in, ~3% over 12s |

Rules that matter more than the settings:

- **One direction per photograph.** Never in-then-out.
- **Never pan across a face.** If a zoom crops someone out mid-hold, make it static.
- Anything held under 2.5 seconds should be **static** — motion that short reads
  as a glitch. That covers the entire chaos montage.
- If Canva's slowest zoom still looks aggressive, **use static**. A still
  photograph held confidently always beats a nervous one.

---

## 9. Transitions

Canva applies transitions *between* pages. Four settings, specified per row in
the manifest's `transition` column:

| Manifest value | Canva setting | Duration |
|---|---|---|
| `CUT` / `HARD_CUT` | **None** | — |
| `CROSSFADE` | Dissolve | **0.5 s** |
| `SLOW_DISSOLVE` | Dissolve | **1.0 s** |
| `FADE_FROM_BLACK` / `FADE_THROUGH_BLACK` | Dissolve, through black | **0.75 s** |
| Opening (page 1) | Fade up from black | **2.0 s** |

**Chapter 5 is all hard cuts.** Fourteen photographs, no transitions between any
of them. That abruptness is the joke — it is what makes the montage feel like
chaos rather than a gallery.

`SLOW_DISSOLVE` is reserved for the emotional beats. It appears 24 times. Do not
add more.

`MATCH_CUT` appears twice, at sequences 099 and 100 — the hard cut from her at
seventeen to your daughter in her own kit. Treat it as a plain cut with no
transition; the name is there to tell you *why* it must not be a dissolve.

---

## 10. Timing

Durations are in the `duration_seconds` column. Set each page's duration
individually — do **not** use Canva's "apply to all pages."

The pacing logic, if you need to adjust:

| Kind of photograph | Hold |
|---|---|
| Chaos montage | 1.8 – 2.5 s |
| Standard | 3.0 – 4.5 s |
| Strong | 4.5 – 6.0 s |
| Major emotional beat | 6.0 – 9.0 s |
| Text card | 3.5 – 6.0 s |
| **Final frame** | **12.0 s** |

The four longest holds in the film are the hospital room at 2:59 (9 s), all four
of you for the first time at 3:57 (9 s), the opening frame (10 s) and the final
frame (12 s). Do not shorten any of them — the film's whole rhythm is built on
those four stops.

---

## 11. Voiceover placement

Record the script from `FINAL_STORYBOARD.md` in **twelve separate takes**, one
per cue. Do not record it as one continuous read — you will spend longer trying
to stretch a single file across nine minutes than re-recording it in pieces.

Upload all twelve, then place each at its cue timecode:

| Cue | Place at |
|---|---|
| VO-1 | 0:19 |
| VO-2 | 1:04 |
| VO-3 | 1:46 |
| VO-4 | 2:18 |
| VO-5 | 2:59 |
| VO-6 | 3:32 |
| VO-7 | 5:17 |
| VO-8 | 5:53 |
| VO-9 | 6:59 |
| VO-10 | 7:49 |
| VO-11 | 8:01 |
| VO-12 | 8:19 |

**Recording notes:**
- Phone voice memo in a carpeted room, phone about a hand's width from your
  mouth, is genuinely fine. Do not use the laptop's built-in mic.
- Read it slower than feels natural. The whole script is ~230 words across nearly
  nine minutes — you have room to leave silence.
- **The first 19 seconds have no voiceover and no music.** Let the opening
  photograph sit there. Resist filling it.
- Leave 1.5 s of silence at the head and tail of every take so nothing clips.
- It should sound like you talking to her, not like a narrator. If a take sounds
  polished, use the one before it.

---

## 12. Music placement

"Just Breathe" is 3:36. The film is 8:47, so it cannot carry the whole thing.
Use it as a **bookend** — it returns when the couple returns.

| Bed | Timecode | Track | Level |
|---|---|---|---|
| 1 | 0:19 – 2:54 | **"Just Breathe" — Pearl Jam**, from the start | Fade in over 4 s; fade out over 6 s under the "Then everything changed" card |
| 2 | 2:54 – 7:18 | One warm instrumental, **no vocals** | Fade in 4 s, out 5 s |
| 3 | 7:18 – 8:47 | **"Just Breathe" again**, from the start | Fade in 4 s; hold to the end; fade out over the last 6 s |

**Bed 1 starts at 0:19, not 0:00.** The first nineteen seconds — the opening
photograph and the date card — are silent. That silence is what makes the song
landing feel like the film starting.

**For bed 2**, pick something with no lyrics that builds slowly; it has to sit
under both the voiceover and the chaos montage without fighting either. Anything
piano- or string-led works. Avoid anything with a strong drum beat — Chapter 5 is
already busy.

**Levels:** music at about 35% under picture, ducked to **20%** under every
voiceover line. Canva's audio timeline lets you set volume per clip; split the
music clip at each VO cue and drop the level rather than trying to automate it.

---

## 13. The final frame

Sequence 119, `IMG_0705.JPG` — golden hour by the water.

- **12 seconds**, vertical treatment as section 6, ~3% slow push in.
- **No text over it.** Nothing. The three closing cards come after it, on black.
- VO-12 plays over it, ending on *"I'd still choose you."*
- Let the last line finish, then hold roughly 1.5 s of picture in silence before
  the fade begins. That gap is the most important second and a half in the film.

**If you want to change it:** four ranked alternatives are argued in
`FINAL_HERO_CANDIDATES.csv`. Swap the image in sequence 119 and change nothing
else — the hold and card sequence work with any of the five.

---

## 14. Fade timing (the last 30 seconds)

| Time | What | Fade |
|---|---|---|
| 8:19 | Final photograph, 12 s | in over 1.0 s |
| 8:31 | `24 YEARS TOGETHER. / 15 YEARS MARRIED.` | through black, 0.75 s each side |
| 8:36 | `I'D STILL CHOOSE YOU.` | through black, 0.75 s |
| 8:41 | `HAPPY 15TH ANNIVERSARY, MY LOVE.` / `15 years down. Forever to go.` | in 0.75 s, **out over 4.0 s** |
| 8:47 | Black | hold **2 s** before the file ends |

That closing 4-second fade and the 2 seconds of black after it are what stop the
film from feeling like it was cut off. Do not trim them.

---

## 15. Opening variants

The cut opens on the lacrosse frame at 0:00 and reveals `March 15, 2002.` at
0:10. Two alternatives, if you prefer:

- **Card first.** Move `March 15, 2002.` to page 1 and the photograph to page 2.
  Cleaner and more literal, but you lose the ten seconds of silence, which is the
  strongest thing in the opening.
- **Strictly literal.** The opening two frames are stamped spring 2000, two years
  before the verified start of the relationship. If you'd rather the film not
  open before its own start date, begin instead with sequence 014
  (`808238834.918744.jpg`, the dorm room) and move the two lacrosse frames into
  the Chapter 6 callback. You would lose the strongest opening image in the
  archive to gain literal accuracy — I would not, but it is your film.

---

## 16. Before you export

- [ ] All four rotated scans fixed (§0)
- [ ] Page durations set individually — spot-check the 9 s, 10 s and 12 s holds
- [ ] Chapter 5 has **no** transitions and **no** animation
- [ ] All 64 vertical slots have the blurred backdrop, not flat black
- [ ] The old-photo grade is applied to all 35 scans
- [ ] No text is sitting on top of any photograph
- [ ] The three already-black-and-white frames are still black and white
- [ ] Music ducks under every one of the twelve voiceover lines
- [ ] The film is silent for the first 19 seconds
- [ ] **Watch it once, all the way through, without stopping.** If one of your
      three daughters feels thinner than the others, that is the one thing the
      archive analysis could not check for you — say so and it can be rebalanced
      in minutes.

Export MP4 1080p. Roughly 350–450 MB.
