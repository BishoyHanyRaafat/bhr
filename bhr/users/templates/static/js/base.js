window.onload = function(){
    mode = localStorage.getItem('mode');
    if(mode == null){
        localStorage.setItem(mode, "light");
        changeTheme('light');
    }
    if(mode == 'dark'){
        changeTheme('dark');
        document.getElementById("darkmode-toggle").checked = true;
    }
    else{
        changeTheme('light');
    }
}


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


function changeMode(){
    if(localStorage.getItem('mode') == 'light'){
        localStorage.setItem('mode', 'dark');
        changeTheme('dark');
    }
    else{
        localStorage.setItem('mode', 'light');
        changeTheme('light');
    }
}
function changeTheme(theme){
    document.body.setAttribute("data-bs-theme", theme);
    document.getElementById("card-profile").setAttribute("data-bs-theme", theme);
    if(theme=='dark'){
        document.getElementById("moon").setAttribute("fill","black");
    }
    else{
        document.getElementById("moon").setAttribute("fill","currentColor");
    }
}

document.getElementById("darkmode-toggle").addEventListener('change', changeMode)
