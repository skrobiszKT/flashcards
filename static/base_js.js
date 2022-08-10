document.addEventListener("DOMContentLoaded", function () {
  const navbarEl = document.querySelectorAll("#navbar > ul > li");
  navbarEl.forEach(function (el) {
      el.className = "nav-item";
  })
});
