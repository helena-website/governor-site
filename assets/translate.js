/* Language picker. Same machine translation as today's governor.ri.gov (Google Translate,
   which GTranslate wraps), behind our own accessible <select> that defaults to English.
   Choosing a language sets Google's "googtrans" cookie and reloads; English clears it. */
(function () {
  "use strict";
  var sel = document.getElementById("lang-select");
  if (!sel) return;
  var m = document.cookie.match(/(?:^|;\s*)googtrans=\/en\/([^;]+)/);
  var current = m ? decodeURIComponent(m[1]) : "en";
  sel.value = current;
  if (!sel.value) sel.value = "en";

  function setCookie(val) {
    var host = location.hostname;
    var exp = val ? "" : "; expires=Thu, 01 Jan 1970 00:00:00 GMT";
    var v = val ? "/en/" + val : "";
    document.cookie = "googtrans=" + v + "; path=/" + exp;
    document.cookie = "googtrans=" + v + "; path=/; domain=" + host + exp;
    var parts = host.split(".");
    if (parts.length > 2) document.cookie = "googtrans=" + v + "; path=/; domain=." + parts.slice(-2).join(".") + exp;
  }

  sel.addEventListener("change", function () {
    setCookie(sel.value === "en" ? "" : sel.value);
    location.reload();
  });

  if (current !== "en") {
    window.googleTranslateElementInit = function () {
      new google.translate.TranslateElement({ pageLanguage: "en", autoDisplay: false }, "google_translate_element");
    };
    var s = document.createElement("script");
    s.src = "https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit";
    document.head.appendChild(s);
  }
})();
