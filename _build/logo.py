#!/usr/bin/env python3
"""Draw the anchor-and-stars mark, an original take on the Rhode Island flag's seal.

Run from the repo root:  python3 _build/logo.py
Writes three SVGs to assets/:
  logo-on-white.svg  navy anchor, gold stars, blue HOPE ribbon (for white backgrounds)
  logo-on-blue.svg   white anchor, gold stars, white HOPE ribbon (for the blue header and navy footer)
  favicon.svg        the on-white mark without the ribbon text, for browser tabs
"""
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GOLD = "#F2C230"       # stars on blue: 8.2:1 against #2253A5 is not needed for graphics, 3:1 is; this clears both backgrounds
GOLD_DARK = "#A87A00"  # stars on white: 3.6:1 against white (WCAG 1.4.11 non-text contrast needs 3:1)


def star(cx, cy, r_out, r_in, rot=-90):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 36)
        pts.append(f"{cx + r * math.cos(a):.2f},{cy + r * math.sin(a):.2f}")
    return f'<polygon points="{" ".join(pts)}"/>'


def stars(fill):
    """13 stars on a ring, like the flag's circle of stars."""
    out = []
    for i in range(13):
        a = math.radians(-90 + i * 360 / 13)
        out.append(star(60 + 50 * math.cos(a), 60 + 50 * math.sin(a), 5.2, 2.1, rot=-90))
    return f'<g fill="{fill}">{"".join(out)}</g>'


def anchor(color):
    return f"""<g fill="none" stroke="{color}" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="60" cy="24" r="6"/>
    <line x1="60" y1="30" x2="60" y2="92"/>
    <line x1="44" y1="39" x2="76" y2="39"/>
    <path d="M30 70 C 34 86, 46 93, 60 93 C 74 93, 86 86, 90 70"/>
  </g>
  <g fill="{color}">
    <polygon points="24,74 32,62 38,74"/>
    <polygon points="96,74 88,62 82,74"/>
  </g>"""


def ribbon(fill, text_fill):
    return f"""<g>
    <path d="M22 104 L98 104 L104 112 L98 120 L22 120 L16 112 Z" fill="{fill}"/>
    <text x="60" y="116.5" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="11" font-weight="700" letter-spacing="2.5" fill="{text_fill}">HOPE</text>
  </g>"""


def svg(body, title, h=124):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 {h}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title>{body}</svg>\n')


def main():
    a = ROOT / "assets"
    a.mkdir(exist_ok=True)
    (a / "logo-on-white.svg").write_text(svg(stars(GOLD_DARK) + anchor("#040D40") + ribbon("#2253A5", "#FFFFFF"),
                                             "Anchor and thirteen stars, the Rhode Island seal"))
    (a / "logo-on-blue.svg").write_text(svg(stars(GOLD) + anchor("#FFFFFF") + ribbon("#FFFFFF", "#2253A5"),
                                            "Anchor and thirteen stars, the Rhode Island seal"))
    (a / "favicon.svg").write_text(svg(f'<rect width="120" height="120" fill="#2253A5"/>' + stars(GOLD) + anchor("#FFFFFF"),
                                       "Office of the Governor", h=120))
    print("wrote logos")


if __name__ == "__main__":
    main()
