#!/usr/bin/env python3
"""Generate the Sparks app icon (PNGs).

Design: a classic four-pointed sparkle on a peach pastel background,
with two smaller sparkles in the corners. Matches the app's aesthetic
(pastel bg + dark tint of same hue as foreground).

Produces:
  - icon.png     (1024x1024 master, used as high-res apple-touch-icon)
  - icon-180.png (180x180, the size iOS actually uses for Add to Home Screen)
"""
from pathlib import Path
from PIL import Image, ImageDraw
import base64
import math
import re

OUT_DIR = Path(__file__).parent

BG = (255, 219, 194)   # #FFDBC2  peach pastel (Campaign palette)
FG = (122, 58, 26)     # #7A3A1A  deep burnt-orange (dark tint of same hue)

def sparkle_polygon(cx, cy, outer_r, inner_ratio=0.14):
    """Return polygon vertices for a 4-pointed sparkle/twinkle shape.

    A 4-pointed star drawn with alternating outer/inner radius points every 45°.
    A small inner_ratio makes the rays pointy and slim — the classic 'sparkle'.
    """
    inner_r = outer_r * inner_ratio
    pts = []
    # 8 vertices: outer at 0,90,180,270 — inner at 45,135,225,315
    for i in range(8):
        angle = math.radians(i * 45 - 90)  # start at top
        r = outer_r if i % 2 == 0 else inner_r
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    return pts

def make_icon(size: int) -> Image.Image:
    img = Image.new("RGB", (size, size), BG)
    d = ImageDraw.Draw(img)

    cx, cy = size / 2, size / 2

    # Main sparkle — centered, takes up most of the canvas
    main_r = size * 0.38
    d.polygon(sparkle_polygon(cx, cy, main_r, inner_ratio=0.12), fill=FG)

    # Small accent sparkle — upper right
    s1_cx = size * 0.78
    s1_cy = size * 0.24
    s1_r  = size * 0.11
    d.polygon(sparkle_polygon(s1_cx, s1_cy, s1_r, inner_ratio=0.14), fill=FG)

    # Even smaller accent sparkle — lower left
    s2_cx = size * 0.22
    s2_cy = size * 0.76
    s2_r  = size * 0.075
    d.polygon(sparkle_polygon(s2_cx, s2_cy, s2_r, inner_ratio=0.14), fill=FG)

    return img

def inline_into_html():
    """Re-inline icon-180.png as the apple-touch-icon data URI in sparks.html.

    sparks.html is a single self-contained file that embeds the icon as a
    base64 data URI. Without this step, regenerating the PNGs wouldn't
    change what users actually see when they "Add to Home Screen", because
    the HTML would still carry the old base64 blob.
    """
    html_path = OUT_DIR / "sparks.html"
    icon_path = OUT_DIR / "icon-180.png"
    if not html_path.exists():
        print(f"Skipped inlining: {html_path.name} not found")
        return
    new_b64 = base64.b64encode(icon_path.read_bytes()).decode("ascii")
    html = html_path.read_text(encoding="utf-8")
    pattern = re.compile(
        r'(rel="apple-touch-icon"[^>]*href="data:image/png;base64,)[^"]+(")'
    )
    new_html, n = pattern.subn(
        lambda m: m.group(1) + new_b64 + m.group(2), html, count=1
    )
    if n != 1:
        print(f"WARN: Could not find apple-touch-icon data URI in {html_path.name}; "
              f"skipped inlining.")
        return
    html_path.write_text(new_html, encoding="utf-8")
    print(f"Inlined icon-180.png into {html_path.name} "
          f"({html_path.stat().st_size:,} bytes)")

def main():
    master = make_icon(1024)
    master.save(OUT_DIR / "icon.png", "PNG", optimize=True)
    print(f"Wrote icon.png (1024x1024)")

    # Downscale with high-quality Lanczos for the precise iOS apple-touch size
    smaller = master.resize((180, 180), Image.LANCZOS)
    smaller.save(OUT_DIR / "icon-180.png", "PNG", optimize=True)
    print(f"Wrote icon-180.png (180x180)")

    inline_into_html()

if __name__ == "__main__":
    main()
