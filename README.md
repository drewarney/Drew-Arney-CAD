# DAC — Drew Arney CAD

Logo files: `logo.svg` (flat, used on the site), `logo-mark.svg` (favicon), and `brand/` (master DAC logo with the matte + satin finish, SVG and transparent PNG, plus a reverse version with white lettering on black).

Static site: plain HTML/CSS/JS, three.js 3D viewer (bundled in /vendor, no build step).

## Add a project
The Our Work page (work.html) shows a placeholder until `PROJECTS` in `projects.js` has an entry.
Follow the template comment there: put STL file(s) in `/models` and drawing PNGs + PDF in `/drawings`.
From Fusion: export STEP and send it to Claude to convert, or right-click each body → Save as Mesh → STL.
(Drawing PNGs: export the drawing as PDF, then File → Save As → PNG per sheet, or ask Claude.)

## Preview locally
    python3 -m http.server   →   open http://localhost:8000
(Double-clicking index.html won't load the 3D model; browsers block that from file://.)

## Publish on GitHub Pages
1. Create a public repo (e.g. `drewarneycad.com`) and upload every file in this folder.
2. Repo → Settings → Pages → Source: "Deploy from a branch" → `main` / root → Save.
3. Settings → Pages → Custom domain → enter your domain → Save, then tick "Enforce HTTPS" once it's available.

## Point your domain at it (at your registrar's DNS settings)
| Type  | Host | Value                   |
|-------|------|-------------------------|
| A     | @    | 185.199.108.153         |
| A     | @    | 185.199.109.153         |
| A     | @    | 185.199.110.153         |
| A     | @    | 185.199.111.153         |
| CNAME | www  | YOUR-GITHUB-USERNAME.github.io |
Delete any existing A records on @ (e.g. a registrar "parking" page). DNS takes minutes to a few hours.

## Edit the website text
Every editable piece of text carries a `data-text="<id>"` attribute (tagline, contact details, and services live in `projects.js`).
`tools/site_text.py` moves all of it in and out of one JSON file, which is what the "DAC Website Text" editor artifact saves:

    python3 tools/site_text.py export content.json   # site -> JSON
    python3 tools/site_text.py apply  content.json   # JSON -> site
