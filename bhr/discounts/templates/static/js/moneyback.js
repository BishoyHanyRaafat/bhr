function getToast(){
    var toast_id = `Toast-${Date.now()}`;
    toast =  `<div id="${toast_id}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="toast-header">
        <img src="/static/assets/logo_no_slag.png" width="40" class="rounded me-2" alt="Logo" />
        <strong class="me-auto">BHR</strong>
        <small>Just now</small>
        <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
        You can't get this voucher
        </div>
    </div>`
    return [toast_id, toast]
}
function showToast(){
    var children = Array.from(document.getElementById("toastContainer").children);
    children.forEach(element => {
        if (element.className == "toast fade hide"){
          element.remove();
        };
    })
    console.log(document.getElementById("toastContainer").childElementCount)
    if(document.getElementById("toastContainer").childElementCount > 3){
        return
    }
    [toast_id,toast] = getToast();
    document.getElementById("toastContainer").innerHTML += toast;
    var element = document.getElementById(toast_id);
    var myToast = new bootstrap.Toast(element);

    myToast.show();
}

function redirectVoucher(voucher,number){
    if(eval(number) <= 0){
        const modal = new bootstrap.Modal(document.getElementById('staticBackdrop'));
        redirectButton = document.getElementById("btn-modal-yes")
        modal.show();
        redirectButton.addEventListener("click", function() {
            const redirectToURL = `/discounts/vouchers/${voucher}`;
            modal.hide();
            setTimeout(function() {
              window.location.href = redirectToURL;
            }, 300); 
          });
        return
    }
    showToast();
}

