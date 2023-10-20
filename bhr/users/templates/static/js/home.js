link_element = document.getElementById("home-link")
link_element.className += " active";
link_element.setAttribute("aria-current", "page");
console.log(document.getElementById("home-link").className);