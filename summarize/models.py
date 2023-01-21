from django.db import models
import datetime
from django.contrib.auth.models import User

# Create your models here.
class Video(models.Model):
    name=models.CharField(max_length=100)
    video=models.FileField(upload_to='videos')
    File_user=models.ForeignKey(User,on_delete=models.DO_NOTHING,blank=True)
    created=models.DateTimeField(auto_now_add=True)
