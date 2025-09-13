// Magnetic hover effect on icons
document.querySelectorAll(".connect-btn").forEach(btn => {
  const icon = btn.querySelector("i");

  btn.addEventListener("mousemove", (e) => {
    const rect = btn.getBoundingClientRect();
    const x = e.clientX - rect.left - rect.width / 2;
    const y = e.clientY - rect.top - rect.height / 2;

    icon.style.transform = `translate(${x * 0.15}px, ${y * 0.15}px) scale(1.2)`;
  });

  btn.addEventListener("mouseleave", () => {
    icon.style.transform = "translate(0, 0) scale(1)";
  });
});


document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".connect-btn");

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.2 }
  );

  buttons.forEach((btn) => observer.observe(btn));
});
