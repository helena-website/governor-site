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

/* Open/closed indicator for the Constituent Services phone line, using Eastern time.
   Hours: Monday to Friday, 8am to 5pm. State holidays are not handled yet. */
(function () {
  "use strict";
  var els = document.querySelectorAll(".open-status");
  if (!els.length || !window.Intl) return;
  var DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  function nowET() {
    var parts = new Intl.DateTimeFormat("en-US", { timeZone: "America/New_York", weekday: "short", hour: "numeric", minute: "numeric", hour12: false }).formatToParts(new Date());
    var o = {};
    parts.forEach(function (p) { o[p.type] = p.value; });
    var day = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].indexOf(o.weekday);
    return { day: day, mins: (parseInt(o.hour, 10) % 24) * 60 + parseInt(o.minute, 10) };
  }
  function update() {
    var t = nowET();
    els.forEach(function (el) {
      var open = parseInt(el.getAttribute("data-open"), 10) * 60, close = parseInt(el.getAttribute("data-close"), 10) * 60;
      var weekday = t.day >= 1 && t.day <= 5;
      var isOpen = weekday && t.mins >= open && t.mins < close;
      var msg;
      if (isOpen) msg = "Open now until 5pm";
      else {
        var next;
        if (weekday && t.mins < open) next = "today";
        else if (t.day >= 1 && t.day <= 4) next = "tomorrow";
        else next = "Monday";
        msg = "Closed now. We open " + next + " at 8am";
      }
      el.classList.toggle("is-open", isOpen);
      el.classList.toggle("is-closed", !isOpen);
      el.querySelector(".open-text").textContent = msg;
    });
  }
  update();
  setInterval(update, 60000);
})();
