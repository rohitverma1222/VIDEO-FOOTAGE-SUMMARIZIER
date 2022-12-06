from django.shortcuts import render
from .forms import VideoForm
from .models import Video
import os
import cv2 # pip install opencv-python
import numpy as np # pip install numpy
# Create your views here.

def home(request):
    form =VideoForm()
    return render(request,'index.html',{'form':form})

def dashBoard(request):
    if request.method=='POST':
        form=VideoForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()

    # media path
    path=os.path.join('/home/rohit/Desktop/cctv/CCTV-FOOTAGE-Summarization-main/media/',str(Video.objects.all().last().video))
    print(path)
    video = cv2.VideoCapture(path)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    threshold = 20.

    writer = cv2.VideoWriter('final.avi', cv2.VideoWriter_fourcc(*'XVID'), 25, (width, height))
    ret, frame1 = video.read()
    prev_frame = frame1

    a = 0
    b = 0
    c = 0

    while True:
        ret, frame = video.read()
        if ret is True:
            if (((np.sum(np.absolute(frame-prev_frame))/np.size(frame)) > threshold)) and np.array_equal(prev_frame,frame)==False:
                writer.write(frame)
                prev_frame = frame
                a += 1
            else:
                prev_frame = frame
                b += 1
            c += 1
        else:
            break

    print("Total frames: ", c)
    print("Unique frames: ", a)
    print("Common frames: ", b)
    video.release()
    writer.release()
    cv2.destroyAllWindows()
    context={'path':"/media/"+str(Video.objects.all().last().video),'frames':c}
    return render(request,'DashBoard.html',{'context':context})

def access(request):
    return render(request,'access.html')

def previous(request):
    video=Video.objects.all()
    return render(request,'previous.html',{'video':video})

def setting(request):
    return render(request,'setting.html')
