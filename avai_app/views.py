import os

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Greeting, Photo
from .forms import ImageForm
from .image_labeler import detect_image_labels
from .playlist_recommender import recommend_playlist

from uuid import uuid4


def detect(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ImageForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            photo = Photo(photo=form["photo"].value())
            photo.save()
            
            filename = os.path.basename(photo.photo.name)
            s3_url = "https://{}.s3-{}.amazonaws.com/{}".format(
                settings.AWS_STORAGE_BUCKET_NAME,
                settings.AWS_S3_REGION_NAME,
                filename
            )
            labels = detect_image_labels(filename)
            recommended_playlist_id = recommend_playlist(labels)
            return render(
                request,
                "results.html",
                {
                    "detection_results":{
                        "playlist_id":recommended_playlist_id,
                        "image_url": s3_url,
                        "labels": labels
                    }
                }
            )
        else:
            return render(request, "index.html", {'form': form})

def index(request):
    form = ImageForm()
    return render(request, "index.html", {'form': form})