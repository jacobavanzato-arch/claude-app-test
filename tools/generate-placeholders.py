#!/usr/bin/env python3
"""
Generates the stylised placeholder artwork used across the site.

These are deliberately illustrative gradients (sunrise, sunset, lagoon, night
sky) rather than fake photography, so nothing on the site pretends to be a
photograph of the resort. Drop real photos over the top of the generated files
in assets/img/ using the same filenames and the site picks them up unchanged.

Usage:  python3 tools/generate-placeholders.py
Requires: Pillow  (pip install Pillow)
"""

import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "img")

# Deterministic output so re-running does not churn the repo.
random.seed(1979)


def hex_rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vertical_gradient(size, stops):
    """stops: list of (position 0-1, '#rrggbb')."""
    w, h = size
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    pts = [(p, hex_rgb(c)) for p, c in stops]
    for y in range(h):
        t = y / max(h - 1, 1)
        lo, hi = pts[0], pts[-1]
        for i in range(len(pts) - 1):
            if pts[i][0] <= t <= pts[i + 1][0]:
                lo, hi = pts[i], pts[i + 1]
                break
        span = max(hi[0] - lo[0], 1e-6)
        draw.line([(0, y), (w, y)], fill=lerp(lo[1], hi[1], (t - lo[0]) / span))
    return img


def glow(img, cx, cy, radius, color, strength=1.0):
    """Soft radial light, composited additively-ish over the base image."""
    w, h = img.size
    layer = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(layer)
    steps = 44
    for i in range(steps):
        t = i / steps
        r = radius * (1 - t)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=int(255 * (t ** 2.1) * strength))
    layer = layer.filter(ImageFilter.GaussianBlur(radius * 0.14))
    tint = Image.new("RGB", (w, h), hex_rgb(color))
    return Image.composite(tint, img, layer.point(lambda v: min(255, int(v * 0.95))))


def sun_disc(img, cx, cy, r, color, rim=None):
    w, h = img.size
    layer = Image.new("L", (w, h), 0)
    ImageDraw.Draw(layer).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    layer = layer.filter(ImageFilter.GaussianBlur(r * 0.05))
    img = Image.composite(Image.new("RGB", (w, h), hex_rgb(color)), img, layer)
    if rim:
        img = glow(img, cx, cy, r * 3.4, rim, 0.55)
    return img


def sea_band(img, horizon, stops, streak=None):
    w, h = img.size
    sea = vertical_gradient((w, h - horizon), stops)
    img.paste(sea, (0, horizon))
    if streak:
        cx, color = streak
        # Painted on its own layer and blurred, so the glitter path reads as
        # light on water rather than a stack of hard-edged rules.
        layer = Image.new("L", (w, h), 0)
        d = ImageDraw.Draw(layer)
        y = horizon
        while y < h:
            depth = (y - horizon) / max(h - horizon, 1)
            width = 14 + depth * 300
            value = int(210 * (1 - depth) ** 1.7 * (0.30 + 0.70 * random.random()))
            jitter = random.uniform(-26, 26) * depth
            d.line([(cx - width / 2 + jitter, y), (cx + width / 2 + jitter, y)],
                   fill=value, width=max(1, int(1 + depth * 3)))
            y += random.randint(2, 5)
        layer = layer.filter(ImageFilter.GaussianBlur(max(3.0, h * 0.010)))
        img = Image.composite(Image.new("RGB", (w, h), hex_rgb(color)), img, layer)
    return img


def island(draw, w, h, horizon, color, scale=1.0, offset=0.0, alpha=255):
    """Low island silhouette sitting on the horizon."""
    base = horizon + 4
    peak = horizon - 78 * scale
    left = w * (0.06 + offset)
    right = w * (0.62 + offset)
    pts = [(left, base)]
    span = right - left
    for i in range(41):
        t = i / 40
        x = left + span * t
        # two soft humps
        y = base - (math.sin(t * math.pi) ** 1.5) * (base - peak) \
                 - math.sin(t * math.pi * 2.4) * 14 * scale
        pts.append((x, y))
    pts.append((right, base))
    draw.polygon(pts, fill=hex_rgb(color) + (alpha,))


def _bezier(p0, p1, p2, steps):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        pts.append(((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0],
                    (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]))
    return pts


def _ribbon(draw, spine, widths, col):
    """Fill a tapered shape around a polyline — used for trunks and fronds."""
    left, right = [], []
    for i, (px, py) in enumerate(spine):
        nx, ny = (spine[min(i + 1, len(spine) - 1)][0] - spine[max(i - 1, 0)][0],
                  spine[min(i + 1, len(spine) - 1)][1] - spine[max(i - 1, 0)][1])
        mag = math.hypot(nx, ny) or 1.0
        ox, oy = -ny / mag * widths[i], nx / mag * widths[i]
        left.append((px + ox, py + oy))
        right.append((px - ox, py - oy))
    draw.polygon(left + right[::-1], fill=col)


def palm(draw, x, base_y, height, color, lean=1.0, alpha=255, fronds=8):
    """Foreground palm silhouette. base_y may sit below the frame so the trunk
    runs off the bottom edge rather than appearing to grow out of the water."""
    col = hex_rgb(color) + (alpha,)

    spine = []
    seg = 30
    for i in range(seg + 1):
        t = i / seg
        spine.append((x + math.sin(t * 1.05) * height * 0.19 * lean, base_y - height * t))
    _ribbon(draw, spine, [height * 0.034 * (1 - t / seg * 0.42) for t in range(seg + 1)], col)

    top = spine[-1]
    # Crown of fronds, arcing up then drooping over.
    for k in range(fronds):
        t_k = k / max(fronds - 1, 1)
        ang = math.pi * (0.10 + t_k * 0.80)
        length = height * random.uniform(0.30, 0.42)
        dir_x = -math.cos(ang) * lean
        tip = (top[0] + dir_x * length, top[1] - math.sin(ang) * length * 0.50 + length * 0.46)
        ctrl = (top[0] + dir_x * length * 0.48, top[1] - math.sin(ang) * length * 0.78 - length * 0.10)
        spine_f = _bezier(top, ctrl, tip, 20)
        widths = [math.sin(min(1.0, i / 20 * 1.05) * math.pi) ** 0.75 * height * 0.024 + 0.6
                  for i in range(21)]
        _ribbon(draw, spine_f, widths, col)
    # Coconut cluster tightens the crown so it doesn't read as a spider.
    r = height * 0.030
    draw.ellipse([top[0] - r, top[1] - r, top[0] + r, top[1] + r], fill=col)


def stars(img, horizon, count=220):
    w, h = img.size
    d = ImageDraw.Draw(img, "RGBA")
    for _ in range(count):
        x = random.uniform(0, w)
        y = random.uniform(0, horizon * 0.92)
        r = random.choice([0.6, 0.8, 1.0, 1.0, 1.4, 1.9])
        a = int(random.uniform(70, 235) * (1 - y / max(horizon, 1)) ** 0.35)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 249, 232, a))
    return img


def grain(img, amount=8):
    w, h = img.size
    noise = Image.effect_noise((w, h), 26).convert("L")
    return Image.blend(img, Image.merge("RGB", (noise, noise, noise)), amount / 100)


def vignette(img, strength=0.42):
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    steps = 60
    for i in range(steps):
        t = i / steps
        d.ellipse([-w * 0.30 + w * 0.62 * t, -h * 0.30 + h * 0.62 * t,
                   w * 1.30 - w * 0.62 * t, h * 1.30 - h * 0.62 * t],
                  fill=int(255 * t))
    mask = mask.filter(ImageFilter.GaussianBlur(w * 0.05))
    dark = Image.new("RGB", (w, h), (0, 0, 0))
    return Image.composite(img, Image.blend(img, dark, strength), mask)


def finish(img, path, quality=86, grain_amount=7, vig=0.40):
    img = grain(img, grain_amount)
    img = vignette(img, vig)
    img.save(os.path.join(OUT, path), quality=quality, optimize=True, progressive=True)
    print("  wrote", path, img.size)


# --------------------------------------------------------------------------
# Scenes
# --------------------------------------------------------------------------

def scene(name, size, sky, horizon_ratio, sea, sun=None, sun_color="#FFE9B0",
          glow_color="#F5B65E", glow_strength=0.7, streak=None, night=False,
          islands=(), palms=(), grain_amount=7, vig=0.40, quality=86):
    w, h = size
    horizon = int(h * horizon_ratio)
    img = vertical_gradient(size, sky)
    if night:
        img = stars(img, horizon)
    if sun:
        sx, sy, sr = sun
        img = glow(img, w * sx, horizon - h * sy, w * 0.44, glow_color, glow_strength)
        img = sun_disc(img, w * sx, horizon - h * sy, h * sr, sun_color, glow_color)
    img = sea_band(img, horizon, sea, streak)
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for spec in islands:
        island(d, w, h, horizon, **spec)
    for spec in palms:
        palm(d, **spec)
    img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
    finish(img, name, quality, grain_amount, vig)


def main():
    os.makedirs(OUT, exist_ok=True)
    print("Generating placeholder artwork into", OUT)

    # Hero — sunrise over the reef, the "sunrise" half of the brand.
    scene("hero-sunrise.jpg", (2400, 1400),
          sky=[(0.00, "#0B1430"), (0.20, "#2B2B57"), (0.42, "#7E3E60"),
               (0.58, "#CC6440"), (0.70, "#EFA95E")],
          horizon_ratio=0.66,
          sea=[(0.0, "#C0793F"), (0.16, "#6E4658"), (0.5, "#1D2E4C"), (1.0, "#0A1428")],
          sun=(0.80, 0.030, 0.062), streak=(2400 * 0.80, "#FFD79A"),
          islands=[dict(color="#0A1020", scale=1.15, offset=-0.16, alpha=245),
                   dict(color="#070C18", scale=0.72, offset=0.36, alpha=255)],
          palms=[dict(x=175, base_y=1560, height=790, color="#05080F", lean=1.0),
                 dict(x=2265, base_y=1600, height=845, color="#05080F", lean=-1.0)])

    # Portrait crop of the same scene, served to phones via <picture>. A tall
    # viewport slicing the landscape hero leaves nothing but sky.
    scene("hero-sunrise-portrait.jpg", (1200, 1700),
          sky=[(0.00, "#0B1430"), (0.26, "#2B2B57"), (0.48, "#7E3E60"),
               (0.62, "#CC6440"), (0.72, "#EFA95E")],
          horizon_ratio=0.70,
          sea=[(0.0, "#C0793F"), (0.16, "#6E4658"), (0.5, "#1D2E4C"), (1.0, "#0A1428")],
          sun=(0.62, 0.028, 0.048), streak=(1200 * 0.62, "#FFD79A"),
          islands=[dict(color="#0A1020", scale=1.0, offset=-0.10, alpha=245)],
          palms=[dict(x=95, base_y=1860, height=760, color="#05080F", lean=1.0)])

    # Sunset — the other half of the brand name.
    scene("sunset-lagoon.jpg", (1800, 1200),
          sky=[(0.00, "#160F26"), (0.20, "#452449"), (0.42, "#9A3A55"),
               (0.60, "#E0663A"), (0.72, "#F6BE72")],
          horizon_ratio=0.64,
          sea=[(0.0, "#D08A4C"), (0.18, "#7A4553"), (0.55, "#232B49"), (1.0, "#0D1224")],
          sun=(0.34, 0.020, 0.070), streak=(1800 * 0.34, "#FFD8A0"),
          islands=[dict(color="#0B0F1C", scale=0.9, offset=0.30, alpha=250)],
          palms=[dict(x=1690, base_y=1370, height=700, color="#06090F", lean=-1.0)])

    # Daytime lagoon / reef.
    scene("lagoon-reef.jpg", (1800, 1200),
          sky=[(0.00, "#1D6E9E"), (0.30, "#57A8C8"), (0.55, "#A6D8E2")],
          horizon_ratio=0.42,
          sea=[(0.0, "#7FD6DC"), (0.28, "#3FA9C4"), (0.62, "#1C7A9E"), (1.0, "#0E4E70")],
          glow_color="#DFF6FA", grain_amount=6, vig=0.30,
          islands=[dict(color="#12463F", scale=0.85, offset=0.24, alpha=235)])

    # Night — village celebration, kava and music under the stars.
    scene("night-village.jpg", (1800, 1200),
          sky=[(0.00, "#03060E"), (0.35, "#081226"), (0.62, "#12233F")],
          horizon_ratio=0.62,
          sea=[(0.0, "#16304C"), (0.4, "#0A1A2E"), (1.0, "#050A14")],
          sun=(0.76, 0.16, 0.030), sun_color="#F3EBD2", glow_color="#7FA8C8",
          glow_strength=0.32, night=True, streak=(1800 * 0.76, "#9FC4DC"),
          islands=[dict(color="#02040A", scale=1.0, offset=-0.22, alpha=255)],
          palms=[dict(x=205, base_y=1345, height=665, color="#010306", lean=1.0),
                 dict(x=1650, base_y=1375, height=615, color="#010306", lean=-0.9)])

    # Aerial-ish: pale sand, turquoise shallows, deep drop-off.
    scene("island-aerial.jpg", (1800, 1200),
          sky=[(0.00, "#0E5A7C"), (0.18, "#1E88A6")],
          horizon_ratio=0.20,
          sea=[(0.00, "#63C9D6"), (0.20, "#9FE2E4"), (0.34, "#EFE2C4"),
               (0.46, "#8FDCE0"), (0.70, "#2C93B4"), (1.0, "#0B4568")],
          grain_amount=6, vig=0.26)

    # Retreat / gathering — warm dusk, lantern light.
    scene("retreat-dusk.jpg", (1800, 1200),
          sky=[(0.00, "#1A1226"), (0.26, "#4A2740"), (0.50, "#8E4442"),
               (0.66, "#D07A45"), (0.76, "#EFC383")],
          horizon_ratio=0.70,
          sea=[(0.0, "#B9834E"), (0.3, "#4E3A48"), (1.0, "#140F1E")],
          sun=(0.50, 0.012, 0.048), streak=(1800 * 0.50, "#FFDDA8"),
          palms=[dict(x=140, base_y=1360, height=720, color="#080609", lean=1.0),
                 dict(x=1725, base_y=1370, height=675, color="#080609", lean=-1.0)])

    # Open-water crossing to the island.
    scene("crossing.jpg", (1800, 1200),
          sky=[(0.00, "#2E7FA6"), (0.28, "#6FB3CA"), (0.50, "#C3E1E8")],
          horizon_ratio=0.48,
          sea=[(0.0, "#3E9DBC"), (0.35, "#1F7599"), (1.0, "#0A3E5E")],
          streak=(1800 * 0.5, "#CFEAF2"), grain_amount=6, vig=0.32,
          islands=[dict(color="#123F44", scale=0.55, offset=0.32, alpha=200)])

    # Social / Open Graph card.
    scene("og-card.jpg", (1200, 630),
          sky=[(0.00, "#0B1430"), (0.24, "#33305E"), (0.46, "#8A4360"),
               (0.62, "#CC6440"), (0.74, "#EFA95E")],
          horizon_ratio=0.68,
          sea=[(0.0, "#C0793F"), (0.2, "#6E4658"), (0.6, "#1D2E4C"), (1.0, "#0A1428")],
          sun=(0.62, 0.030, 0.075), streak=(1200 * 0.62, "#FFD79A"),
          islands=[dict(color="#0A1020", scale=0.8, offset=-0.14, alpha=245)],
          palms=[dict(x=90, base_y=720, height=400, color="#05080F", lean=1.0)])

    print("Done.")


if __name__ == "__main__":
    main()
