#!/usr/bin/env python3
"""Merge factual metadata + visual annotations into ARCHIVE_INVENTORY.csv.

Visual fields (people, event, theme, scores) come from work/annotations.json,
which is written from actual visual review of contact sheets. Any photo not yet
reviewed is emitted with UNKNOWN rather than a guess.
"""
import json, os, csv

SP = "/tmp/claude-0/-home-user-OpenFIN/2e259a81-ccde-53fc-8059-70cd5c69f215/scratchpad"
WORK = os.path.join(SP, "work")
OUT = "/home/user/15_YEARS_OF_US"

FOLDER_NAMES = {
    "1EPwabfad6nXw1I3DmHBhHso45_92LVnb": "01- DIGITAL PHOTOS 2013-2026",
    "1Usv9KcgoM-zQfzFL32a93cls33MkJbF2": "02 - OLD PHOTOS 2003-2013",
}

COLUMNS = ["unique_id", "filename", "drive_path", "drive_url", "file_type", "width", "height",
           "file_size_bytes", "exif_date", "estimated_date", "date_confidence", "date_source",
           "source_folder", "people_visible", "people_count", "family_grouping", "location",
           "location_confidence", "event", "era", "theme", "technical_quality",
           "duplicate_group", "near_duplicate_group", "burst_group", "technical_score",
           "emotional_score", "story_score", "uniqueness_score", "hero_score",
           "candidate_status", "notes"]


def tech_quality(r):
    """Coarse technical band from measured pixel stats — not a judgement of worth."""
    if r.get("error"):
        return "UNREADABLE"
    s, b, mp = r.get("sharpness") or 0, r.get("brightness") or 0, r.get("megapixels") or 0
    flags = []
    if s < 80:
        flags.append("soft")
    if b < 55:
        flags.append("dark")
    if b > 205:
        flags.append("blown")
    if mp < 0.5:
        flags.append("low-res")
    if not flags:
        return "GOOD"
    return "USABLE (" + ",".join(flags) + ")"


def main():
    rows = json.load(open(os.path.join(WORK, "clustered.json")))
    drive = {}
    for src in ("drive_meta.json",):
        p = os.path.join(WORK, src)
        if os.path.exists(p):
            for d in json.load(open(p)):
                drive[d["id"]] = d
    # folder-02 listing carries no parentId, so stamp it explicitly
    p2 = os.path.join(WORK, "folder02_meta.json")
    if os.path.exists(p2):
        try:
            j = json.load(open(p2))
            for d in (j.get("files") if isinstance(j, dict) else j):
                d.setdefault("parentId", "1Usv9KcgoM-zQfzFL32a93cls33MkJbF2")
                d.setdefault("viewUrl", f"https://drive.google.com/file/d/{d['id']}/view")
                drive[d["id"]] = d
        except Exception:
            pass

    ann = {}
    pa = os.path.join(WORK, "annotations.json")
    if os.path.exists(pa):
        ann = json.load(open(pa))

    rows.sort(key=lambda r: (r.get("est_datetime") or "9999", r.get("filename") or ""))

    out_rows = []
    for i, r in enumerate(rows, 1):
        fid = r["file_id"]
        d = drive.get(fid, {})
        a = ann.get(fid, {})
        parent = d.get("parentId", "")
        folder = FOLDER_NAMES.get(parent, "UNKNOWN")
        out_rows.append({
            "unique_id": f"P{i:03d}",
            "filename": d.get("title") or r.get("filename"),
            "drive_path": f"15 YEARS OF US/{folder}",
            "drive_url": d.get("viewUrl", ""),
            "file_type": d.get("mimeType", "image/jpeg"),
            "width": r.get("width", ""),
            "height": r.get("height", ""),
            "file_size_bytes": r.get("bytes", ""),
            "exif_date": r.get("datetime_original") or "",
            "estimated_date": r.get("est_date") or "UNKNOWN",
            "date_confidence": r.get("date_confidence", "UNKNOWN"),
            "date_source": r.get("date_source", ""),
            "source_folder": folder,
            "people_visible": a.get("people", "UNKNOWN"),
            "people_count": a.get("people_count", "UNKNOWN"),
            "family_grouping": a.get("grouping", "UNKNOWN"),
            "location": a.get("location", "UNKNOWN"),
            "location_confidence": a.get("location_conf", "UNKNOWN"),
            "event": a.get("event", "UNKNOWN"),
            "era": r.get("era", "UNKNOWN"),
            "theme": a.get("theme", "UNKNOWN"),
            "technical_quality": tech_quality(r),
            "duplicate_group": r.get("duplicate_group", ""),
            "near_duplicate_group": r.get("near_duplicate_group", ""),
            "burst_group": r.get("burst_group", ""),
            "technical_score": a.get("tech", ""),
            "emotional_score": a.get("emo", ""),
            "story_score": a.get("story", ""),
            "uniqueness_score": a.get("uniq", ""),
            "hero_score": a.get("hero", ""),
            "candidate_status": a.get("status", "NOT_REVIEWED"),
            "notes": a.get("notes", ""),
        })

    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "ARCHIVE_INVENTORY.csv")
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(out_rows)
    print(f"wrote {path}: {len(out_rows)} rows")

    # id map for annotation work
    with open(os.path.join(WORK, "idmap.tsv"), "w") as f:
        for o, r in zip(out_rows, rows):
            f.write(f"{o['unique_id']}\t{r['file_id']}\t{r['path']}\t{o['estimated_date']}\t{o['filename']}\n")


if __name__ == "__main__":
    main()
