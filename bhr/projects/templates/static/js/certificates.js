const certificateTitle = document.getElementById('certificate-title');
const certificateContent = document.getElementById('certificate-content');
const divImage = document.getElementById('div-image');


function loadCertificates(certificateId) {
    fetch(`/core/certificates/${certificateId}`)
        .then(response => response.json())
        .then(data => {
            certificateContent.innerHTML = '';
            divImage.className = 'col-6 ms-5 mt-5';
            var imageElement = document.createElement('img');
            imageElement.src = data.image;
            imageElement.style.width = '100%';
            imageElement.className += `float-start border m-1`
            certificateTitle.innerHTML = data.title;
            certificateContent.appendChild(imageElement);
        }
    )
};
