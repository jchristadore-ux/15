#!/usr/bin/env python3
"""Build labeled contact sheets so many photos can be reviewed visually at once.

Each cell is captioned with its short ID (e.g. P042) so visual findings can be
tied back to exact files. Usage: contactsheet.py <order.tsv> <outdir> [cols] [rows]
order.tsv lines: shortid<TAB>path<TAB>caption
"""
import sys, os, math
from PIL import Image, ImageDraw, ImageFont

CELL = 380
PAD = 8
BAR = 26
BG = (18, 18, 20)
FG = (245, 245, 245)


def font(sz=17):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, sz)
            except Exception:
                pass
    return ImageFont.load_default()


def main():
    order, outdir = sys.argv[1], sys.argv[2]
    cols = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    rows = int(sys.argv[4]) if len(sys.argv) > 4 else 3
    per = cols * rows
    os.makedirs(outdir, exist_ok=True)
    f = font()

    items = []
    for line in open(order):
        line = line.rstrip("\n")
        if not line:
            continue
        parts = line.split("\t")
        items.append((parts[0], parts[1], parts[2] if len(parts) > 2 else ""))

    sheets = 0
    for s in range(0, len(items), per):
        chunk = items[s:s + per]
        W = cols * CELL + (cols + 1) * PAD
        H = rows * (CELL + BAR) + (rows + 1) * PAD
        sheet = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(sheet)
        for i, (sid, path, cap) in enumerate(chunk):
            r, c = divmod(i, cols)
            x = PAD + c * (CELL + PAD)
            y = PAD + r * (CELL + BAR + PAD)
            try:
                im = Image.open(path).convert("RGB")
                im.thumbnail((CELL, CELL))
                ox = x + (CELL - im.size[0]) // 2
                oy = y + (CELL - im.size[1]) // 2
                sheet.paste(im, (ox, oy))
            except Exception:
                d.rectangle([x, y, x + CELL, y + CELL], outline=(120, 40, 40), width=2)
                d.text((x + 8, y + 8), "UNREADABLE", fill=(220, 120, 120), font=f)
            label = f"{sid}  {cap}"[:46]
            d.text((x + 2, y + CELL + 5), label, fill=FG, font=f)
        out = os.path.join(outdir, f"sheet_{sheets:02d}.jpg")
        sheet.save(out, quality=88)
        sheets += 1
    print(f"sheets written: {sheets} -> {outdir}")


if __name__ == "__main__":
    main()
