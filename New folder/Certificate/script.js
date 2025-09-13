// ----------------------
// THEME TOGGLE
// ----------------------
const toggleBtn = document.getElementById("theme-toggle");
const body = document.body;
const icon = toggleBtn.querySelector("i");

toggleBtn.addEventListener("click", () => {
  body.classList.toggle("dark-mode");
  body.classList.toggle("light-mode");

  if (body.classList.contains("dark-mode")) {
    icon.classList.remove("fa-moon");
    icon.classList.add("fa-sun");
  } else {
    icon.classList.remove("fa-sun");
    icon.classList.add("fa-moon");
  }
});

// ----------------------
// CERTIFICATES
// ----------------------
const CSV_CANDIDATES = [
  "certificates_full_with_desc.csv",
  "certificates_full.csv",
  "certificates.csv"
];

let angle = 0;
let numCards = 0;
let rotationStep = 0;
let radius = 500;

const box = document.getElementById("certificates-box");

// Utility: pick first non-empty from candidate keys
function pick(obj, keys) {
  for (const k of keys) {
    const v = obj?.[k];
    if (v && String(v).trim() !== "") return String(v).trim();
  }
  return "";
}

function filterNonEmpty(rows) {
  return rows.filter(r => Object.values(r).some(v => String(v || "").trim() !== ""));
}

// Build cards
function buildCards(rows) {
  box.innerHTML = "";
  rows.forEach((row) => {
    const title = pick(row, ["Title", "Name", "Certificate Title"]);
    const issuer = pick(row, ["Issuer", "Organization", "Provider", "Company"]);
    const date = pick(row, ["Date", "Issued", "Issue Date"]);
    const link = pick(row, ["Link", "URL", "Certificate URL"]);
    const desc = pick(row, ["Description", "Desc", "About"]);

    if (!title) return;

    const card = document.createElement("div");
    card.className = "cert-card";
    card.innerHTML = `
      <img src="award.svg" alt="Certificate Icon" class="cert-icon">
      <span class="cert-date"><i class="fa-regular fa-calendar"></i> ${date || ""}</span>
      <h3 class="cert-title">${title}</h3>
      <p class="cert-issuer">${issuer || ""}</p>
      <p class="cert-desc">${desc || ""}</p>
      ${link ? `<a href="${link}" target="_blank" class="cert-btn">View Certificate</a>` : `<span class="cert-btn" style="pointer-events:none;opacity:.6">No Link</span>`}
    `;
    box.appendChild(card);
  });

  numCards = document.querySelectorAll(".cert-card").length;

  if (numCards === 0) {
    const fallback = document.createElement("div");
    fallback.className = "cert-card";
    fallback.innerHTML = `
      <i class="fa-solid fa-triangle-exclamation cert-icon" style="color:#ffcc66"></i>
      <span class="cert-date"><i class="fa-regular fa-calendar"></i> — </span>
      <h3 class="cert-title">No certificates loaded</h3>
      <p class="cert-issuer">Check CSV filename & headers</p>
      <p class="cert-desc">Put <b>certificates_full.csv</b> in this folder & open with a local server.</p>
      <span class="cert-btn" style="pointer-events:none;opacity:.6">—</span>
    `;
    box.appendChild(fallback);
    numCards = 1;
  }

  // Desktop/tablet → carousel
  if (window.innerWidth >= 600) {
    rotationStep = 360 / numCards;
    computeRadius();
    arrangeCards();
  } else {
    // Mobile → stacked grid
    switchToGrid();
  }
}

const isMobile = () => window.matchMedia("(max-width: 600px)").matches;

function arrangeCards() {
  // Mobile: stacked cards, no transforms
  if (isMobile()) {
    box.style.transform = "none";
    document.querySelectorAll(".cert-card").forEach(card => {
      card.style.transform = "none";
    });
    return;
  }

  // Desktop/Tablet: 3D carousel
  const cards = document.querySelectorAll(".cert-card");
  cards.forEach((card, i) => {
    const cardAngle = i * rotationStep;
    card.style.transform = `rotateY(${cardAngle}deg) translateZ(${radius}px)`;
  });
  box.style.transform = `rotateY(${angle}deg)`;
}

function computeRadius() {
  const minR = 200;
  const maxR = 560;
  const w = Math.min(window.innerWidth, 1200);

  if (w < 600) {
    radius = 260;
  } else if (w < 900) {
    radius = 360;
  } else {
    radius = Math.max(minR, Math.min(maxR, Math.round(w * 0.35)));
  }
}

// Switch to grid layout for mobile
function switchToGrid() {
  const cards = document.querySelectorAll(".cert-card");
  box.style.transform = "none";
  box.style.display = "flex";
  box.style.flexDirection = "column";
  box.style.alignItems = "center";
  box.style.gap = "16px";

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1 }
  );

  cards.forEach((card) => {
    card.classList.remove("visible"); // reset
    observer.observe(card);
  });
}




// Load CSV
function loadCsv(path) {
  return new Promise((resolve, reject) => {
    Papa.parse(path, {
      download: true,
      header: true,
      complete: (res) => resolve(res),
      error: (err) => reject(err)
    });
  });
}

async function loadCertificates() {
  for (const candidate of CSV_CANDIDATES) {
    try {
      const res = await loadCsv(candidate);
      const rows = filterNonEmpty(res.data || []);
      if (rows.length) {
        console.log(`Loaded ${rows.length} rows from: ${candidate}`);
        buildCards(rows);
        return;
      }
    } catch (e) {
      console.warn(`Failed to load ${candidate}`, e);
    }
  }
  buildCards([]);
}

// ----------------------
// INIT
// ----------------------
document.addEventListener("DOMContentLoaded", () => {
  loadCertificates();

  if (window.innerWidth > 600) {  // Only bind for desktop/tablet
    document.querySelector(".next").addEventListener("click", () => {
      angle -= rotationStep;
      arrangeCards();
    });

    document.querySelector(".prev").addEventListener("click", () => {
      angle += rotationStep;
      arrangeCards();
    });
  }

  window.addEventListener("resize", () => {
    computeRadius();
    arrangeCards();
  });
});

