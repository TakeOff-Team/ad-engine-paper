#!/usr/bin/env python3
"""
product-bbox.py — find where the product (or any subject) sits in a plate, and record it.

Usage (from project root):
  python3 .claude/skills/paper-ads/product-bbox.py <concept-folder> --variant feed_4x5 [--plate path] [--bbox x0,y0,x1,y1] [--tolerance 28]

Auto mode: compares every pixel to the plate's background colour (sampled from the
four corners) and takes the bounding box of everything that differs by more than
--tolerance. Works on studio plates with a plain ground. On a busy scene, pass the
box yourself with --bbox after measuring it in Paper or an image viewer.

Writes variants.<variant>.product_bbox = [x0, y0, x1, y1] (pixels, delivery size)
into spec.json, and prints whether the box sits inside the product stage and clear
of the 9:16 platform rail. preflight.js reads the same field and fails any text
layer that overlaps it. Free, no network.
"""
import json, sys
from pathlib import Path
from PIL import Image

STAGE = {"fullscreen_9x16": (120, 430, 810, 1350)}
RAIL = {"fullscreen_9x16": (840, 560, 1080, 1500)}


def _arg(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


def _latest(out: Path, stem: str):
    c = sorted(out.glob(f"{stem}_v*.png"), key=lambda p: int(p.stem.rsplit("_v", 1)[1]))
    return c[-1] if c else None


def auto_bbox(im: Image.Image, tol: int):
    im = im.convert("RGB"); w, h = im.size; px = im.load()
    corners = [px[2, 2], px[w - 3, 2], px[2, h - 3], px[w - 3, h - 3]]
    bg = tuple(sum(c[i] for c in corners) // 4 for i in range(3))
    spread = max(max(abs(c[i] - bg[i]) for i in range(3)) for c in corners)
    if spread > tol:
        return None, bg, spread
    x0, y0, x1, y1 = w, h, -1, -1
    step = 2
    for y in range(0, h, step):
        for x in range(0, w, step):
            r, g, b = px[x, y]
            if abs(r - bg[0]) + abs(g - bg[1]) + abs(b - bg[2]) > tol * 3:
                if x < x0: x0 = x
                if x > x1: x1 = x
                if y < y0: y0 = y
                if y > y1: y1 = y
    if x1 < 0:
        return None, bg, spread
    return (x0, y0, x1 + step, y1 + step), bg, spread


def main():
    if len(sys.argv) < 2 or "--variant" not in sys.argv:
        sys.exit(__doc__)
    out = Path(sys.argv[1]); variant = _arg("--variant")
    spec = json.loads((out / "spec.json").read_text()); name = spec.get("output_name", out.name)
    vspec = spec.setdefault("variants", {}).setdefault(variant, {})
    plate = Path(_arg("--plate")) if _arg("--plate") else _latest(out, f"{name}-{variant}-plate")
    if not plate or not plate.exists():
        sys.exit("Error: no plate found for this variant. Run the plate step first, or pass --plate.")
    im = Image.open(plate); w, h = im.size
    if _arg("--bbox"):
        bbox = tuple(int(v) for v in _arg("--bbox").split(",")); how = "given"
    else:
        tol = int(_arg("--tolerance", 28))
        bbox, bg, spread = auto_bbox(im, tol)
        how = "auto"
        if bbox is None:
            sys.exit(f"Could not separate the subject from the background (corner colours differ by {spread}). "
                     "Measure the product box in Paper or an image viewer and pass --bbox x0,y0,x1,y1.")
        if (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) > 0.6 * w * h:
            sys.exit(f"Auto detection found a box covering most of the frame (x{bbox[0]}–{bbox[2]}, y{bbox[1]}–{bbox[3]}): "
                     "this is a scene, not a product on a plain ground. Measure the product itself and pass --bbox x0,y0,x1,y1.")
    vspec["product_bbox"] = list(bbox); vspec["product_bbox_source"] = how; vspec["product_bbox_plate"] = plate.name
    (out / "spec.json").write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
    print(f"  product box ({how}): x{bbox[0]}–{bbox[2]}, y{bbox[1]}–{bbox[3]} of {w}x{h}")
    if variant in STAGE:
        sx0, sy0, sx1, sy1 = STAGE[variant]; rx0, ry0, rx1, ry1 = RAIL[variant]
        inside = bbox[0] >= sx0 and bbox[1] >= sy0 and bbox[2] <= sx1 and bbox[3] <= sy1
        in_rail = bbox[2] > rx0 and bbox[3] > ry0 and bbox[1] < ry1
        print(f"  product stage x{sx0}–{sx1}, y{sy0}–{sy1}: {'inside' if inside else 'OUTSIDE'}")
        print(f"  platform rail: {'CLEAR' if not in_rail else 'ENTERED by ' + str(bbox[2] - rx0) + 'px'}")
        if not inside or in_rail:
            print("  ! this plate cannot ship as a 9:16. Derive it from the 4:5 with extend-plate.py, or re-render.")
            sys.exit(1)


if __name__ == "__main__":
    main()
