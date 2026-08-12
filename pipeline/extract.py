#!/usr/bin/env python3
"""Extract EXIF + technical metrics + perceptual hashes for every downloaded photo.

Writes work/base_metadata.json — the factual spine of ARCHIVE_INVENTORY.csv.
Nothing here is inferred: every field is read off the file or computed from pixels.
"""
import json, os, glob, sys, math
from PIL import Image, ExifTags
import imagehash
import numpy as np

SP = "/tmp/claude-0/-home-user-OpenFIN/2e259a81-ccde-53fc-8059-70cd5c69f215/scratchpad"
ORIG = os.path.join(SP, "originals")
WORK = os.path.join(SP, "work")

TAGS = {v: k for k, v in ExifTags.TAGS.items()}


def rational(v):
    try:
        return float(v)
    except Exception:
        return None


def gps_to_deg(ref, val):
    try:
        d, m, s = [float(x) for x in val]
        deg = d + m / 60.0 + s / 3600.0
        if ref in ("S", "W"):
            deg = -deg
        return round(deg, 5)
    except Exception:
        return None


def sharpness(gray):
    """Variance of Laplacian — higher = sharper. Standard blur metric."""
    a = np.asarray(gray, dtype=np.float64)
    k = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=np.float64)
    h, w = a.shape
    if h < 5 or w < 5:
        return 0.0
    out = (a[:-2, 1:-1] * k[0, 1] + a[1:-1, :-2] * k[1, 0] + a[1:-1, 1:-1] * k[1, 1]
           + a[1:-1, 2:] * k[1, 2] + a[2:, 1:-1] * k[2, 1])
    return float(out.var())


def main():
    rows = []
    files = sorted(glob.glob(os.path.join(ORIG, "*")))
    for p in files:
        base = os.path.basename(p)
        fid, _, title = base.partition("__")
        rec = {"file_id": fid, "filename": title.replace("_", " ") if " " not in title else title,
               "stored_name": base, "path": p, "bytes": os.path.getsize(p)}
        try:
            im = Image.open(p)
        except Exception as e:
            rec["error"] = f"unreadable: {e}"
            rows.append(rec)
            continue

        rec["width"], rec["height"] = im.size
        rec["megapixels"] = round(im.size[0] * im.size[1] / 1e6, 2)
        rec["orientation_shape"] = ("portrait" if im.size[1] > im.size[0]
                                    else "landscape" if im.size[0] > im.size[1] else "square")
        rec["aspect"] = round(im.size[0] / im.size[1], 3) if im.size[1] else None

        # ---- EXIF ----
        try:
            ex = im.getexif()
        except Exception:
            ex = None
        if ex:
            top = {ExifTags.TAGS.get(k, k): v for k, v in ex.items()}
            rec["make"] = str(top.get("Make")).strip() if top.get("Make") else None
            rec["model"] = str(top.get("Model")).strip() if top.get("Model") else None
            rec["software"] = str(top.get("Software")).strip() if top.get("Software") else None
            rec["exif_datetime"] = str(top.get("DateTime")) if top.get("DateTime") else None
            try:
                sub = {ExifTags.TAGS.get(k, k): v for k, v in ex.get_ifd(0x8769).items()}
            except Exception:
                sub = {}
            rec["datetime_original"] = str(sub.get("DateTimeOriginal")) if sub.get("DateTimeOriginal") else None
            rec["lens"] = str(sub.get("LensModel")) if sub.get("LensModel") else None
            rec["iso"] = sub.get("ISOSpeedRatings")
            fn = rational(sub.get("FNumber"))
            rec["f_number"] = round(fn, 2) if fn else None
            et = rational(sub.get("ExposureTime"))
            rec["exposure_time"] = et
            try:
                g = ex.get_ifd(0x8825)
                gg = {ExifTags.GPSTAGS.get(k, k): v for k, v in g.items()} if g else {}
            except Exception:
                gg = {}
            if gg.get("GPSLatitude"):
                rec["gps_lat"] = gps_to_deg(gg.get("GPSLatitudeRef"), gg.get("GPSLatitude"))
                rec["gps_lon"] = gps_to_deg(gg.get("GPSLongitudeRef"), gg.get("GPSLongitude"))
            rec["exif_tag_count"] = len(ex)
        else:
            rec["exif_tag_count"] = 0

        # ---- pixel-derived technical metrics ----
        try:
            small = im.convert("RGB")
            small.thumbnail((400, 400))
            gray = small.convert("L")
            arr = np.asarray(gray, dtype=np.float64)
            rec["sharpness"] = round(sharpness(gray), 1)
            rec["brightness"] = round(float(arr.mean()), 1)
            rec["contrast"] = round(float(arr.std()), 1)
            hsv = np.asarray(small.convert("HSV"), dtype=np.float64)
            rec["saturation"] = round(float(hsv[:, :, 1].mean()), 1)
            # perceptual hashes for duplicate / near-duplicate grouping
            rec["phash"] = str(imagehash.phash(small))
            rec["dhash"] = str(imagehash.dhash(small))
            rec["ahash"] = str(imagehash.average_hash(small))
        except Exception as e:
            rec["error"] = f"pixel metrics failed: {e}"

        rows.append(rec)

    os.makedirs(WORK, exist_ok=True)
    with open(os.path.join(WORK, "base_metadata.json"), "w") as f:
        json.dump(rows, f, indent=1)
    print(f"extracted: {len(rows)}")
    withexif = sum(1 for r in rows if r.get("datetime_original"))
    print(f"with DateTimeOriginal: {withexif}  ({100*withexif//max(len(rows),1)}%)")
    print(f"with GPS: {sum(1 for r in rows if r.get('gps_lat'))}")


if __name__ == "__main__":
    main()
