window.onload =  function(){
    mode = localStorage.getItem('mode');
    if(mode == null){
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            localStorage.setItem('mode', 'dark');
          } else {
            localStorage.setItem('mode', 'light');
          }
    }
    mode = localStorage.getItem('mode');
    if(mode == 'dark'){
        changeTheme('dark');
        document.getElementById("darkmode-toggle").checked = true;
    }
    else{
        changeTheme('light');
    }
};


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
    console.log(theme)
    if(theme=='dark'){
        document.getElementById("moon").setAttribute("fill","black");
        document.getElementById('sun').setAttribute("fill","yellow");
    }
    else{
        document.getElementById("moon").setAttribute("fill","currentColor");
        document.getElementById("sun").setAttribute("fill","currentColor");
    }
}

