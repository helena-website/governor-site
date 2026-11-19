/* Mobile menu toggle. Without JavaScript the menu is always shown (see .no-js in site.css). */
(function () {
  "use strict";
  document.documentElement.classList.remove("no-js");
  var btn = document.querySelector(".menu-btn");
  var nav = document.getElementById("site-nav");
  if (!btn || !nav) return;
  btn.addEventListener("click", function () {
    var open = btn.getAttribute("aria-expanded") === "true";
    btn.setAttribute("aria-expanded", String(!open));
    nav.classList.toggle("open", !open);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && btn.getAttribute("aria-expanded") === "true") {
      btn.setAttribute("aria-expanded", "false");
      nav.classList.remove("open");
      btn.focus();
    }
  });
})();
