from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import math
import random

OUT = Path(__file__).parent / "mockups"
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1280, 720

COLORS = {
    "ink": (12, 14, 18, 236),
    "ink2": (20, 24, 32, 230),
    "panel": (28, 33, 43, 228),
    "panel2": (35, 42, 55, 238),
    "edge": (118, 147, 164, 255),
    "edge_dark": (44, 53, 64, 255),
    "gold": (226, 174, 88, 255),
    "cyan": (83, 238, 255, 255),
    "cyan_dim": (35, 159, 188, 255),
    "green": (90, 232, 142, 255),
    "red": (255, 97, 86, 255),
    "text": (238, 244, 247, 255),
    "muted": (158, 174, 184, 255),
    "black": (0, 0, 0, 255),
}

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(size, bold=False):
    path = FONT_BOLD if bold else FONT_PATH
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

F10 = font(10)
F12 = font(12)
F14 = font(14)
F16 = font(16)
F18 = font(18)
F22 = font(22, True)
F28 = font(28, True)


def rgba(color):
    return color if len(color) == 4 else (*color, 255)


def composite_rect(base, box, color):
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).rectangle(box, fill=color)
    base.alpha_composite(layer)


def draw_text(draw, xy, text, fill=COLORS["text"], fnt=F14, anchor=None):
    draw.text(xy, text, fill=fill, font=fnt, anchor=anchor)


def draw_pixel_panel(img, box, title=None, accent=COLORS["cyan"], fill=COLORS["panel"], border=6, style="steel"):
    draw = ImageDraw.Draw(img)
    x1, y1, x2, y2 = box
    # Outer 9-slice-style frame. Corners are intentionally heavier than edges.
    draw.rectangle([x1, y1, x2, y2], fill=fill, outline=COLORS["edge_dark"], width=2)
    draw.rectangle([x1+2, y1+2, x2-2, y2-2], outline=COLORS["edge"], width=1)
    draw.line([x1+border, y1+3, x2-border, y1+3], fill=(178, 206, 217, 160), width=1)
    draw.line([x1+border, y2-3, x2-border, y2-3], fill=(0, 0, 0, 140), width=1)
    # Square reinforced corners; these survive 9-slice stretching.
    for sx, sy in [(x1, y1), (x2-border, y1), (x1, y2-border), (x2-border, y2-border)]:
        draw.rectangle([sx, sy, sx+border, sy+border], fill=(18, 23, 31, 255), outline=accent, width=1)
    if title:
        tw = draw.textlength(title, font=F14)
        draw.rectangle([x1+14, y1-8, x1+24+tw, y1+12], fill=(16, 20, 27, 245), outline=accent)
        draw_text(draw, (x1+19, y1-5), title, accent, F14)


def draw_button(draw, box, label, selected=False, accent=COLORS["cyan"]):
    x1, y1, x2, y2 = box
    fill = (34, 45, 57, 240) if selected else (20, 25, 32, 230)
    edge = accent if selected else (78, 92, 105, 255)
    draw.rectangle(box, fill=fill, outline=edge, width=2 if selected else 1)
    draw.line([x1+2, y1+2, x2-2, y1+2], fill=(255,255,255,70), width=1)
    draw_text(draw, ((x1+x2)//2, y1+6), label, COLORS["text"] if selected else COLORS["muted"], F12, anchor="ma")


def draw_slider(draw, x, y, w, label, value=0.55, accent=COLORS["cyan"]):
    draw_text(draw, (x, y-15), label, COLORS["muted"], F12)
    draw.rectangle([x, y, x+w, y+8], fill=(12,15,20,255), outline=(71,84,96,255))
    fillw = int(w*value)
    draw.rectangle([x+1, y+1, x+fillw, y+7], fill=accent)
    kx = x + fillw
    draw.rectangle([kx-4, y-4, kx+4, y+12], fill=(232,244,248,255), outline=(23,30,36,255))


def draw_color_chip(draw, x, y, color, label="", selected=False):
    draw.rectangle([x, y, x+26, y+26], fill=color, outline=(245, 250, 255, 255) if selected else (48, 56, 68, 255), width=2)
    draw.rectangle([x+2, y+2, x+24, y+24], outline=(0,0,0,100))
    if label:
        draw_text(draw, (x+13, y+32), label, COLORS["muted"], F10, anchor="ma")


def draw_scene(seed=4, label="LIVE WORLD PREVIEW"):
    random.seed(seed)
    img = Image.new("RGBA", (W, H), (0,0,0,255))
    draw = ImageDraw.Draw(img)
    # Pixelated vault-like background.
    for y in range(H):
        t = y / H
        r = int(16 + 20*t)
        g = int(22 + 18*t)
        b = int(34 + 42*t)
        draw.line([0, y, W, y], fill=(r, g, b, 255))
    # Distant walls/blocks.
    for i in range(0, W, 48):
        h = random.randint(80, 210)
        col = random.choice([(36,44,58,255), (46,54,70,255), (31,38,52,255)])
        draw.rectangle([i, H-h-82, i+48, H-82], fill=col)
        draw.rectangle([i, H-h-82, i+48, H-h-76], fill=(70,84,102,255))
    # Ground grid.
    ground_y = H-110
    draw.polygon([(0, ground_y), (W, ground_y-20), (W, H), (0, H)], fill=(30,36,43,255))
    for x in range(-200, W+200, 64):
        draw.line([(x, ground_y), (x+260, H)], fill=(55,65,75,160), width=2)
    for y in range(ground_y, H, 30):
        draw.line([(0, y), (W, y-20)], fill=(49,59,69,150), width=2)
    # Player silhouette and beam.
    px, py = W//2 - 90, H//2 + 80
    target = (W//2 + 300, H//2 - 68)
    glow = Image.new("RGBA", (W, H), (0,0,0,0))
    gd = ImageDraw.Draw(glow)
    for width, alpha in [(34, 36), (22, 58), (12, 110), (5, 230)]:
        gd.line([px, py, *target], fill=(70, 235, 255, alpha), width=width)
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(4)))
    draw = ImageDraw.Draw(img)
    draw.line([px, py, *target], fill=(214, 255, 255, 255), width=3)
    draw.ellipse([target[0]-16, target[1]-16, target[0]+16, target[1]+16], outline=(120,245,255,230), width=3)
    draw.rectangle([px-14, py-40, px+14, py+34], fill=(16,18,22,255), outline=(96,115,128,255))
    draw.rectangle([px-24, py-24, px+24, py-8], fill=(19,23,30,255), outline=(96,115,128,255))
    draw_text(draw, (W//2, 28), label, (204, 230, 236, 160), F14, anchor="ma")
    return img


def add_safe_zone(draw, box, label="PREVIEW SAFE ZONE"):
    x1, y1, x2, y2 = box
    dash = 12
    col = (116, 238, 255, 135)
    for x in range(x1, x2, dash*2):
        draw.line([x, y1, min(x+dash, x2), y1], fill=col, width=2)
        draw.line([x, y2, min(x+dash, x2), y2], fill=col, width=2)
    for y in range(y1, y2, dash*2):
        draw.line([x1, y, x1, min(y+dash, y2)], fill=col, width=2)
        draw.line([x2, y, x2, min(y+dash, y2)], fill=col, width=2)
    draw_text(draw, (x1+12, y1+10), label, col, F12)


def option_a():
    img = draw_scene(1, "OPTION A - SIDE INSPECTOR")
    draw = ImageDraw.Draw(img)
    composite_rect(img, (0,0,W,H), (0,0,0,40))
    add_safe_zone(draw, (188, 84, 874, 600), "uncovered beam preview")
    # Left tab rail.
    draw_pixel_panel(img, (28, 72, 146, 632), "ABILITIES", COLORS["gold"], (20,23,30,230))
    tabs = ["Arcane", "Rail", "Strike", "Altar", "Storm", "Smite", "Archon"]
    for i, t in enumerate(tabs):
        draw_button(draw, (44, 104+i*62, 130, 142+i*62), t, selected=(i==0), accent=COLORS["gold"] if i==0 else COLORS["cyan"])
    # Right inspector.
    draw_pixel_panel(img, (912, 58, 1244, 662), "ARCANE / DEFAULT", COLORS["cyan"], (22,27,35,236))
    draw_text(draw, (936, 92), "Preview stays open; controls live on one edge.", COLORS["muted"], F12)
    y = 132
    sections = [("COLORS", COLORS["cyan"]), ("BEAM", COLORS["green"]), ("SOUND", COLORS["gold"]), ("TRANSITION", COLORS["red"])]
    for title, accent in sections:
        draw.rectangle([930, y, 1226, y+34], fill=(12,16,22,220), outline=accent)
        draw_text(draw, (944, y+9), title, accent, F14)
        y += 50
        if title == "COLORS":
            for j,c in enumerate([(78,245,255,255),(42,175,220,255),(91,99,255,255),(238,255,255,255)]):
                draw_color_chip(draw, 944+j*42, y, c, str(j+1), selected=j==0)
            y += 64
        elif title == "SOUND":
            draw_button(draw, (944, y, 1118, y+30), "Option 2 loop", True, accent)
            draw_slider(draw, 944, y+56, 250, "Volume", .42, accent)
            y += 92
        else:
            draw_slider(draw, 944, y, 250, "Intensity", .36, accent)
            draw_slider(draw, 944, y+44, 250, "Glow radius", .68, accent)
            y += 86
    # Bottom action strip.
    draw_pixel_panel(img, (210, 628, 872, 680), None, COLORS["cyan"], (18,22,30,210), border=5)
    draw_text(draw, (232, 645), "Palette opens as a popover; inspector can collapse with [I].", COLORS["muted"], F14)
    draw_button(draw, (748, 640, 846, 668), "Done", False, COLORS["cyan"])
    return img


def option_b():
    img = draw_scene(8, "OPTION B - COLLAPSIBLE BOTTOM DRAWER")
    draw = ImageDraw.Draw(img)
    add_safe_zone(draw, (108, 76, 1172, 438), "full-width preview while editing")
    # Top tabs as small pills.
    draw_pixel_panel(img, (160, 24, 1120, 74), None, COLORS["gold"], (14,18,25,210), border=5)
    labels = ["Arcane", "Rail", "Lightning", "Altar", "Storm", "Smite", "Archon"]
    x = 190
    for i, label in enumerate(labels):
        w = 94 if label not in ["Lightning"] else 118
        draw_button(draw, (x, 38, x+w, 64), label, selected=(label=="Lightning"), accent=COLORS["gold"])
        x += w + 12
    # Bottom drawer.
    draw_pixel_panel(img, (74, 470, 1206, 692), "LIGHTNING STRIKE DRAWER", COLORS["gold"], (24,29,38,240))
    draw_text(draw, (98, 500), "Drawer height can collapse to a 34px handle. Great when the effect needs the center of the screen.", COLORS["muted"], F12)
    # Drawer columns.
    colx = [104, 390, 676, 962]
    titles = ["Shape", "Flash", "Audio", "Profiles"]
    for i, cx in enumerate(colx):
        draw.rectangle([cx, 532, cx+230, 654], fill=(12,16,22,215), outline=(67,78,91,255))
        draw_text(draw, (cx+14, 544), titles[i], COLORS["gold"] if i==0 else COLORS["cyan"], F16)
    draw_slider(draw, 122, 584, 180, "End radius", .72, COLORS["gold"])
    draw_slider(draw, 122, 628, 180, "Ring thickness", .38, COLORS["gold"])
    for j,c in enumerate([(20,242,255,255),(255,255,255,255),(28,160,255,255),(198,255,147,255)]):
        draw_color_chip(draw, 408+j*44, 582, c, ["Ring","Core","Cone","Spots"][j], selected=j==0)
    draw_button(draw, (694, 580, 858, 610), "Seismic Charge", True, COLORS["cyan"])
    draw_slider(draw, 694, 640, 180, "Volume", .36, COLORS["cyan"])
    draw_button(draw, (980, 580, 1168, 610), "Profile: Main", True, COLORS["green"])
    draw_button(draw, (980, 624, 1062, 654), "Add", False, COLORS["green"])
    draw_button(draw, (1074, 624, 1168, 654), "Done", False, COLORS["green"])
    # Collapse handle.
    draw.rectangle([558, 458, 722, 482], fill=(16,20,26,255), outline=COLORS["gold"], width=2)
    draw_text(draw, (640, 463), "collapse drawer", COLORS["gold"], F12, anchor="ma")
    return img


def option_c():
    img = draw_scene(12, "OPTION C - FLOATING TOOLCARDS")
    draw = ImageDraw.Draw(img)
    composite_rect(img, (0,0,W,H), (0,0,0,18))
    add_safe_zone(draw, (246, 100, 1010, 612), "center stays unobstructed")
    # Floating tabs bottom-left.
    draw_pixel_panel(img, (32, 86, 220, 610), "STACK", COLORS["cyan"], (18,22,30,222))
    groups = [("Arcane", COLORS["cyan"]), ("Rail", COLORS["green"]), ("Lightning", COLORS["gold"]), ("Altar", (255,126,70,255)), ("Storm", (255,80,70,255)), ("Smite", (92,220,255,255)), ("Archon", (160,230,255,255))]
    for i,(label,accent) in enumerate(groups):
        draw_button(draw, (54, 124+i*56, 198, 158+i*56), label, selected=(label=="Archon"), accent=accent)
    # Floating toolcards, sparse.
    draw_pixel_panel(img, (1000, 90, 1244, 250), "COLORS", (160,230,255,255), (21,26,35,232))
    for j,c in enumerate([(217,243,255,255),(80,213,255,255),(255,255,255,255),(191,239,255,255)]):
        draw_color_chip(draw, 1024+j*50, 132, c, ["Circle","Plume","Core","Flash"][j], selected=j==1)
    draw_text(draw, (1024, 204), "Only the active edit card is open.", COLORS["muted"], F12)
    draw_pixel_panel(img, (1000, 284, 1244, 456), "MISSILE", (160,230,255,255), (21,26,35,232))
    draw_slider(draw, 1024, 332, 178, "Origin height", .62, (160,230,255,255))
    draw_slider(draw, 1024, 386, 178, "Origin radius", .78, (160,230,255,255))
    draw_pixel_panel(img, (330, 28, 950, 78), None, (160,230,255,255), (14,18,25,210), border=5)
    draw_text(draw, (354, 45), "Toolcards float at edges. Press [Tab] to cycle cards; [H] hides all chrome.", COLORS["muted"], F14)
    draw_button(draw, (814, 42, 926, 66), "Hide UI", True, (160,230,255,255))
    # Command palette lower-right.
    draw_pixel_panel(img, (838, 522, 1244, 670), "ACTIONS", (160,230,255,255), (18,22,30,225))
    draw_button(draw, (864, 560, 1012, 592), "Sound: Option 1", False, (160,230,255,255))
    draw_button(draw, (1030, 560, 1190, 592), "Profile: Default", False, (160,230,255,255))
    draw_button(draw, (864, 616, 980, 648), "Reset card", False, COLORS["red"])
    draw_button(draw, (1068, 616, 1190, 648), "Done", True, COLORS["green"])
    return img


def make_sprite(size, border, fill, accent):
    img = Image.new("RGBA", size, (0,0,0,0))
    draw = ImageDraw.Draw(img)
    w,h = size
    draw.rectangle([0,0,w-1,h-1], fill=fill, outline=(18,22,28,255), width=2)
    draw.rectangle([2,2,w-3,h-3], outline=accent, width=1)
    draw.line([border,3,w-border,3], fill=(255,255,255,80), width=1)
    draw.line([border,h-4,w-border,h-4], fill=(0,0,0,150), width=1)
    for sx, sy in [(0,0),(w-border,0),(0,h-border),(w-border,h-border)]:
        draw.rectangle([sx, sy, sx+border-1, sy+border-1], fill=(13,17,23,255), outline=accent)
    return img


def stretch_sprite(sprite, out_size, border):
    sw, sh = sprite.size
    ow, oh = out_size
    out = Image.new("RGBA", out_size, (0,0,0,0))
    # corners
    regions = [
        ((0,0,border,border),(0,0,border,border)),
        ((sw-border,0,sw,border),(ow-border,0,ow,border)),
        ((0,sh-border,border,sh),(0,oh-border,border,oh)),
        ((sw-border,sh-border,sw,sh),(ow-border,oh-border,ow,oh)),
        ((border,0,sw-border,border),(border,0,ow-border,border)),
        ((border,sh-border,sw-border,sh),(border,oh-border,ow-border,oh)),
        ((0,border,border,sh-border),(0,border,border,oh-border)),
        ((sw-border,border,sw,sh-border),(ow-border,border,ow,oh-border)),
        ((border,border,sw-border,sh-border),(border,border,ow-border,oh-border)),
    ]
    for src, dst in regions:
        part = sprite.crop(src).resize((dst[2]-dst[0], dst[3]-dst[1]), Image.Resampling.NEAREST)
        out.alpha_composite(part, (dst[0], dst[1]))
    return out


def atlas_preview():
    img = Image.new("RGBA", (1280, 720), (18,22,29,255))
    draw = ImageDraw.Draw(img)
    draw_text(draw, (34, 28), "9-slice atlas concept", COLORS["text"], F28)
    draw_text(draw, (36, 66), "Source sprites stay tiny; Java draws them stretched for panels, drawers, tabs, buttons, slots.", COLORS["muted"], F14)
    specs = [
        ("glass_panel", (32,32), 6, (25,32,43,224), COLORS["cyan"]),
        ("iron_panel", (32,32), 6, (35,39,47,242), COLORS["edge"]),
        ("gold_drawer", (32,32), 6, (36,31,26,238), COLORS["gold"]),
        ("button", (48,24), 5, (22,27,35,245), COLORS["green"]),
        ("color_slot", (22,22), 4, (10,12,16,255), COLORS["cyan"]),
    ]
    y = 116
    for name, size, border, fill, accent in specs:
        sprite = make_sprite(size, border, fill, accent)
        draw_text(draw, (38, y+8), name, COLORS["text"], F16)
        draw_text(draw, (38, y+32), f"source {size[0]}x{size[1]}, border {border}px", COLORS["muted"], F12)
        img.alpha_composite(sprite.resize((size[0]*3, size[1]*3), Image.Resampling.NEAREST), (210, y))
        draw.rectangle([210, y, 210+size[0]*3-1, y+size[1]*3-1], outline=(255,255,255,95))
        x = 360
        for ow, oh in [(132, 42), (238, 84), (380, 116)]:
            stretched = stretch_sprite(sprite, (ow, oh), border)
            img.alpha_composite(stretched, (x, y))
            draw.rectangle([x, y, x+ow-1, y+oh-1], outline=(255,255,255,55))
            draw_text(draw, (x, y+oh+8), f"{ow}x{oh}", COLORS["muted"], F10)
            x += ow + 36
        y += 116
    # UV table placeholder.
    draw_pixel_panel(img, (850, 510, 1226, 674), "REGION TABLE", COLORS["cyan"], (14,18,25,230))
    rows = [
        "glass_panel: x=0 y=0 w=32 h=32 b=6",
        "iron_panel: x=32 y=0 w=32 h=32 b=6",
        "gold_drawer: x=64 y=0 w=32 h=32 b=6",
        "button: x=0 y=32 w=48 h=24 b=5",
        "color_slot: x=48 y=32 w=22 h=22 b=4",
    ]
    for i,row in enumerate(rows):
        draw_text(draw, (872, 546+i*22), row, COLORS["muted"], F12)
    return img


def contact_sheet(images):
    thumb_w, thumb_h = 400, 225
    img = Image.new("RGBA", (1280, 930), (10,12,16,255))
    draw = ImageDraw.Draw(img)
    draw_text(draw, (32, 28), "ArcaneBeam Menu Overhaul Alternatives", COLORS["text"], F28)
    draw_text(draw, (34, 66), "All options preserve the live world preview by moving controls into 9-slice-capable surfaces.", COLORS["muted"], F14)
    positions = [(34,110), (440,110), (846,110)]
    names = ["A. Side Inspector", "B. Bottom Drawer", "C. Floating Toolcards"]
    notes = [
        "Best implementation path; predictable right-side settings stack.",
        "Maximum preview visibility; good for lightning/altar effects.",
        "Most immersive; controls open as small edge cards.",
    ]
    for (src, pos, name, note) in zip(images, positions, names, notes):
        thumb = src.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        img.alpha_composite(thumb, pos)
        draw.rectangle([pos[0], pos[1], pos[0]+thumb_w, pos[1]+thumb_h], outline=(104,128,144,255), width=2)
        draw_text(draw, (pos[0], pos[1]+thumb_h+16), name, COLORS["cyan"], F18)
        draw_text(draw, (pos[0], pos[1]+thumb_h+42), note, COLORS["muted"], F12)
    atlas = atlas_preview().resize((900, 506), Image.Resampling.LANCZOS)
    img.alpha_composite(atlas, (190, 404))
    draw.rectangle([190,404,1090,910], outline=(104,128,144,255), width=2)
    return img


def main():
    imgs = [option_a(), option_b(), option_c()]
    filenames = ["option_a_side_inspector.png", "option_b_bottom_drawer.png", "option_c_floating_toolcards.png"]
    for im, fn in zip(imgs, filenames):
        im.save(OUT / fn)
    atlas_preview().save(OUT / "nine_slice_atlas_preview.png")
    contact_sheet(imgs).save(OUT / "menu_overhaul_contact_sheet.png")
    print("Generated:")
    for fn in filenames + ["nine_slice_atlas_preview.png", "menu_overhaul_contact_sheet.png"]:
        print(OUT / fn)

if __name__ == "__main__":
    main()
