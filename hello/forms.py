from django import forms
from .models import Photo

# Create the form class.
class ImageForm(forms.Form):  
    photo = forms.ImageField()