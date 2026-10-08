# Yaroslav Mukhin — academic website

Static, single-page website for GitHub Pages. Edit the HTML and CSS directly;
no build step is needed to view or publish the supplied website. The three
Python helpers are optional local utilities, not deployment dependencies.

Run commands from this directory unless stated otherwise.

## Edit content and styling

| File | Purpose |
| --- | --- |
| `index.html` | Biography, publications, coauthors, talks, teaching, running, and links. |
| `styles.css` | Layout, typography, spacing, portrait crop, and artwork placement. |
| `assets/` | Photograph, SVG artwork, contact graphic, and favicon. |
| `publications.bib` | Downloadable BibTeX records and source for the inline citation display. |
| `sources/observed-trajectories-web.tex` | Editable source for the displayed illustration. |
| `sources/stopped-trajectories.tex` | Original slide frame, linked from Research. |
| `files/` | Public documents such as a CV or talk slides. |

Copy an existing article, talk, or running entry when adding content. Keep HTML
`id` values unique. Use relative paths for local files, such as `files/cv.pdf`.
The optional CV and profile links are commented out until you supply their targets.
Keep conference date ranges distinct from individual presentation dates.

### Layout controls

Edit the variables at the top of `styles.css`, then reload the browser. All current
settings are in that file; there is no second configuration file to synchronize.

The main controls are `--page-width`, `--portrait-width`, `--portrait-ratio`,
`--name-size`, `--subtitle-size`, `--body-size`, and `--paper-title-size`.
For the artwork, use `--artifact-overlap`, `--artifact-size`, `--artifact-scale`,
`--artifact-x`, `--artifact-y`, and the alignment controls.
Positive x/y offsets move the graphic right/down; negative values move it left/up.

CSS resizing and positioning do **not** require recompiling the SVG. Rebuild only
when changing the drawing, labels, colors, or relative line/text sizes. Preview
large size or offset changes to check for overlap and horizontal scrolling.
Responsive overrides immediately below the main controls apply at smaller widths;
edit them separately when a change should also apply on phones or compact desktops.

### Photograph and contact graphic

Replace `assets/portrait.jpg` to change the photograph. Update the image's intrinsic
`width` and `height` in `index.html` when its pixel dimensions change, and keep
meaningful alt text. Adjust `--portrait-crop-x` and `--portrait-crop-y` for the crop.

The contact graphic is path-only SVG and is not a link. To regenerate it, install
Inkscape with its command available on `PATH`, then run:

```bash
python3 tools/make_email.py
```

Enter the address at the hidden prompt. Do not store it in HTML, SVG text or
metadata, accessible labels, command-line arguments, or committed configuration.
The helper uses temporary files and retains only outlined paths in
`assets/email.svg`. Use `--help` for dimensions and font-size options.
Check that the complete line fits; adjust the email size controls if necessary.

This keeps a textual address out of these source files, not out of the visible
image. Screen readers cannot read or copy it as text. Review any existing public
Git history separately; replacing a file does not rewrite earlier commits.

### Citations

Edit `publications.bib`, then update the inline BibTeX disclosure:

```bash
python3 tools/sync_citations.py
```

Commit both `publications.bib` and the updated `index.html`. The helper changes
only the block between the generated-citation comments; it does not update paper
titles, displayed years, or other research text.

Use unique keys in the form `surnameYYYYkeyword`, such as `mukhin2025kernel`.
When changing a key, also update its article's `data-bib-key` in `index.html`.
Keep displayed years and bibliography years consistent.

## Compile the illustration

The supplied SVG is ready to publish. To change it, edit
`sources/observed-trajectories-web.tex`, then run:

```bash
python3 tools/render_artifact.py
```

Local requirements: Python 3.10 or later, LuaLaTeX, TikZ, the Beamer Metropolis
theme, Fira Sans, the LaTeX `preview` package, and Poppler's `pdftocairo`.
Both `lualatex` and `pdftocairo` must be on `PATH`.

The helper compiles in a temporary directory, converts the PDF to outlined SVG,
and writes `assets/stopped-trajectories.svg`. It does not publish intermediate
PDFs, raster copies, font files, or diagnostic reports. Review the illustration
in the page, then commit its source and the updated SVG.

## Preview

Open `index.html` in your browser. A local server is optional:

```bash
python3 -m http.server 8000
```

Visit `http://localhost:8000`; stop the server with `Ctrl+C`.
Before publishing, check the page at desktop and phone widths, open the figure
and citation disclosures, and test changed links and the bibliography download.

## Deploy to GitHub Pages

### First deployment

Create an empty repository named `YOUR-USERNAME.github.io`. Put this directory's
contents at the repository root, not inside an extra enclosing folder.
Substitute your username in these commands:

```bash
git init -b main
git add .
git commit -m "Create academic website"
git remote add origin https://github.com/YOUR-USERNAME/YOUR-USERNAME.github.io.git
git push -u origin main
```

Under **Settings → Pages**, select **Deploy from a branch**, **main**, and
**/(root)**. Keep `.nojekyll`. No custom build workflow is needed.

### Updates

Edit files in your existing repository and run a helper only when its source has
changed. Preview, review the diff, and push:

```bash
git status
git diff
git add -A
git commit -m "Update website"
git push
```

When replacing a previously supplied package, preserve the existing `.git`
directory, working `CNAME`, CV, and any other personal files you have added.
Remove retired files explicitly: copying a new folder over an old one does not
delete files that are absent from the new package.

### Custom domain

Verify domain ownership with GitHub, set **Settings → Pages → Custom domain**,
and configure the DNS records at your domain provider using GitHub's instructions.
The publishing-root `CNAME` must contain only the domain, without `https://` or
a path. `CNAME.example` is an inactive example; preserve any working `CNAME`.
Enable **Enforce HTTPS** when available.

Official instructions:

- [Publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [Custom domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)
