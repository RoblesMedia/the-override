#!/usr/bin/env python3
"""
Generate the Override Starter Guide PDF (coaching lead magnet).

IMPORTANT — brand rule: this is the COACHING brand. Never print the clinical
license ("LMSW", "LCSW", "Licensed Psychotherapist") or frame the guide as
therapy / clinical practice. Credibility = Creator of the Override Method.

Usage:
    .venv/bin/python build_guide.py [output.pdf]
Default output: override-starter-guide.pdf
"""
import sys
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

OUT = sys.argv[1] if len(sys.argv) > 1 else "override-starter-guide.pdf"

W, H = letter  # 612 x 792
M = 64         # margin

INK   = HexColor("#15120d")
GOLD  = HexColor("#f0a500")
GRAY  = HexColor("#6b6b6b")
LIGHT = HexColor("#9a9a9a")
DARK  = HexColor("#0a0a0a")
WHITE = HexColor("#ffffff")
CREAM = HexColor("#f3efe7")

BODY  = "Helvetica"
BOLD  = "Helvetica-Bold"
OBL   = "Helvetica-Oblique"

c = canvas.Canvas(OUT, pagesize=letter)
c.setTitle("The Override Starter Guide")
c.setAuthor("David Robles")                      # no license — coaching brand
c.setSubject("Break the pattern. Choose your life.")
c.setCreator("The Override")


def tracked(x, y, s, font, size, color, tracking=2.0, center=False):
    """Draw letter-spaced (tracked) text. Returns total width."""
    widths = [c.stringWidth(ch, font, size) for ch in s]
    total = sum(widths) + tracking * (len(s) - 1 if s else 0)
    cx = x - total / 2 if center else x
    c.setFont(font, size)
    c.setFillColor(color)
    for ch, w in zip(s, widths):
        c.drawString(cx, y, ch)
        cx += w + tracking
    return total


def wrap(text, font, size, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if c.stringWidth(t, font, size) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(x, y, text, font, size, color, maxw, leading, center=False):
    c.setFont(font, size)
    c.setFillColor(color)
    for ln in wrap(text, font, size, maxw):
        if center:
            c.drawCentredString(x, y, ln)
        else:
            c.drawString(x, y, ln)
        y -= leading
    return y


def footer(page):
    tracked(M, 54, "THE OVERRIDE  ·  STARTER GUIDE", BOLD, 7.5, LIGHT, tracking=2.2)
    c.setFont(BOLD, 9)
    c.setFillColor(GOLD)
    c.drawRightString(W - M, 54, str(page))


def eyebrow(y, label):
    tracked(M, y, label, BOLD, 10, GOLD, tracking=3.0)


def heading(y, text, size=30):
    c.setFont(BOLD, size)
    c.setFillColor(INK)
    c.drawString(M, y, text)


# ----------------------------------------------------------------- PAGE 1 (cover)
c.setFillColor(DARK)
c.rect(0, 0, W, H, fill=1, stroke=0)
tracked(M, H - 96, "A FREE STARTER GUIDE", BOLD, 11, GOLD, tracking=4.5)

c.setFont(BOLD, 76)
c.setFillColor(WHITE)
c.drawString(M, H - 196, "THE")
c.setFillColor(GOLD)
c.drawString(M, H - 268, "OVERRIDE")

c.setFont(BODY, 17)
c.setFillColor(HexColor("#d8d8d8"))
c.drawString(M, H - 312, "The Hidden Code Running Your Life")
c.drawString(M, H - 336, "& How to Rewrite It")

c.setStrokeColor(GOLD)
c.setLineWidth(2)
c.line(M, H - 372, M + 84, H - 372)

c.setFont(BOLD, 18)
c.setFillColor(GOLD)
c.drawString(M, H - 410, "Break the pattern. Choose your life.")

para(M, H - 446,
     "A short, practical guide to seeing the pattern while it's running, "
     "creating a pause, and choosing a different response.",
     BODY, 13, HexColor("#b6b6b6"), W - 2 * M - 60, 19)

c.setFont(BOLD, 15)
c.setFillColor(WHITE)
c.drawString(M, 112, "DAVID ROBLES")
tracked(M, 90, "CREATOR OF THE OVERRIDE METHOD", BOLD, 9.5, GOLD, tracking=2.6)
c.showPage()


# ----------------------------------------------------------------- PAGE 2 (model)
c.setFillColor(WHITE); c.rect(0, 0, W, H, fill=1, stroke=0)
eyebrow(H - 92, "THE MODEL")
heading(H - 128, "One Pattern. Two Paths.")
y = para(M, H - 168,
         "You are not your patterns. You are the one running them. Most of life runs on "
         "autopilot — the same trigger producing the same outcome, again and again. "
         "The Override is the one move that changes the path.",
         BODY, 12.5, INK, W - 2 * M, 19)


def path_row(y, label, steps, label_color, chip_bg, chip_fg, chip_border):
    tracked(M, y, label, BOLD, 9, label_color, tracking=2.4)
    y -= 26
    x = M
    c.setFont(BOLD, 10.5)
    for i, st in enumerate(steps):
        tw = c.stringWidth(st, BOLD, 10.5)
        cw = tw + 22
        c.setFillColor(chip_bg)
        if chip_border:
            c.setStrokeColor(chip_border); c.setLineWidth(1); sf = 1
        else:
            sf = 0
        c.roundRect(x, y - 16, cw, 26, 6, fill=1, stroke=sf)
        c.setFillColor(chip_fg)
        c.drawString(x + 11, y - 8, st)
        x += cw
        if i < len(steps) - 1:
            c.setFillColor(GRAY); c.setFont(BODY, 12)
            c.drawString(x + 5, y - 7, "→"); x += 19
            c.setFont(BOLD, 10.5)
    return y - 40

y = path_row(y - 18, "THE OLD PATH — RUNNING ON AUTOPILOT",
             ["Trigger", "Story", "Emotion", "Pattern", "Outcome"],
             GRAY, CREAM, GRAY, HexColor("#e0dccf"))
y = path_row(y, "THE NEW PATH — THE OVERRIDE",
             ["Trigger", "Pause", "Override", "New Action", "New Outcome"],
             GOLD, GOLD, DARK, None)

# key insight callout
box_y = y - 8
c.setFillColor(CREAM)
c.roundRect(M, box_y - 86, W - 2 * M, 86, 12, fill=1, stroke=0)
c.setStrokeColor(GOLD); c.setLineWidth(3)
c.line(M, box_y - 86, M, box_y)
tracked(M + 22, box_y - 24, "THE KEY INSIGHT", BOLD, 9, GOLD, tracking=2.6)
para(M + 22, box_y - 44,
     "The trigger didn't cause the outcome. The story did — and the story was written a "
     "long time ago. The pause is where you catch it. The override is where you choose differently.",
     BODY, 11.5, INK, W - 2 * M - 44, 17)
footer(2)
c.showPage()


# ----------------------------------------------------------------- PAGE 3 (assessment)
c.setFillColor(WHITE); c.rect(0, 0, W, H, fill=1, stroke=0)
eyebrow(H - 92, "SELF-ASSESSMENT")
heading(H - 128, "Which One Are You?")
y = para(M, H - 166,
         "Eight patterns. Each one made sense once — it was protecting something. Most people "
         "are running at least one, usually without ever naming it. Read each tell and check the "
         "ones that feel like you. Then circle your top one or two.",
         BODY, 12, INK, W - 2 * M, 18)

patterns = [
    ("The Achiever", "Doing everything right and feeling dead inside. Outruns the emptiness with more — but the goal post keeps moving."),
    ("The Peacekeeper", "Never says what she needs. Years of swallowed words have built a quiet wall of resentment."),
    ("The Fixer", "Solves everyone's problem so he never has to sit with his own. Feels most alive when needed."),
    ("The Avoider", "Doesn't start what she might not finish. Lives in a permanent state of ‘almost.’"),
    ("The Perfectionist", "Standards impossible by design. If the bar can't be cleared, he can never truly fail — just ‘not yet.’"),
    ("The Pleaser", "Learned love is conditional. Shapeshifts to be whoever's wanted — and lost track of what she wants."),
    ("The Controller", "Doesn't trust it'll go well unless he manages every variable. Control is the only safety he's known."),
    ("The Drifter", "Likable, capable, and in the same place for years. Goes along with things. Disconnection as flexibility."),
]
y -= 14
for name, tell in patterns:
    c.setStrokeColor(GOLD); c.setLineWidth(1.4)
    c.rect(M, y - 10, 13, 13, fill=0, stroke=1)
    c.setFont(BOLD, 12.5); c.setFillColor(INK)
    c.drawString(M + 26, y, name)
    para(M + 26, y - 16, tell, BODY, 10.5, GRAY, W - 2 * M - 26, 14)
    y -= 50
footer(3)
c.showPage()


# ----------------------------------------------------------------- PAGE 4 (tool)
c.setFillColor(WHITE); c.rect(0, 0, W, H, fill=1, stroke=0)
eyebrow(H - 92, "YOUR FIRST TOOL")
heading(H - 128, "The 10-Second Pause")
y = para(M, H - 168,
         "Between what happens to you and what you do next, there is a space. For most people "
         "running automatic patterns, that space is a fraction of a second — the pattern fires "
         "before there's any awareness it was coming. The work is to widen that space until "
         "there's room for a choice. Start here.",
         BODY, 12.5, INK, W - 2 * M, 19)

steps = [
    ("Notice the cue", "Learn the physical signal that your pattern is about to fire — a tight chest, a held breath, a clenched jaw, a flush of heat. The body knows before the mind does."),
    ("Do nothing for ten seconds", "When you feel it, don't respond. Don't send the text, say the thing, or take the action. Just breathe — slow out-breaths. Ten seconds. That's the whole drill."),
    ("Ask one question", "In the space you just made, ask: ‘Is this a fact, or a story?’ Then choose your response from there — not from the pattern."),
]
y -= 16
for i, (title, desc) in enumerate(steps, 1):
    c.setFillColor(GOLD)
    c.circle(M + 12, y - 4, 13, fill=1, stroke=0)
    c.setFillColor(DARK); c.setFont(BOLD, 13)
    c.drawCentredString(M + 12, y - 8, str(i))
    c.setFont(BOLD, 13.5); c.setFillColor(INK)
    c.drawString(M + 36, y, title)
    ny = para(M + 36, y - 18, desc, BODY, 11.5, GRAY, W - 2 * M - 36, 16)
    y = ny - 14

# try-it callout
box_y = y - 4
c.setFillColor(DARK)
c.roundRect(M, box_y - 78, W - 2 * M, 78, 12, fill=1, stroke=0)
tracked(M + 22, box_y - 24, "TRY IT THIS WEEK", BOLD, 9, GOLD, tracking=2.6)
para(M + 22, box_y - 44,
     "Pick one recurring trigger — a certain email, a certain person, a certain time of day. "
     "For one week, run the 10-second pause every time it shows up. Notice what changes.",
     BODY, 11.5, HexColor("#dcdcdc"), W - 2 * M - 44, 16)
footer(4)
c.showPage()


# ----------------------------------------------------------------- PAGE 5 (close)
c.setFillColor(DARK); c.rect(0, 0, W, H, fill=1, stroke=0)
tracked(M, H - 110, "THIS IS THE FIRST MOVE", BOLD, 11, GOLD, tracking=4.0)
c.setFont(BOLD, 40); c.setFillColor(WHITE)
c.drawString(M, H - 168, "The book goes deeper.")
para(M, H - 208,
     "This guide gives you the model and the first tool. The Override — the book — walks the "
     "whole path: how patterns get written, what they're protecting, how to build the pause, "
     "execute the override, and make a new response your default.",
     BODY, 13, HexColor("#cfcfcf"), W - 2 * M - 40, 21)
c.setFont(BOLD, 14); c.setFillColor(GOLD)
c.drawString(M, H - 300, "Keep an eye on your inbox — more is coming.")

# disclaimer box (coaching-safe — NOT clinical)
by = 250
c.setFillColor(HexColor("#141414"))
c.roundRect(M, by - 118, W - 2 * M, 118, 12, fill=1, stroke=0)
c.setStrokeColor(HexColor("#2a2a2a")); c.setLineWidth(1)
c.roundRect(M, by - 118, W - 2 * M, 118, 12, fill=0, stroke=1)
tracked(M + 22, by - 26, "PLEASE READ", BOLD, 9, LIGHT, tracking=2.6)
para(M + 22, by - 46,
     "The Override is a coaching and personal-growth resource. It is not therapy, not a "
     "diagnosis, and not a replacement for professional mental-health care. If you are in "
     "crisis, call or text 988 (Suicide & Crisis Lifeline) or dial 911.",
     BODY, 10.5, HexColor("#9a9a9a"), W - 2 * M - 44, 15)

tracked(M, 64, "© DAVID ROBLES  ·  THE OVERRIDE", BOLD, 8.5, LIGHT, tracking=2.2)
c.showPage()

c.save()
print("wrote", OUT)
