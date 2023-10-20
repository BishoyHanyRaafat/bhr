const projectTitle = document.getElementById('project-title');
const projectContent = document.getElementById('project-content');
const messageInput = document.getElementById('message-input');
const fileInput = document.getElementById('file-input-div');
const submitButton = document.getElementById('submit-button');
const projectIdInput = document.getElementById('project-id');
const imagePreview = document.getElementById('image-preview');
const imageUrl = document.getElementById('image-url');
const projectPredictions = document.getElementById('project-predictions');
var loadFile = function(event) {  
    try{
        imagePreview.style.display = 'block';
        imagePreview.src = URL.createObjectURL(event.target.files[0]);
        messageInput.style.height = "70px"
        messageInput.setAttribute('placeholder', ' ');
        fileInput.style.display = 'none';
        submitButton.style.display = 'inline';
        imageUrl.value = imagePreview.src
    }
    catch{
        imagePreview.style.display = 'none';
        messageInput.setAttribute('placeholder', 'Enter a prompt here (Used in some demo models)');
    }
    messageInput.onload = function() {
      URL.revokeObjectURL(output.src) // free memory
    }
  };
window.onload = function(project_id) {
    var reloading = sessionStorage.getItem("reloading");
    var project_id = sessionStorage.getItem("project_id");
    if (reloading) {
        sessionStorage.removeItem("reloading");
        loadProject(project_id);
        sessionStorage.removeItem('project_id');
        projectPredictions.innerHTML = '';
    }
}
    
function reloadP(project_id) {
    sessionStorage.setItem("reloading", "true");
    sessionStorage.setItem("project_id", project_id);
    
    document.location.reload();
}
function reloadPage(project_id){
    if(project_id == projectIdInput.value){
        return;
    }
    reloadP(project_id);
}
function loadProject(project_id) {
fetch(`/core/projects/${project_id}`)
    .then(response => response.json())
    .then(data => {
        if(data.demo == false){
            fetchAndDisplayImages(project_id);
        }
        
        document.getElementById('file-input').value = null
        messageInput.setAttribute('placeholder', 'Enter a prompt here (Used in some demo models)');
        messageInput.style.height = "40px"
        imagePreview.style.display = 'none';
        projectTitle.innerHTML = `${data.title}`;
        projectContent.innerHTML = data.description;
        projectIdInput.value = data.project_id;
        if (data.demo) {
            messageInput.style.display = 'inline'
            if (data.chat){
                messageInput.removeAttribute('readonly');
            }
            else {
                messageInput.setAttribute('readonly', 'readonly');
            }
            fileInput.style.display = 'inline';
            submitButton.style.display = 'none';
            messageInput.value = '';
        }
        else{
            messageInput.setAttribute('readonly', 'readonly');
            fileInput.style.display = 'none';
            submitButton.style.display = 'none';
            messageInput.style.display='none';
        }
    });
}


// Add an event listener to the input field
messageInput.addEventListener('input', function() {
    if (messageInput.value.trim() !== '') {
        // If there is content in the input field, hide the file input and show the submit button
        fileInput.style.display = 'none';
        submitButton.style.display = 'inline';
    } else {
        // If the input is empty, show the file input and hide the submit button
        fileInput.style.display = 'inline';
        submitButton.style.display = 'none';
    }
});


// Function to fetch and display images from a Django endpoint
function fetchAndDisplayImages(projectId) {
    fetch(`/core/projects/images/${projectId}`)
    .then(response => response.json())
    .then(data => {
        document.getElementById('project-images').innerHTML = '';
        document.getElementById('project-predictions').display = "block";
        var aligment = 'end';
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
            imageElement.className = `rounded float-${aligment}`;
            divElement.appendChild(imageElement);
            document.getElementById('project-images').appendChild(divElement);
            
        }
  })};
  