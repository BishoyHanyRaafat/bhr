
document.getElementById("profile-link").addEventListener('click', appearCard)
function appearCard(){
    console.log(document.getElementById("profile-card").style.display)
    if(document.getElementById("profile-card").style.display == "block"){
        document.getElementById("profile-card").style.display = "none";
    }
    else{
        document.getElementById("profile-card").style.display = "block";
    }
    document.getElementById("profile-card").style.transition = "all 4s";
}