'use strict';

// Load later GIFs near the viewport instead of downloading the whole gallery.
(() => {
  const images = [...document.querySelectorAll('.animation')];
  const pending = new Set(images.filter(image => image.hasAttribute('data-deferred')));

  function activate(image) {
    if (!pending.delete(image)) return;
    image.removeAttribute('data-deferred');
    image.loading = 'eager';
    image.src = image.dataset.gif;
    image.setAttribute('aria-label', `Pause ${image.dataset.description}`);
    image.setAttribute('aria-pressed', 'true');
  }

  for (const image of images) {
    const toggle = () => {
      if (pending.has(image)) { activate(image); return; }
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

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          activate(entry.target);
          observer.unobserve(entry.target);
        }
      }
    }, { rootMargin: '100px 0px', threshold: 0 });
    pending.forEach(image => observer.observe(image));
  } else [...pending].forEach(activate);
})();
