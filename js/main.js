// ==========================================================================
// Merkaba Holdings: Site scripts
// Small bits of behavior for the page. The site still works if this fails.
// ==========================================================================

// 1. Mobile menu: open/close the nav when the hamburger button is tapped
const navToggle = document.querySelector(".nav-toggle");
const siteNav = document.querySelector(".site-nav");

function setMenuOpen(isOpen) {
  siteNav.classList.toggle("is-open", isOpen);
  navToggle.setAttribute("aria-expanded", String(isOpen));
  navToggle.setAttribute("aria-label", isOpen ? "Close menu" : "Open menu");
}

navToggle.addEventListener("click", function () {
  const isOpen = navToggle.getAttribute("aria-expanded") === "true";
  setMenuOpen(!isOpen);
});

// Close the menu after a link is tapped, so the page is visible again
siteNav.querySelectorAll("a").forEach(function (link) {
  link.addEventListener("click", function () {
    setMenuOpen(false);
  });
});

// 2. Footer year: keeps the copyright year current automatically
document.getElementById("year").textContent = new Date().getFullYear();
