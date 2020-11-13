from django.db import models
import uuid

# Create your models here.

class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)

class Photo(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True) 
    photo = models.ImageField()
    label = models.CharField(max_length=30)