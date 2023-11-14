function setCookie(cookieName, cookieValue) {
    document.cookie = cookieName + "=" + cookieValue + ";path=/";
}
function getCookie(cookieName) {
    var name = cookieName + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var cookieArray = decodedCookie.split(';');

    for (var i = 0; i < cookieArray.length; i++) {
        var cookie = cookieArray[i].trim();
        if (cookie.indexOf(name) == 0) {
            return cookie.substring(name.length, cookie.length);
        }
    }

    // Return null if the cookie is not found
    return null;
}

window.onload =  function(){
    mode = getCookie('mode');
    if(mode != 'dark' && mode != 'light'){
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            setCookie('mode', 'dark');
            changeTheme('dark');
          } else {
            setCookie('mode', 'light');
            changeTheme('light');
          }
    }
    mode = getCookie('mode');
    if(mode == 'dark'){
        //changeTheme('dark');
        document.getElementById("moon").style.display = "block";
        document.getElementById('sun').style.display = "none";
    }
    //else{
        //changeTheme('light');
    //}
};


function changeMode(){
    if(getCookie('mode') == 'light'){
        setCookie('mode', 'dark');
        changeTheme('dark');
    }
    else{
        setCookie('mode', 'light');
        changeTheme('light');
    }
}
function changeTheme(theme){
    document.body.setAttribute("data-bs-theme", theme);
    console.log(theme)
    if(theme=='dark'){
        document.getElementById("moon").style.display = "block";
        document.getElementById('sun').style.display = "none";
    }
    else{
        document.getElementById("moon").style.display = "none";
        document.getElementById('sun').style.display = "block";
    }
}

