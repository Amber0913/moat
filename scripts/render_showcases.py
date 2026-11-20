"""Render the English showcase page from compact, editable prompt pairs."""
import json
from html import escape
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
TITLE = 'Generative Match-Cut Based on Visual References'


def image(case, name, description, width, height):
    base = f'assets/{case}/{name}'
    return (f'<img class="animation" src="{base}.gif" data-still="{base}.jpg" '
            f'data-gif="{base}.gif" width="{width}" height="{height}" '
            f'alt="{escape(description, quote=True)}" data-description="{escape(description, quote=True)}" '
            f'loading="lazy" decoding="async" tabindex="0" role="button" '
            f'aria-label="Pause {escape(description, quote=True)}" aria-pressed="true">')


def main():
    cases = json.loads((SITE/'scripts/showcases.json').read_text())
    cards = []
    for case in cases:
        cid = case['id']
        a = escape(case['prompt_a'])
        b = escape(case['prompt_b'])
        cards.append(f'''        <article class="showcase">
          <p class="version-label">original version</p>
          <div class="original-grid">
            <figure>
              <figcaption>video A</figcaption>
              {image(cid, 'original-a', 'original video A: '+case['prompt_a'], 240, 138)}
            </figure>
            <figure>
              <figcaption>video B</figcaption>
              {image(cid, 'original-b', 'original video B: '+case['prompt_b'], 240, 138)}
            </figure>
          </div>
          <p class="version-label edited-label">edited version</p>
          {image(cid, 'edited', 'edited match-cut showcase', 480, 276)}
          <div class="prompts">
            <p class="prompt-line"><span class="prompt-label">Prompt A:</span><span class="prompt-text">{a}</span></p>
            <p class="prompt-line"><span class="prompt-label">Prompt B:</span><span class="prompt-text">{b}</span></p>
          </div>
        </article>''')
    html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{TITLE}. Original reference videos and edited match-cut showcases.">
  <meta name="theme-color" content="#ffffff">
  <title>{TITLE}</title>
  <link rel="stylesheet" href="style.css?v=20261120-gif-default">
  <script src="app.js?v=20261120-gif-default" defer></script>
</head>
<body>
  <header class="publication-header">
    <h1>{TITLE}</h1>
  </header>
  <main>
    <section class="results" aria-labelledby="showcases-title">
      <h2 id="showcases-title">Showcases</h2>
      <div class="showcase-grid">
{chr(10).join(cards)}
      </div>
    </section>
  </main>
  <footer>
    <p>Page layout inspired by <a href="https://matchdiffusion.github.io/" target="_blank" rel="noreferrer">MatchDiffusion</a>.</p>
  </footer>
</body>
</html>
'''
    (SITE/'index.html').write_text(html)
    print(f'Rendered {len(cases)} showcases with original A/B, GIF results, and short prompts.')


if __name__ == '__main__':
    main()
