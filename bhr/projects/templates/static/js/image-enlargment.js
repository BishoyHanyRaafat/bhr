function enlargeImage(image_url){
    const modal = new bootstrap.Modal(document.getElementById('imageModal'));
    document.getElementById('image-preview').src = image_url;
    modal.show();
}