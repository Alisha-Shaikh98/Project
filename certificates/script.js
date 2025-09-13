let angle = 0;
let numCards = 0;
let rotationStep = 0;

function loadCertificates() {
  Papa.parse("certificates_full_with_desc.csv", {
    download: true,
    header: true,
    complete: function(results) {
      certificatesData = results.data.filter(c => c.Title); // store all
      renderCertificates("All");
    }
  });
}

function renderCertificates(category) {
  const box = document.getElementById("certificates-box");
  box.innerHTML = "";
  angle = 0; // reset rotation

  const filtered = category === "All"
    ? certificatesData
    : certificatesData.filter(c => c.Category === category);

  filtered.forEach(cert => {
    const card = document.createElement("div");
    card.className = "cert-card";
    card.innerHTML = `
      <div class="cert-header">
        <img src="${cert.Image}" alt="${cert.Issuer}" class="cert-logo">
        <span class="cert-tag">${cert.Category}</span>
      </div>
      <span class="cert-date">${cert.Date}</span>
      <h3 class="cert-title">${cert.Title}</h3>
      <p class="cert-issuer">${cert.Issuer}</p>
      <p class="cert-desc">${cert.Description || ""}</p>
      <a href="${cert.Link}" target="_blank" class="cert-btn">View Certificate</a>
    `;
    box.appendChild(card);
  });

  numCards = document.querySelectorAll(".cert-card").length;
  rotationStep = 360 / numCards;
  arrangeCards();
}

function arrangeCards() {
  const cards = document.querySelectorAll(".cert-card");
  cards.forEach((card, i) => {
    let cardAngle = i * rotationStep;
    card.style.transform = `rotateY(${cardAngle}deg) translateZ(600px)`;
  });
  document.getElementById("certificates-box").style.transform = `rotateY(${angle}deg)`;
}

// Navigation
document.addEventListener("DOMContentLoaded", () => {
  loadCertificates();

  document.querySelector(".next").addEventListener("click", () => {
    angle -= rotationStep;
    arrangeCards();
  });

  document.querySelector(".prev").addEventListener("click", () => {
    angle += rotationStep;
    arrangeCards();
  });

  // Filter bar logic
  document.querySelectorAll(".filter-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      renderCertificates(btn.dataset.category);
    });
  });
});
let certificatesData = [];

function loadCertificates() {
  Papa.parse("certificates_full_with_desc.csv", {
    download: true,
    header: true,
    complete: function(results) {
      certificatesData = results.data.filter(c => c.Title);
      updateCounts();
      renderCertificates("All");
    }
  });
}

function updateCounts() {
  const total = certificatesData.length;
  const coding = certificatesData.filter(c => c.Category === "Coding").length;
  const leadership = certificatesData.filter(c => c.Category === "Leadership").length;

  document.querySelector('.filter-btn[data-category="All"] .badge').textContent = total;
  document.querySelector('.filter-btn[data-category="Coding"] .badge').textContent = coding;
  document.querySelector('.filter-btn[data-category="Leadership"] .badge').textContent = leadership;
}

function renderCertificates(category) {
  const box = document.getElementById("certificates-box");
  box.innerHTML = "";
  angle = 0; 

  const filtered = category === "All"
    ? certificatesData
    : certificatesData.filter(c => c.Category === category);

  filtered.forEach(cert => {
    const card = document.createElement("div");
    card.className = "cert-card";
    card.innerHTML = `
      <div class="cert-header">
        <img src="${cert.Image}" alt="${cert.Issuer}" class="cert-logo">
        <span class="cert-tag">${cert.Category}</span>
      </div>
      <span class="cert-date">${cert.Date}</span>
      <h3 class="cert-title">${cert.Title}</h3>
      <p class="cert-issuer">${cert.Issuer}</p>
      <p class="cert-desc">${cert.Description || ""}</p>
      <a href="${cert.Link}" target="_blank" class="cert-btn">View Certificate</a>
    `;
    box.appendChild(card);
  });

  numCards = document.querySelectorAll(".cert-card").length;
  rotationStep = 360 / numCards;
  arrangeCards();
}
