from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import tensorflow as tf
import os
from keras.preprocessing import image
from PIL import Image
import numpy as np
from .models import Project, ProjectImage,Certificate
from .forms import ImageUploadForm
import io
# Create your views here.


def projects(request):
    prediction = ''
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.cleaned_data['image']
            image_bytes = uploaded_image.read()
            image_io = io.BytesIO(image_bytes)
            try:
                model = tf.keras.models.load_model(
                    os.path.join('projects', 'models', f'{request.POST["project_id"]}.h5')
                )
                target_size = [(150,150),(256, 256)][int(request.POST["project_id"])-1]
                img = image.load_img(image_io, target_size=target_size)
                # Rest of your image processing code here
            except Exception as e:
                return HttpResponse(f"Error processing image: {str(e)}")
            img = image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            img = img/255
            prediction = model.predict(img)
            project_prediction = [["Dog","Cat"],["Upset","Glad"]][int(request.POST["project_id"])-1]
            prediction = [project_prediction[0] if prediction[0][0] > 0.5 else project_prediction[1]][0]
    form = ImageUploadForm()
    projects = Project.objects.all()
    try:
        project_id = request.POST["project_id"]
        image_url = request.POST["image_url"]
    except:
        image_url = ''
        project_id = ''
    return render(request, 'projects.html',{'projects':projects,
                                            'form':form,
                                            "prediction":{"project_id": project_id,
                                                        "prediction":prediction,
                                                        "image_url":image_url}})

def return_project(_, project_id):
    project = Project.objects.filter(project_id=project_id).first()
    return JsonResponse({'project_id':project_id,'title':project.title,'description':project.description,"demo":project.demo,"chat":project.chat})

def return_images(_, project_id):
    project_images = ProjectImage.objects.filter(project_id=project_id)
    images = []
    for project_image in project_images:
        images.append(project_image.image.url)
    return JsonResponse({"images":images})

def return_certificates(_, certificate_id):
    certificate = Certificate.objects.filter(certificate_id=certificate_id).first()
    return JsonResponse({'title':certificate.title,'image':certificate.image.url})

def certificates(request):
    certificate = Certificate.objects.values("certificate_id","title")
    return render(request, 'certificates.html',{"certificates":certificate})