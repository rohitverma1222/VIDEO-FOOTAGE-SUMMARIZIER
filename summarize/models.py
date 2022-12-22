from django.db import models
import datetime

# Create your models here.
class Video(models.Model):
    name=models.CharField(max_length=100)
    video=models.FileField(upload_to='videos')
    created=models.DateTimeField(auto_now_add=True)
