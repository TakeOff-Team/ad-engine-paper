#!/usr/bin/env python3
"""
contact-sheet.py — one image showing every file in a folder, numbered, for picking references.

Usage (from project root):
  python3 .claude/skills/paper-ads/contact-sheet.py FOLDER [--cols 5] [--out contact-sheet.png]

Writes contact-sheet.png and index.md (number -> file) into FOLDER. Free, no network.
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps

EXT = {".png", ".jpg", ".jpeg", ".webp"}


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    folder = Path(sys.argv[1])
    cols = int(sys.argv[sys.argv.index("--cols") + 1]) if "--cols" in sys.argv else 5
    out_name = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "contact-sheet.png"
    files = sorted(p for p in folder.rglob("*") if p.suffix.lower() in EXT and p.name != out_name)
    if not files:
        sys.exit(f"No images found under {folder}")
    cw, ch, pad, label = 320, 400, 16, 28
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (cw + pad) + pad, rows * (ch + label + pad) + pad), "#FFFFFF")
    draw = ImageDraw.Draw(sheet); lines = ["# Contact sheet", ""]
    for i, f in enumerate(files):
        try:
            im = Image.open(f).convert("RGB")
        except Exception:
            continue
        thumb = ImageOps.contain(im, (cw, ch))
        x = pad + (i % cols) * (cw + pad); y = pad + (i // cols) * (ch + label + pad)
        sheet.paste(thumb, (x + (cw - thumb.size[0]) // 2, y + label))
        draw.text((x, y + 6), f"{i + 1:02d}  {f.name[:36]}", fill="#111111")
        lines.append(f"{i + 1:02d}. `{f.relative_to(folder)}`")
    sheet.save(folder / out_name)
    (folder / "index.md").write_text("\n".join(lines) + "\n")
    print(f"  ✓ {out_name} ({len(files)} images) and index.md")


if __name__ == "__main__":
    main()
