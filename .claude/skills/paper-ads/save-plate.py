#!/usr/bin/env python3
"""
save-plate.py — file a plate made outside fal (Higgsfield, or a photo the brand already owns).

Usage (from project root):
  python3 .claude/skills/paper-ads/save-plate.py OUTPUT_DIR --variant feed_4x5 --source <url-or-local-path> [--no-desaturate] [--keep-size]

Downloads or copies the source, centre-crops it to the variant's ratio when the model
could not return that ratio natively, resizes to delivery size (1080 wide), applies the
house 10% desaturation, and writes
[output-name]-[variant]-plate_vN.png next to spec.json. Free: no image model is called.
"""
import io, json, os, sys
from pathlib import Path
try:
    import requests
    from PIL import Image, ImageEnhance
except ImportError as exc:
    sys.exit(f"Error: missing dependency '{exc.name}'. pip install -r requirements.txt")

RATIOS = {"feed_4x5": (4, 5), "fullscreen_9x16": (9, 16), "square_1x1": (1, 1)}
DELIVERY = {"feed_4x5": (1080, 1350), "fullscreen_9x16": (1080, 1920), "square_1x1": (1080, 1080)}


def _next(out: Path, stem: str) -> Path:
    n = 1
    while (out / f"{stem}_v{n}.png").exists():
        n += 1
    return out / f"{stem}_v{n}.png"


def _arg(flag):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else None


def main():
    if len(sys.argv) < 2 or "--source" not in sys.argv or "--variant" not in sys.argv:
        sys.exit(__doc__)
    out = Path(sys.argv[1]); spec = json.loads((out / "spec.json").read_text())
    variant, source = _arg("--variant"), _arg("--source")
    vspec = spec.get("variants", {}).get(variant)
    if vspec is None:
        sys.exit(f"Error: variant '{variant}' is not declared in spec.json variants.")
    ratio = vspec.get("aspect_ratio")
    rw, rh = (int(x) for x in ratio.split(":")) if ratio else RATIOS.get(variant, (4, 5))
    if source.startswith(("http://", "https://")):
        raw = requests.get(source, timeout=120).content
    else:
        if not Path(source).exists():
            sys.exit(f"Error: source not found: {source}")
        raw = Path(source).read_bytes()
    im = Image.open(io.BytesIO(raw)).convert("RGB"); w, h = im.size
    target = rw / rh; actual = w / h
    if abs(actual - target) / target > 0.01:
        if actual > target:
            nw = round(h * target); x0 = (w - nw) // 2; box = (x0, 0, x0 + nw, h)
        else:
            nh = round(w / target); y0 = (h - nh) // 2; box = (0, y0, w, y0 + nh)
        lost = 1 - ((box[2] - box[0]) * (box[3] - box[1])) / (w * h)
        im = im.crop(box)
        print(f"  cropped {w}x{h} to {im.size[0]}x{im.size[1]} for {rw}:{rh} ({lost:.1%} of the frame removed, centred)")
        if lost > 0.12:
            print("  ! more than 12% removed: check the product and the copy space survived, or re-render at a closer ratio")
    # Delivery size: the type floors and safe zones are defined at 1080px wide, so the
    # plate is normalised to it. --keep-size leaves a larger source untouched.
    if "--keep-size" not in sys.argv and variant in DELIVERY and im.size != DELIVERY[variant]:
        before = im.size
        im = im.resize(DELIVERY[variant], Image.Resampling.LANCZOS)
        print(f"  resized {before[0]}x{before[1]} to {im.size[0]}x{im.size[1]} (delivery size)")
        if before[0] < DELIVERY[variant][0] * 0.9:
            print("  ! source is smaller than delivery size: it was upscaled. Request a higher resolution next time")
    if "--no-desaturate" not in sys.argv:
        im = ImageEnhance.Color(im).enhance(0.9)
    name = spec.get("output_name", out.name)
    dest = _next(out, f"{name}-{variant}-plate")
    im.save(dest)
    note = "" if "--no-desaturate" in sys.argv else " (90% saturation)"
    print(f"  ✓ {dest.name} {im.size[0]}x{im.size[1]}{note}")


if __name__ == "__main__":
    main()
