/* Mock form handling for the prototype. Validates required fields, shows an error summary
   linked to each field, then shows the confirmation panel. Nothing is sent anywhere. */
(function () {
  "use strict";
  function labelFor(el) {
    var group = el.closest("fieldset");
    if (group) return group.querySelector("legend").childNodes[0].textContent.trim();
    var l = document.querySelector('label[for="' + el.id + '"]');
    return l ? l.childNodes[0].textContent.trim() : el.name;
  }
  function clear(form) {
    form.querySelectorAll(".field-err").forEach(function (n) { n.remove(); });
    form.querySelectorAll("[aria-invalid]").forEach(function (n) {
      n.removeAttribute("aria-invalid");
      var d = (n.getAttribute("aria-describedby") || "").split(" ").filter(function (x) { return x && x.indexOf("-err") === -1; });
      if (d.length) n.setAttribute("aria-describedby", d.join(" ")); else n.removeAttribute("aria-describedby");
    });
  }
  function flag(el, msg, errors) {
    var id = (el.id || el.name) + "-err";
    var p = document.createElement("p");
    p.className = "field-err"; p.id = id; p.textContent = msg;
    var host = el.closest("fieldset") || el.parentNode;
    host.appendChild(p);
    var target = el.closest("fieldset") || el;
    target.setAttribute("aria-invalid", "true");
    var d = target.getAttribute("aria-describedby");
    target.setAttribute("aria-describedby", (d ? d + " " : "") + id);
    errors.push({ id: el.id || (el.closest("fieldset").querySelector("input").id), msg: msg, el: el });
  }
  document.querySelectorAll(".mock-form").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      clear(form);
      var errors = [];
      form.querySelectorAll("input[required], select[required], textarea[required]").forEach(function (el) {
        if (el.type === "radio") return;
        if (!el.value.trim()) flag(el, "Please answer: " + labelFor(el), errors);
        else if (el.type === "email" && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(el.value)) flag(el, "Enter an email address like name@example.com.", errors);
      });
      var seen = {};
      form.querySelectorAll('input[type=radio][required]').forEach(function (el) {
        if (seen[el.name]) return; seen[el.name] = true;
        if (!form.querySelector('input[name="' + el.name + '"]:checked')) flag(el, "Please choose: " + labelFor(el), errors);
      });
      form.querySelectorAll("fieldset[data-req-group]").forEach(function (fs) {
        if (!fs.querySelector("input:checked")) flag(fs.querySelector("input"), "Please choose at least one: " + labelFor(fs.querySelector("input")), errors);
      });
      var sum = form.querySelector(".err-summary");
      if (errors.length) {
        var items = errors.map(function (er, i) {
          var target = er.el.id ? er.el.id : "";
          return '<li><a href="#' + target + '">' + er.msg + "</a></li>";
        }).join("");
        sum.innerHTML = "<h3>Please fix " + (errors.length === 1 ? "1 problem" : errors.length + " problems") + "</h3><ul>" + items + "</ul>";
        sum.hidden = false;
        sum.focus();
        return;
      }
      sum.hidden = true;
      var done = document.getElementById(form.id + "-done");
      form.hidden = true;
      done.hidden = false;
      done.focus();
    });
  });
})();
