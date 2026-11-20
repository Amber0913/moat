'use strict';

// Actual GIF files play in view; still previews avoid animating the entire page.
(() => {
  const images = [...document.querySelectorAll('.animation')];
  const visible = new Set();
  const manuallyPaused = new WeakSet();
  const manuallyPlaying = new WeakSet();
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  function update(image) {
    const play = visible.has(image) && !document.hidden && !manuallyPaused.has(image) &&
      (!reducedMotion.matches || manuallyPlaying.has(image));
    const source = play ? image.dataset.gif : image.dataset.still;
    if (image.getAttribute('src') !== source) image.src = source;
    image.setAttribute('aria-label', `${play ? 'Pause' : 'Play'} ${image.dataset.description}`);
    image.setAttribute('aria-pressed', String(play));
  }

  function synchronize() { images.forEach(update); }

  for (const image of images) {
    const toggle = () => {
      if (image.getAttribute('src') === image.dataset.gif) {
        manuallyPaused.add(image);
        manuallyPlaying.delete(image);
      } else {
        manuallyPaused.delete(image);
        manuallyPlaying.add(image);
        visible.add(image);
      }
      update(image);
    };
    image.addEventListener('click', toggle);
    image.addEventListener('keydown', event => {
      if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); toggle(); }
    });
  }

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (entry.isIntersecting) visible.add(entry.target);
        else visible.delete(entry.target);
        update(entry.target);
      }
    }, { rootMargin: '150px 0px', threshold: 0 });
    images.forEach(image => observer.observe(image));
  } else images.forEach(image => visible.add(image));

  document.addEventListener('visibilitychange', synchronize);
  reducedMotion.addEventListener('change', synchronize);
  synchronize();
})();
