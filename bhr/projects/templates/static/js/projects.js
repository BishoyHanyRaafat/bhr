const projectTitle = document.getElementById('project-title');
const projectContent = document.getElementById('project-content');

document.addEventListener('DOMContentLoaded', function() {
    console.log('Window loaded');
    var reloading = sessionStorage.getItem("reloading");
    var project_id = sessionStorage.getItem("project_id");
    if (reloading) {
        sessionStorage.removeItem("reloading");
        loadProject(project_id);
        console.log(project_id);
        sessionStorage.removeItem('project_id');
    }
})
function reloadPage(project_id){
    sessionStorage.setItem("reloading", "true");
    sessionStorage.setItem("project_id", project_id);
    document.location.reload();
}
function loadProject(project_id) {
fetch(`/core/projects/${project_id}`)
    .then(response => response.json())
    .then(data => {
        if(data.demo == false){
            fetchAndDisplayImages(project_id);
        }
        else{
            divElement = document.getElementById('div-warning');
            divElement.innerHTML = `<b class="text-danger">Demo is no longer available in this version due to the lack of memory</b>`;  
        }
        projectTitle.innerHTML = data.title;
        projectContent.innerHTML = data.description;
    });
}


// Function to fetch and display images from a Django endpoint
function fetchAndDisplayImages(projectId) {
    fetch(`/core/projects/images/${projectId}`)
    .then(response => response.json())
    .then(data => {
        document.getElementById('project-images').innerHTML = '';
        var aligment = 'end';
        if (data.images.length > 1){
            for (let i = 0; i < data.images.length; i++) {
                if(aligment == 'start'){
                    aligment = 'end';
                }
                else{
                    aligment = 'start';
                    var divElement = document.createElement('div');
                    divElement.className= 'row';
                }
                const imageElement = document.createElement('img');
                imageElement.src = data.images[i];
                imageElement.style.width = '300px';
                imageElement.className = `rounded-4 float-${aligment} border border-2 border-black m-1`;
                divElement.appendChild(imageElement);
                document.getElementById('project-images').appendChild(divElement); } 
        }else{
            const imageElement = document.createElement('img');
            imageElement.src = data.images[0];
            imageElement.style.width = '100%';
            imageElement.className = `rounded-4 border border-2 border-black m-1`;
            document.getElementById('project-images').appendChild(imageElement); 
        }
            
        }
  )};
  