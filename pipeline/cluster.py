#!/usr/bin/env python3
"""Duplicate / near-duplicate / burst grouping + chronology scaffolding.

Reads work/base_metadata.json, writes work/clustered.json.
Everything here is derived from file bytes, pixels, or EXIF — never guessed.
"""
import json, os, hashlib, datetime, itertools
import imagehash

SP = "/tmp/claude-0/-home-user-OpenFIN/2e259a81-ccde-53fc-8059-70cd5c69f215/scratchpad"
WORK = os.path.join(SP, "work")

NEAR_THRESHOLD = 10   # hamming distance on 64-bit phash
BURST_SECONDS = 90

ERAS = [
    ("2003-2006 BEFORE WE WERE MARRIED", 2003, 2006),
    ("2006-2010 WEDDING / EARLY MARRIAGE", 2006, 2010),
    ("2010-2013 EARLY FAMILY", 2010, 2013),
    ("2013-2016 FAMILY GROWING", 2013, 2016),
    ("2016-2020 FAMILY OF FIVE", 2016, 2020),
    ("2020-2023 THE CHAOS YEARS", 2020, 2023),
    ("2023-2026 TODAY", 2023, 2026),
]


def era_for(year):
    if not year:
        return "UNKNOWN"
    for name, lo, hi in ERAS:
        if lo <= year < hi:
            return name
    if year >= 2026:
        return "2023-2026 TODAY"
    if year < 2003:
        return f"PRE-2003 ({year})"
    return "UNKNOWN"


def parse_dt(s):
    if not s:
        return None
    for fmt in ("%Y:%m:%d %H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.datetime.strptime(s.strip(), fmt)
        except Exception:
            pass
    return None


class DSU:
    def __init__(self):
        self.p = {}

    def find(self, x):
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra


def main():
    rows = json.load(open(os.path.join(WORK, "base_metadata.json")))

    # md5 of raw bytes -> exact duplicates
    for r in rows:
        try:
            r["md5"] = hashlib.md5(open(r["path"], "rb").read()).hexdigest()
        except Exception:
            r["md5"] = None

    # dates
    for r in rows:
        # Scans of physical prints carry the SCAN time in EXIF, not the capture
        # time. Trusting it would file 2003-2013 prints under "TODAY".
        soft = (r.get("software") or "")
        r["is_scan"] = "photoscan" in soft.lower() or "scan" in soft.lower()
        if r["is_scan"]:
            r["scan_datetime"] = r.get("datetime_original") or ""
            r["est_date"] = ""
            r["est_datetime"] = ""
            r["year"] = None
            r["date_confidence"] = "UNKNOWN"
            r["date_source"] = f"scan artifact ({soft}) - EXIF is scan date, needs visual dating"
            r["era"] = "UNKNOWN (scanned print - date TBD)"
            continue
        dt = parse_dt(r.get("datetime_original")) or parse_dt(r.get("exif_datetime"))
        if dt:
            r["est_date"] = dt.strftime("%Y-%m-%d")
            r["est_datetime"] = dt.strftime("%Y-%m-%d %H:%M:%S")
            r["year"] = dt.year
            r["date_confidence"] = "HIGH"
            r["date_source"] = "EXIF DateTimeOriginal" if r.get("datetime_original") else "EXIF DateTime"
        else:
            r["est_date"] = ""
            r["est_datetime"] = ""
            r["year"] = None
            r["date_confidence"] = "UNKNOWN"
            r["date_source"] = "none (EXIF stripped)"
        r["era"] = era_for(r.get("year"))

    # exact duplicate groups (identical bytes)
    bymd5 = {}
    for r in rows:
        bymd5.setdefault(r["md5"], []).append(r["file_id"])
    exact = {k: v for k, v in bymd5.items() if k and len(v) > 1}
    exact_map = {}
    for i, (k, ids) in enumerate(sorted(exact.items()), 1):
        for fid in ids:
            exact_map[fid] = f"EXACT_{i:02d}"

    # near-duplicate groups via phash hamming distance
    hs = [(r["file_id"], imagehash.hex_to_hash(r["phash"])) for r in rows if r.get("phash")]
    dsu = DSU()
    for fid, _ in hs:
        dsu.find(fid)
    for (a, ha), (b, hb) in itertools.combinations(hs, 2):
        if (ha - hb) <= NEAR_THRESHOLD:
            dsu.union(a, b)
    groups = {}
    for fid, _ in hs:
        groups.setdefault(dsu.find(fid), []).append(fid)
    near_map = {}
    gi = 0
    for root, members in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        if len(members) > 1:
            gi += 1
            for fid in members:
                near_map[fid] = f"NEAR_{gi:02d}"

    # bursts: near-dup members shot within BURST_SECONDS of each other
    byid = {r["file_id"]: r for r in rows}
    burst_map = {}
    bi = 0
    for root, members in groups.items():
        if len(members) < 2:
            continue
        timed = sorted([m for m in members if byid[m].get("est_datetime")],
                       key=lambda m: byid[m]["est_datetime"])
        run = []
        for m in timed:
            if not run:
                run = [m]
                continue
            prev = parse_dt(byid[run[-1]]["est_datetime"])
            cur = parse_dt(byid[m]["est_datetime"])
            if prev and cur and abs((cur - prev).total_seconds()) <= BURST_SECONDS:
                run.append(m)
            else:
                if len(run) > 1:
                    bi += 1
                    for x in run:
                        burst_map[x] = f"BURST_{bi:02d}"
                run = [m]
        if len(run) > 1:
            bi += 1
            for x in run:
                burst_map[x] = f"BURST_{bi:02d}"

    for r in rows:
        r["duplicate_group"] = exact_map.get(r["file_id"], "")
        r["near_duplicate_group"] = near_map.get(r["file_id"], "")
        r["burst_group"] = burst_map.get(r["file_id"], "")

    json.dump(rows, open(os.path.join(WORK, "clustered.json"), "w"), indent=1)

    dated = [r for r in rows if r.get("year")]
    print(f"total: {len(rows)}")
    print(f"exact duplicate groups: {len(exact)} covering {len(exact_map)} files")
    print(f"near-duplicate groups: {gi} covering {len(near_map)} files")
    print(f"burst groups: {bi} covering {len(burst_map)} files")
    print(f"dated (EXIF): {len(dated)} | undated: {len(rows)-len(dated)}")
    if dated:
        yrs = sorted(r["year"] for r in dated)
        print(f"date range: {yrs[0]} - {yrs[-1]}")
        from collections import Counter
        for era, n in sorted(Counter(r["era"] for r in rows).items()):
            print(f"   {era}: {n}")


if __name__ == "__main__":
    main()
