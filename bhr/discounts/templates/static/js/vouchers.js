link_element = document.getElementById("vouchers-link")
link_element.className += " active";
link_element.setAttribute("aria-current", "page");
function showModal(){
    const modal = new bootstrap.Modal(document.getElementById('staticBackdrop'));
    modal.show();
}