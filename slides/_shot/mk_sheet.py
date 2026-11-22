"""Stitch the 19 rendered frames into _shot/contact_sheet.png.

Reads _shot/frames/b00.png … b18.png (written by mk_sheet.sh), scales each to
half size, labels it with the 1-based page number and the beat index, and lays
them out two per row.
"""
import os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
FR = os.path.join(HERE, "frames")
OUT = os.path.join(HERE, "contact_sheet.png")

W, H = 800, 450                      # each tile
COLS, GAP, PAD, BAR = 2, 12, 14, 26


def main():
    frames = sorted(f for f in os.listdir(FR) if f.startswith("b") and f.endswith(".png"))
    if not frames:
        raise SystemExit("no frames in " + FR)
    rows = (len(frames) + COLS - 1) // COLS
    sheet = Image.new("RGB", (PAD * 2 + COLS * W + (COLS - 1) * GAP,
                              PAD * 2 + rows * (H + BAR) + (rows - 1) * GAP), (14, 18, 26))
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(frames):
        im = Image.open(os.path.join(FR, f)).convert("RGB").resize((W, H), Image.LANCZOS)
        r, c = divmod(i, COLS)
        x = PAD + c * (W + GAP)
        y = PAD + r * (H + BAR + GAP)
        sheet.paste(im, (x, y))
        d.text((x + 6, y + H + 6), "page %02d  ·  beat %d" % (i + 1, i), fill=(150, 168, 190))
    sheet.save(OUT)
    print("wrote", OUT, sheet.size)


if __name__ == "__main__":
    main()
