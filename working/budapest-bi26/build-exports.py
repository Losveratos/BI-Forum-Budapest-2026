#!/usr/bin/env python3
"""Build the PDF and PowerPoint exports of story-v2.html. Usage: python build-exports.py (no arguments).

Writes One-Model-Three-Visual-Stacks.pdf and One-Model-Three-Visual-Stacks.pptx next to the deck.
Rerun after any change to story-v2.html or to a PNG in assets/.

Requirements:
  - Google Chrome or Microsoft Edge (found automatically; or set CHROME to the exe path)
  - Python 3.9+ with:  pip install pymupdf python-pptx   (use a venv, not the system Python)
  - Internet access while printing: the deck loads the Exo 2 font from Google Fonts

Steps: headless Chrome prints the deck with its own print CSS (one 1920x1080 slide per page)
to PDF; PyMuPDF renders every page to an image and extracts its text; python-pptx builds a
13.333 x 7.5 in deck with the rendered slide as a full-bleed picture, the headline as the
(off-slide) title for outline and accessibility, the picture alt text, and the visible slide
text in the notes so it is searchable.
"""
import io
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
DECK = HERE / "story-v2.html"
PDF = HERE / "One-Model-Three-Visual-Stacks.pdf"
PPTX = HERE / "One-Model-Three-Visual-Stacks.pptx"
RENDER_DPI = 144  # 1920 px page = 1440 pt; 144 dpi gives 2880 x 1620 px per slide
EXPECTED_SLIDES = 25


def find_browser():
    cands = [os.environ.get("CHROME", "")]
    for root in (os.environ.get("ProgramFiles"), os.environ.get("ProgramFiles(x86)"), os.environ.get("LOCALAPPDATA")):
        if root:
            cands += [
                os.path.join(root, "Google", "Chrome", "Application", "chrome.exe"),
                os.path.join(root, "Microsoft", "Edge", "Application", "msedge.exe"),
            ]
    for name in ("google-chrome", "chromium", "chrome", "msedge", "microsoft-edge"):
        cands.append(shutil.which(name) or "")
    for c in cands:
        if c and Path(c).is_file():
            return c
    sys.exit("No Chrome or Edge found. Set the CHROME environment variable to the browser exe.")


def build_pdf():
    browser = find_browser()
    with tempfile.TemporaryDirectory() as profile:
        cmd = [
            browser, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
            f"--user-data-dir={profile}", "--virtual-time-budget=20000",
            f"--print-to-pdf={PDF}", DECK.as_uri(),
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
    print(f"PDF: {PDF.name} ({PDF.stat().st_size / 1e6:.1f} MB)")


def headline(page):
    """Slide headline = the largest text on the page (all lines sharing the top size)."""
    spans = []
    for b in page.get_text("dict")["blocks"]:
        for ln in b.get("lines", []):
            for s in ln["spans"]:
                if s["text"].strip():
                    spans.append((s["size"], ln["bbox"][1], s["text"].strip()))
    top = max(s[0] for s in spans)
    parts = sorted((y, t) for sz, y, t in spans if sz >= top * 0.97)
    return " ".join(t for _, t in parts)


def build_pptx():
    import pymupdf
    from pptx import Presentation
    from pptx.util import Emu, Inches

    doc = pymupdf.open(PDF)
    if len(doc) != EXPECTED_SLIDES:
        print(f"WARNING: PDF has {len(doc)} pages, expected {EXPECTED_SLIDES}")
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    layout = prs.slide_layouts[5]  # Title Only
    for i, page in enumerate(doc, 1):
        title = headline(page)
        slide = prs.slides.add_slide(layout)
        t = slide.shapes.title
        t.text = title
        # park the title below the slide: invisible when presenting, present in outline/accessibility
        t.left, t.top, t.width, t.height = Inches(0.5), prs.slide_height + Inches(0.2), Inches(12), Inches(1)
        png = page.get_pixmap(dpi=RENDER_DPI).tobytes("png")
        pic = slide.shapes.add_picture(io.BytesIO(png), 0, 0, prs.slide_width, prs.slide_height)
        pic.name = f"Slide {i} image"
        pic._element.nvPicPr.cNvPr.set("descr", f"Slide {i}: {title}")
        slide.notes_slide.notes_text_frame.text = page.get_text("text").strip()
    prs.save(PPTX)
    print(f"PPTX: {PPTX.name} ({PPTX.stat().st_size / 1e6:.1f} MB, {len(prs.slides)} slides)")


if __name__ == "__main__":
    build_pdf()
    build_pptx()
