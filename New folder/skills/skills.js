function enableMarqueeControls(marqueeId) {
  const marquee = document.querySelector(`#${marqueeId} .skills-track`);
  const container = document.getElementById(marqueeId);
  let isPaused = false;

  function toggleScroll() {
    if (isPaused) {
      marquee.style.animationPlayState = "running";
    } else {
      marquee.style.animationPlayState = "paused";
    }
    isPaused = !isPaused;
  }

  // Pause on hover (desktop)
  container.addEventListener("mouseenter", () => {
    marquee.style.animationPlayState = "paused";
  });
  container.addEventListener("mouseleave", () => {
    marquee.style.animationPlayState = "running";
  });

  // Pause/resume on click (mobile + desktop)
  container.addEventListener("click", toggleScroll);
}

enableMarqueeControls("marquee1");
enableMarqueeControls("marquee2");
