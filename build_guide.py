#!/usr/bin/env python3
"""
Generate the Override Starter Guide PDF (coaching lead magnet).

IMPORTANT — brand rule: this is the COACHING brand. Never print the clinical
license ("LMSW", "LCSW", "Licensed Psychotherapist") or frame the guide as
therapy / clinical practice. Credibility = Creator of the Override Method.
Per David (2026-08-10): the guide is NOT a book promotion. The close page is
a coaching CTA (free consultation), and the book-cover art stays out of it
(the mockup also carries a "Psychotherapist" byline, which is banned here).

The design lives in guide.html (Archivo Black / Space Grotesk, black + gold,
photos in guide-assets/). This script prints it to PDF with headless Chrome.

Usage:
    python3 build_guide.py [output.pdf]
Default output: override-starter-guide.pdf   <- keep this name: it is linked
from theoverride.co (hero CTA + every /pattern/* page) and from past emails.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else "override-starter-guide.pdf"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

ASSETS = [
    "guide.html",
    "guide-assets/cover-tunnel.jpg",     # Alexander Kaufmann / Unsplash
    "guide-assets/pause-water.jpg",      # Clayton Tonna / Unsplash
]

for rel in ASSETS:
    if not os.path.exists(os.path.join(HERE, rel)):
        sys.exit(f"missing {rel} — guide can't build without it")

if not os.path.exists(CHROME):
    sys.exit("Google Chrome not found — needed to render guide.html to PDF")

out_path = os.path.join(HERE, OUT)
subprocess.run(
    [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--no-pdf-header-footer",
        "--virtual-time-budget=20000",  # let Google Fonts + images finish loading
        f"--print-to-pdf={out_path}",
        "file://" + os.path.join(HERE, "guide.html"),
    ],
    check=True,
    capture_output=True,
)

size_mb = os.path.getsize(out_path) / 1e6
print(f"wrote {OUT} ({size_mb:.1f} MB)")
