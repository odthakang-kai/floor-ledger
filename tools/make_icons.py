#!/usr/bin/env python3
"""Draw the Floor Ledger home-screen icons with the standard library only (no Pillow).
Original artwork: three rising white bars on orange over a tape-measure tick strip. No store logos.
usage: python tools/make_icons.py   (writes icon-*.png and apple-touch-icon.png next to index.html)"""
import os, struct, zlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORANGE, WHITE, CHAR = (249, 99, 2), (255, 255, 255), (35, 37, 39)
SS = 2  # supersampling for smooth edges


def shapes(k):
    """Shapes in a 1000-unit square; k shrinks art toward the center for maskable icons."""
    c = 500
    s = lambda v: c + (v - c) * k
    R = lambda x0, y0, x1, y1, col, rad=0: ("r", s(x0), s(y0), s(x1), s(y1), col, rad * k)
    out = [
        R(160, 640, 840, 780, CHAR, 22),          # tape body
        R(250, 470, 370, 640, WHITE, 14),         # bars
        R(440, 350, 560, 640, WHITE, 14),
        R(630, 210, 750, 640, WHITE, 14),
    ]
    for i in range(0, 25):                        # tape ticks: long every 4th
        x = 190 + i * 26
        h = 70 if i % 4 == 0 else 38
        out.append(R(x, 650, x + 7, 650 + h, ORANGE))
    return out


def inside(sh, x, y):
    _, x0, y0, x1, y1, _, rad = sh
    if not (x0 <= x <= x1 and y0 <= y <= y1):
        return False
    if rad <= 0:
        return True
    cx = min(max(x, x0 + rad), x1 - rad)
    cy = min(max(y, y0 + rad), y1 - rad)
    return (x - cx) ** 2 + (y - cy) ** 2 <= rad * rad


def render(size, maskable=False):
    sh = shapes(0.8 if maskable else 1.0)
    rows = []
    n = size * SS
    for py in range(size):
        row = bytearray([0])
        for px in range(size):
            acc = [0, 0, 0]
            for sy in range(SS):
                y = (py * SS + sy + 0.5) / n * 1000
                for sx in range(SS):
                    x = (px * SS + sx + 0.5) / n * 1000
                    col = ORANGE
                    for s_ in sh:
                        if inside(s_, x, y):
                            col = s_[5]
                    acc[0] += col[0]; acc[1] += col[1]; acc[2] += col[2]
            row += bytes(int(a / (SS * SS)) for a in acc)
        rows.append(bytes(row))
    raw = b"".join(rows)
    chunk = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")


for name, size, mask in [("icon-192.png", 192, False), ("icon-512.png", 512, False), ("icon-maskable-512.png", 512, True), ("apple-touch-icon.png", 180, False)]:
    with open(os.path.join(ROOT, name), "wb") as f:
        f.write(render(size, mask))
    print("wrote", name)
