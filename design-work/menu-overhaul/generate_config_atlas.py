#!/usr/bin/env python3
"""Generate the in-mod ArcaneBeam config GUI atlas.

The Java region constants in NineSliceRenderer mirror the table below.
"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "src/main/resources/assets/arcanebeam/textures/gui/config_atlas.png"

ATLAS_SIZE = (256, 256)
REGIONS = {
    "glass_panel": (0, 0, 32, 32, 8),
    "iron_panel": (32, 0, 32, 32, 8),
    "gold_drawer": (64, 0, 32, 32, 8),
    "button": (96, 0, 24, 24, 6),
    "button_active": (120, 0, 24, 24, 6),
    "color_slot": (144, 0, 20, 20, 4),
    "inset": (164, 0, 24, 24, 6),
}

PALETTES = {
    "glass_panel": {
        "outer": (242, 198, 111, 210),
        "edge": (99, 157, 196, 185),
        "inner": (12, 21, 31, 188),
        "shine": (255, 236, 177, 82),
    },
    "iron_panel": {
        "outer": (109, 127, 146, 218),
        "edge": (53, 75, 96, 205),
        "inner": (17, 24, 33, 222),
        "shine": (197, 229, 239, 70),
    },
    "gold_drawer": {
        "outer": (239, 184, 83, 235),
        "edge": (119, 77, 31, 225),
        "inner": (29, 24, 21, 230),
        "shine": (255, 236, 167, 92),
    },
    "button": {
        "outer": (121, 151, 172, 225),
        "edge": (42, 57, 76, 220),
        "inner": (26, 37, 49, 230),
        "shine": (183, 226, 235, 66),
    },
    "button_active": {
        "outer": (248, 190, 89, 242),
        "edge": (95, 63, 25, 228),
        "inner": (46, 35, 24, 235),
        "shine": (255, 240, 170, 118),
    },
    "color_slot": {
        "outer": (239, 184, 83, 245),
        "edge": (68, 91, 112, 230),
        "inner": (7, 10, 16, 235),
        "shine": (255, 250, 216, 90),
    },
    "inset": {
        "outer": (56, 80, 100, 210),
        "edge": (12, 18, 27, 235),
        "inner": (5, 8, 13, 225),
        "shine": (97, 175, 206, 48),
    },
}


def draw_region(draw: ImageDraw.ImageDraw, region_name: str):
    x, y, w, h, border = REGIONS[region_name]
    p = PALETTES[region_name]
    draw.rectangle((x, y, x + w - 1, y + h - 1), fill=p["inner"])
    draw.rectangle((x, y, x + w - 1, y + h - 1), outline=p["outer"])
    draw.rectangle((x + 1, y + 1, x + w - 2, y + h - 2), outline=p["edge"])
    draw.line((x + border, y + 2, x + w - border - 1, y + 2), fill=p["shine"])
    draw.line((x + 2, y + border, x + 2, y + h - border - 1), fill=p["shine"])
    # Corner cuts make the atlas feel arcane sci-fi without copying any franchise UI.
    cut = max(2, border // 2)
    shadow = (0, 0, 0, 0)
    for coords in [
        (x, y, x + cut - 1, y),
        (x, y, x, y + cut - 1),
        (x + w - cut, y, x + w - 1, y),
        (x + w - 1, y, x + w - 1, y + cut - 1),
        (x, y + h - 1, x + cut - 1, y + h - 1),
        (x, y + h - cut, x, y + h - 1),
        (x + w - cut, y + h - 1, x + w - 1, y + h - 1),
        (x + w - 1, y + h - cut, x + w - 1, y + h - 1),
    ]:
        draw.line(coords, fill=shadow)
    # Small gold nodes for the hybrid theme.
    node = (246, 195, 91, 215)
    for px, py in [(x + 4, y + 4), (x + w - 5, y + 4), (x + 4, y + h - 5), (x + w - 5, y + h - 5)]:
        draw.point((px, py), fill=node)


def main():
    image = Image.new("RGBA", ATLAS_SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    for name in REGIONS:
        draw_region(draw, name)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUT)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
