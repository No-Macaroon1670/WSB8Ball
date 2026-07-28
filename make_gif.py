"""Render a looping demo GIF of the WSB Magic 8-Ball, mimicking the site's
shake/blur/reveal animation. Uses the real blacked-out background and the same
card geometry + auto-fit text rule as index.html."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ---- geometry (matches index.html: card 12.8cqw, center 51.2%/48.4%) ----
SRC = "background.jpg"
W2 = 560                                  # visible frame width
H2 = round(W2 * 768 / 1376)              # keep image aspect
M  = 14                                   # margin so shake-crop never shows edges
CARD = round(0.128 * W2)
PAD  = round(0.010 * W2)
RAD  = round(0.06 * CARD)
CX   = round(0.512 * W2) + M
CY   = round(0.484 * H2) + M
FONT_PATH = "C:/Windows/Fonts/ariblk.ttf"
FMAX = 0.017 * W2
FMIN = 0.009 * W2
INNER = CARD - 2 * PAD

PHRASES = [
    "To the moon!",
    "Buy everything",
    "It's fucking over",
    "Diamond hands",
    "Ask wife's boyfriend",
    "We're so back",
]

scratch = ImageDraw.Draw(Image.new("RGB", (10, 10)))

def wrap(text, font):
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if not cur or scratch.textlength(t, font=font) <= INNER:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines

def fit(text):
    text = text.upper()
    size = int(FMAX)
    while size >= FMIN:
        font = ImageFont.truetype(FONT_PATH, size)
        lines = wrap(text, font)
        widest = max(scratch.textlength(l, font=font) for l in lines)
        lh = size * 1.12
        if widest <= INNER and lh * len(lines) <= (CARD - 2 * PAD):
            return font, lines, lh
        size -= 1
    font = ImageFont.truetype(FONT_PATH, int(FMIN))
    return font, wrap(text, font), FMIN * 1.12

def make_card(text):
    font, lines, lh = fit(text)
    card = Image.new("RGBA", (CARD, CARD), (0, 0, 0, 0))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle([0, 0, CARD - 1, CARD - 1], radius=RAD, fill=(243, 244, 246, 255))
    total = lh * len(lines)
    y0 = (CARD - total) / 2 + lh / 2
    for i, line in enumerate(lines):
        d.text((CARD / 2, y0 + i * lh), line, font=font, fill=(12, 31, 74, 255), anchor="mm")
    return card

CARDS = {p: make_card(p) for p in PHRASES}

base_big = Image.open(SRC).convert("RGBA").resize((W2 + 2 * M, H2 + 2 * M), Image.LANCZOS)

def make_glow(scale, alpha):
    """Backlit blue halo behind the card — mirrors the CSS box-shadow layers."""
    g = Image.new("RGBA", base_big.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    for mult, col, a in [(0.95, (45, 95, 225), 70), (0.72, (130, 175, 255), 95)]:
        r = CARD * mult * scale
        gd.ellipse([CX - r, CY - r, CX + r, CY + r], fill=col + (int(a * alpha),))
    return g.filter(ImageFilter.GaussianBlur(int(CARD * 0.22)))

def frame(text, scale=1.0, alpha=1.0, blur=0.0, dx=0, dy=0):
    canvas = base_big.copy()
    c = CARDS[text]
    if scale != 1.0:
        ns = max(1, int(CARD * scale))
        c = c.resize((ns, ns), Image.LANCZOS)
    if blur > 0:
        c = c.filter(ImageFilter.GaussianBlur(blur))
    if alpha < 1.0:
        a = c.split()[3].point(lambda v: int(v * alpha))
        c = c.copy(); c.putalpha(a)
    if alpha > 0.02:
        canvas = Image.alpha_composite(canvas, make_glow(scale, alpha))
    canvas.alpha_composite(c, (int(CX - c.width / 2), int(CY - c.height / 2)))
    crop = canvas.crop((M + dx, M + dy, M + dx + W2, M + dy + H2))
    return crop.convert("RGB")

frames, durs = [], []
# transition keyframes: (scale, alpha, blur, dx, dy) for the OUTgoing card,
# then the INcoming card fading in. Mirrors the site's fade-out -> fade-in.
OUT = [(0.96, 0.75, 2, 5, -3), (0.88, 0.4, 5, -5, 3), (0.8, 0.0, 8, 4, 4)]
IN  = [(0.8, 0.25, 8, -4, -4), (0.9, 0.65, 4, 3, -2), (0.97, 0.9, 1, -1, 1)]

for i, p in enumerate(PHRASES):
    nxt = PHRASES[(i + 1) % len(PHRASES)]
    frames.append(frame(p)); durs.append(950)            # settled hold
    for s, a, b, dx, dy in OUT:
        frames.append(frame(p, s, a, b, dx, dy)); durs.append(70)
    for s, a, b, dx, dy in IN:
        frames.append(frame(nxt, s, a, b, dx, dy)); durs.append(70)

# single stable palette from a colorful settled frame -> avoids flicker
pal = frames[0].quantize(colors=256, method=Image.MEDIANCUT)
pframes = [f.quantize(palette=pal, dither=Image.NONE) for f in frames]
pframes[0].save("demo.gif", save_all=True, append_images=pframes[1:],
                duration=durs, loop=0, optimize=True, disposal=1)

import os
print("frames", len(frames), "size", round(os.path.getsize("demo.gif") / 1024 / 1024, 2), "MB", f"{W2}x{H2}")
