// main.js
// Handles two small pieces of interactivity:
// 1. Light/Dark theme toggle (persisted in localStorage so it
//    survives page reloads and navigating between pages)
// 2. Mobile hamburger menu toggle

document.addEventListener("DOMContentLoaded", () => {
    const root = document.documentElement;
    const themeToggleBtn = document.getElementById("themeToggle");
    const navToggleBtn = document.getElementById("navToggle");
    const navLinks = document.getElementById("navLinks");

    // --- THEME TOGGLE ---
    // On page load, check if the user previously chose a theme.
    const savedTheme = localStorage.getItem("theme") || "light";
    root.setAttribute("data-theme", savedTheme);
    updateThemeIcon(savedTheme);

    themeToggleBtn.addEventListener("click", () => {
        const current = root.getAttribute("data-theme");
        const next = current === "light" ? "dark" : "light";
        root.setAttribute("data-theme", next);
        localStorage.setItem("theme", next);
        updateThemeIcon(next);
    });

    function updateThemeIcon(theme) {
        themeToggleBtn.textContent = theme === "light" ? "🌙" : "☀️";
    }

    // --- MOBILE NAV TOGGLE ---
    navToggleBtn.addEventListener("click", () => {
        navLinks.classList.toggle("open");
    });
});
