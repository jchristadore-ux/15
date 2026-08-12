#!/usr/bin/env python3
"""Merge visual annotations with measured metadata -> all Phase 1 CSV deliverables.

Annotation keys are sheet labels (D### for digital, S### for scans); the order
files map those back to real files, and from there to Drive file ids.
Anything never reviewed is emitted as NOT_REVIEWED, never guessed.
"""
import json, os, csv, glob, re

SP = "/tmp/claude-0/-home-user-OpenFIN/2e259a81-ccde-53fc-8059-70cd5c69f215/scratchpad"
WORK = os.path.join(SP, "work")
OUT = "/home/user/15_YEARS_OF_US"

FOLDER = {
    "1EPwabfad6nXw1I3DmHBhHso45_92LVnb": "01- DIGITAL PHOTOS 2013-2026",
    "1Usv9KcgoM-zQfzFL32a93cls33MkJbF2": "02 - OLD PHOTOS 2003-2013",
}


def load_orders():
    """label -> file_id, using the order files that drove the contact sheets."""
    lab2fid = {}
    for name in ("order_digital.tsv", "order_scans.tsv"):
        p = os.path.join(WORK, name)
        if not os.path.exists(p):
            continue
        for line in open(p):
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 2:
                continue
            label, path = parts[0], parts[1]
            base = os.path.basename(path)
            fid = base.split("__")[0]
            # ids may themselves contain '__'; recover by matching the stored name
            lab2fid[label] = fid
        # fix ids containing/ending with underscores by re-deriving from disk
    return lab2fid


def true_fid(path, valid):
    base = os.path.basename(path)
    for v in valid:
        if base.startswith(v + "__"):
            return v
    return base.split("__")[0]


def main():
    valid = [l.split("\t")[0].strip() for l in open(os.path.join(WORK, "all_full.txt"))]
    validset = set(valid)

    lab2fid = {}
    for name in ("order_digital.tsv", "order_scans.tsv"):
        p = os.path.join(WORK, name)
        if not os.path.exists(p):
            continue
        for line in open(p):
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 2:
                continue
            lab2fid[parts[0]] = true_fid(parts[1], validset)

    ann = {}
    for p in sorted(glob.glob(os.path.join(SP, "ann", "*.json"))):
        try:
            d = json.load(open(p))
        except Exception as e:
            print(f"  !! skipping unparseable {os.path.basename(p)}: {e}")
            continue
        for label, entry in d.items():
            fid = lab2fid.get(label)
            if not fid:
                continue
            entry["_label"] = label
            # merge, don't replace: date-only passes must not clobber full annotations
            if fid in ann:
                ann[fid].update({k: v for k, v in entry.items() if v not in (None, "")})
            else:
                ann[fid] = dict(entry)

    rows = json.load(open(os.path.join(WORK, "clustered.json")))
    drive = {}
    for d in json.load(open(os.path.join(WORK, "drive_meta.json"))):
        drive[d["id"]] = d
    p2 = os.path.join(WORK, "folder02_meta.json")
    if os.path.exists(p2):
        j = json.load(open(p2))
        for d in (j.get("files") if isinstance(j, dict) else j):
            d.setdefault("parentId", "1Usv9KcgoM-zQfzFL32a93cls33MkJbF2")
            d.setdefault("viewUrl", f"https://drive.google.com/file/d/{d['id']}/view")
            drive[d["id"]] = d

    def sortkey(r):
        a = ann.get(r["file_id"], {})
        # prefer EXIF date; else the visually estimated year
        if r.get("est_datetime"):
            return (0, r["est_datetime"])
        est = str(a.get("est_date", "")) or ""
        m = re.search(r"(19|20)\d{2}", est)
        return (0, f"{m.group(0)}-06-15 00:00:00") if m else (1, r.get("filename", ""))

    rows.sort(key=sortkey)

    out = []
    for i, r in enumerate(rows, 1):
        fid = r["file_id"]
        d = drive.get(fid, {})
        a = ann.get(fid, {})
        folder = FOLDER.get(d.get("parentId", ""), "UNKNOWN")

        if r.get("est_date"):
            est, conf, src = r["est_date"], "HIGH", r.get("date_source", "EXIF")
        elif a.get("est_date") and a.get("est_date") != "UNKNOWN":
            est = a["est_date"]
            conf = a.get("date_confidence", "LOW")
            src = "visual estimate: " + a.get("date_evidence", "")
        else:
            est, conf, src = "UNKNOWN", "UNKNOWN", r.get("date_source", "")

        era = r.get("era", "")
        if era.startswith("UNKNOWN") and a.get("era") and a["era"] != "UNKNOWN":
            era = a["era"]

        tq = "UNREADABLE" if r.get("error") else None
        if not tq:
            s, b, mp = r.get("sharpness") or 0, r.get("brightness") or 0, r.get("megapixels") or 0
            f = []
            if s < 80: f.append("soft")
            if b < 55: f.append("dark")
            if b > 205: f.append("blown")
            if mp < 0.5: f.append("low-res")
            tq = "GOOD" if not f else "USABLE (" + ",".join(f) + ")"

        out.append({
            "unique_id": f"P{i:03d}", "sheet_label": a.get("_label", ""),
            "filename": d.get("title") or r.get("filename"),
            "drive_path": f"15 YEARS OF US/{folder}", "drive_url": d.get("viewUrl", ""),
            "file_type": d.get("mimeType", "image/jpeg"),
            "width": r.get("width", ""), "height": r.get("height", ""),
            "file_size_bytes": r.get("bytes", ""),
            "exif_date": r.get("datetime_original") or "",
            "estimated_date": est, "date_confidence": conf, "date_source": src,
            "source_folder": folder,
            "people_visible": a.get("people", "NOT_REVIEWED"),
            "people_count": a.get("people_count", ""),
            "family_grouping": a.get("grouping", "NOT_REVIEWED"),
            "location": a.get("location", "UNKNOWN"),
            "event": a.get("event", "NOT_REVIEWED"),
            "era": era or "UNKNOWN",
            "theme": a.get("theme", "NOT_REVIEWED"),
            "technical_quality": tq,
            "duplicate_group": r.get("duplicate_group", ""),
            "near_duplicate_group": r.get("near_duplicate_group", ""),
            "burst_group": r.get("burst_group", ""),
            "technical_score": a.get("tech", ""), "emotional_score": a.get("emo", ""),
            "story_score": a.get("story", ""), "uniqueness_score": a.get("uniq", ""),
            "hero_score": a.get("hero", ""),
            "candidate_status": a.get("status", "NOT_REVIEWED"),
            "notes": a.get("notes", ""),
        })

    os.makedirs(OUT, exist_ok=True)
    cols = list(out[0].keys())
    with open(os.path.join(OUT, "ARCHIVE_INVENTORY.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(out)
    print(f"ARCHIVE_INVENTORY.csv: {len(out)} rows")

    reviewed = [r for r in out if r["candidate_status"] != "NOT_REVIEWED"]
    print(f"  reviewed: {len(reviewed)} | not reviewed: {len(out)-len(reviewed)}")

    def score(r):
        def g(k):
            try: return int(r[k])
            except Exception: return 0
        return (g("story_score") * 3 + g("emotional_score") * 3
                + g("uniqueness_score") * 2 + g("hero_score") * 2 + g("technical_score"))

    # ---- preliminary pool ----
    rank = {"HERO": 0, "HERO_COUPLE": 0, "STRONG_CANDIDATE": 1, "CANDIDATE": 2, "ARCHIVE": 9}
    pool = [r for r in reviewed if rank.get(r["candidate_status"], 9) <= 2]
    pool.sort(key=lambda r: (rank.get(r["candidate_status"], 9), -score(r)))
    pool = pool[:150]
    pool.sort(key=lambda r: r["unique_id"])
    pcols = ["unique_id", "filename", "drive_path", "drive_url", "estimated_date",
             "date_confidence", "era", "family_grouping", "people_visible", "event", "theme",
             "technical_score", "emotional_score", "story_score", "uniqueness_score",
             "hero_score", "candidate_status", "notes"]
    with open(os.path.join(OUT, "PRELIMINARY_PHOTO_POOL.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=pcols, extrasaction="ignore")
        w.writeheader(); w.writerows(pool)
    print(f"PRELIMINARY_PHOTO_POOL.csv: {len(pool)} rows")

    # ---- best-of collections ----
    def has(r, *words):
        blob = " ".join([r["family_grouping"], r["theme"], r["event"], r["notes"]]).lower()
        return any(w in blob for w in words)

    collections = {
        "COUPLE_BEST_OF.csv": lambda r: r["family_grouping"] == "Couple" or r["candidate_status"] == "HERO_COUPLE",
        "FAMILY_BEST_OF.csv": lambda r: r["family_grouping"].startswith("Family of"),
        "DAUGHTERS_BEST_OF.csv": lambda r: has(r, "daughter", "sister"),
        "CANDID_BEST_OF.csv": lambda r: has(r, "candid", "unposed", "everyday life", "chaos"),
        "EMOTIONAL_BEST_OF.csv": lambda r: (int(r["emotional_score"]) if str(r["emotional_score"]).isdigit() else 0) >= 8,
        "FUNNY_BEST_OF.csv": lambda r: has(r, "humor", "funny", "silly"),
        "VACATION_BEST_OF.csv": lambda r: has(r, "vacation", "beach", "resort", "trip", "adventure"),
        "EVERYDAY_LIFE_BEST_OF.csv": lambda r: has(r, "everyday life", "home"),
    }
    for fname, pred in collections.items():
        sel = [r for r in reviewed if r["candidate_status"] != "ARCHIVE" and pred(r)]
        sel.sort(key=lambda r: -score(r))
        sel = sel[:40]
        with open(os.path.join(OUT, fname), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=pcols, extrasaction="ignore")
            w.writeheader(); w.writerows(sel)
        print(f"{fname}: {len(sel)}")

    json.dump({r["unique_id"]: r for r in out}, open(os.path.join(WORK, "final_rows.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
