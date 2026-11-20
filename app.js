'use strict';

// GIF playback is native. JavaScript only handles optional manual pause/resume.
(() => {
  for (const image of document.querySelectorAll('.animation')) {
    const toggle = () => {
      const pause = image.getAttribute('src') === image.dataset.gif;
      image.src = pause ? image.dataset.still : image.dataset.gif;
      image.setAttribute('aria-label', `${pause ? 'Play' : 'Pause'} ${image.dataset.description}`);
      image.setAttribute('aria-pressed', String(!pause));
    };
    image.addEventListener('click', toggle);
    image.addEventListener('keydown', event => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        toggle();
      }
    });
  }
})();
