// JavaScript to show and hide the loader when clicking on external links
document.addEventListener("DOMContentLoaded", function() {
  var loader = document.getElementById("loader");
  var spinner = new Spinner().spin(loader);

  var externalLinks = document.querySelectorAll('a[href^="http"]:not([href*="' + window.location.hostname + '"])');
  externalLinks.forEach(function(link) {
    link.addEventListener("click", function(event) {
      event.preventDefault();
      loader.style.display = "block";
      spinner.spin(loader);
      setTimeout(function() {
        window.location.href = link.href;
      }, 500);
    });
  });

  window.addEventListener("load", function() {
    spinner.stop();
    loader.style.display = "none";
  });
});