// Smooth scroll for details button
document.querySelectorAll('.details-btn').forEach(btn => {
  btn.addEventListener('click', e => {
    e.preventDefault();
    document.querySelector(btn.getAttribute('href')).scrollIntoView({
      behavior: 'smooth'
    });
  });
});
