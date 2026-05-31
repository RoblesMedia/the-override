# The Override — Landing / Squeeze Page

A single-file, dependency-free landing page for the book **The Override** by David Robles, LMSW.
Captures **first name + email** to send the free *Override Starter Guide* PDF.

Design goes off the book covers: storm→sunrise crossroads, distressed white title,
glowing blue/gold Trigger → Pause → Override → New Action → New Outcome path, circular stamp.
(Deliberately does **not** look like therapybydavid.com.)

## Files
- `index.html` — the whole page (HTML + CSS + JS inline). Fonts load from Google Fonts CDN.
- `cover.png` — the vertical fork-in-the-road cover (THE BOOK V1), shown crisp as the product in the hero.
- `cover-bg.png` — the square figure-at-crossroads cover (THE BOOK V2), blurred + darkened as the hero background.
  (To swap which cover is the product vs. the background, just rename/replace these two files.)

## Preview locally
```bash
cd /Users/robles/Clients/the-override-landing
python3 -m http.server 8091
# open http://localhost:8091
```

## Cover art
The hero already uses the real cover art (`cover.png` as the product, `cover-bg.png` as the
blurred background). Sourced from `~/Desktop/THE BOOK V1.png` and `THE BOOK V2.png`.

## Wire up email capture (currently DEMO MODE)
The form validates and shows a success state, but does **not** send anything yet.
Open `index.html`, find:

```js
const ENDPOINT = ""; // <-- paste your Worker / Mailchimp / Formspree URL here
```

Set `ENDPOINT` to one of:

- **Cloudflare Worker** (matches David's stack) — a Worker that accepts
  `POST {name, email, source}` as JSON, stores the signup, and emails the PDF via Resend.
  Same pattern as the existing `openpath-intake` / `therapybydavid-intake` Workers.
- **Mailchimp / beehiiv** — use their embedded form action URL (both accounts already exist).
  Their automation handles storage + the welcome email with the PDF.
- **Formspree / similar** — paste the form endpoint; it forwards submissions to email.

The page POSTs JSON `{ name, email, source: "override-landing" }`. A honeypot field
(`company`) silently drops bots.

## Deploy to GitHub Pages
1. Create a new repo (e.g. `the-override`) and push `index.html` to the default branch.
2. Repo → Settings → Pages → deploy from branch root.
3. Point a custom domain via Cloudflare (same setup as therapybydavid.com):
   add a CNAME for the subdomain → `<user>.github.io`, and a `CNAME` file in the repo.

## Notes
- Footer carries the standard "not therapy / 988 crisis" disclaimer.
- All copy is drawn from the book outline (the 8 patterns, the two-path model, author bio).
