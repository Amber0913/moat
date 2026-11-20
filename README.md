# Generative Match-Cut Based on Visual References

A minimal English project page with a single-line title and a showcase grid, following
the presentation style of [MatchDiffusion](https://matchdiffusion.github.io/).

Open `index.html` directly, or preview from this repository with:

```bash
python -m http.server 8000
```

Visit `http://localhost:8000`. Each showcase contains two half-width original GIFs
(video A and video B), a full-width edited GIF, and two short English prompts.
The prompts stay on one line and cannot expand the grid columns. Original and
edited versions are labeled above their images.

GIFs load directly as images and animate without JavaScript. Native lazy loading
defers images farther down the page. Click one, or focus it and press Enter/Space,
to switch between the animation and its still preview. The script only provides
these manual pause/resume controls.

The displayed showcases are listed in `scripts/showcases.json` and retain their
source order. Prompts are labeled `Prompt A` and `Prompt B`.
There are no case names, categories, statistics, toolbars, or selection controls.
The original GIFs come from the original A/B source videos, not edited_A.mp4.
GIFs retain the full frame and clip duration, sampled at 10 fps. Edited GIFs are
480 pixels wide; originals are 240 pixels wide. The source MP4 files are unchanged.

Compact prompts and source mappings are in `scripts/showcases.json`. To regenerate
the GIFs and page from the source workspace (ffmpeg required):

```bash
python scripts/build_gifs.py
python scripts/render_showcases.py
```

To publish with GitHub Pages, set **Settings > Pages > Deploy from a branch** to
**main / (root)**. All paths are relative, so the page also works under a project
URL such as `https://amber0913.github.io/moat.github.io/`.
