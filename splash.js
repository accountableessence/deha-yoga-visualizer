/* ============================================================
   DEHA — SPLASH SCREEN  (splash.js)
   Add as FIRST <script> in every page's <body>
   ============================================================ */

(function () {
  const splash = document.createElement('div');
  splash.id = 'deha-splash';

  // SVG traced from the Deha logo D lettermark:
  // - Outer D: large sweeping curve
  // - Inner figure: the woman silhouette inside the D
  // - Swoosh: the gold underline
  splash.innerHTML = `
    <div style="display:flex;align-items:center;">
      <img src="assets/splash-logo.png" class="splash-logo-img" alt="Deha" />
    </div>

    <div class="splash-line"></div>
    <div class="splash-tagline">move with intention</div>
  `;

  document.documentElement.appendChild(splash);

  // Hide after animations complete
  setTimeout(function () {
    splash.classList.add('hide');
    setTimeout(function () { splash.remove(); }, 750);
  }, 1800);
})();