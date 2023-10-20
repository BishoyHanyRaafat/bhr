from django import forms

class ImageUploadForm(forms.Form):
    image_url = forms.CharField(widget=forms.HiddenInput(attrs={
        "id":"image-url",
        "name":"image_url",
        "value" : "",
    }))
    project_id = forms.CharField(widget=forms.HiddenInput(attrs={
        "name":"project_id",
        "value" : "",
        "id" : "project-id"
    }))
    image = forms.FileField(widget=forms.FileInput(attrs={
        "name":"file",
        "id":"file-input",
        "accept":".jpg,.jpeg,.png,.webp",
        "style":"display: none;",
        "onchange":"loadFile(event)"
    }))