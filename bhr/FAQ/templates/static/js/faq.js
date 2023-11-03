link_element = document.getElementById("faq-link")
link_element.className += " active";
link_element.setAttribute("aria-current", "page");

function getQuestion(question_id) {
    // Get the current URL
    var currentURL = window.location.href;
    // Check if the current URL already has a query string
    if (currentURL.indexOf('?') === -1) {
        // If there is no query string, add the query parameter with a "?" delimiter
        var newURL = currentURL + `?q=${question_id}`;
    } else {
        // If there is a query string, add the query parameter with an "&" delimiter
        var newURL = currentURL.split('?')[0] + `?q=${question_id}`;
    }

    // Redirect the user to the new URL
    window.location.href = newURL;
}