const certificateTitle = document.getElementById('certificate-title');
const certificateContent = document.getElementById('certificate-content');
const divImage = document.getElementById('div-image');


function loadCertificates(certificateId) {
    fetch(`/core/certificates/${certificateId}`)
        .then(response => response.json())
        .then(data => {
            certificateContent.innerHTML = '';
            var imageElement = document.createElement('img');
            const imageUrl = data.image;
            imageElement.onclick = function() {enlargeImage(imageUrl)};
            imageElement.src = imageUrl;
            imageElement.style.width = '100%';
            imageElement.className += `float-start border m-1`
            certificateTitle.innerHTML = data.title;
            certificateContent.appendChild(imageElement);
        }
    )
};
