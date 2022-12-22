from django.shortcuts import render
from .forms import VideoForm
from .models import Video
import os
from datetime import timedelta
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
    # print(path)
    video = cv2.VideoCapture(path)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    fps = video.get(cv2.CAP_PROP_FPS)
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    threshold = 20.

    writer = cv2.VideoWriter('final.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 25, (width, height))
    ret, frame1 = video.read()
    prev_frame = frame1

    a = 0
    b = 0
    c = 0

    config_file="/home/rohit/Desktop/cctv/CCTV-FOOTAGE-Summarization-main/summarize/config/frozen_inference_graph.pb"
    forzen_model="/home/rohit/Desktop/cctv/CCTV-FOOTAGE-Summarization-main/summarize/config/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
    model=cv2.dnn_DetectionModel(config_file,forzen_model)
    classLabels=[]
    file_name='/home/rohit/Desktop/cctv/CCTV-FOOTAGE-Summarization-main/summarize/config/labels.txt'
    with open(file_name,'rt') as fpt:
        classLabels=fpt.read().rstrip('\n').split('\n')

    model.setInputSize(320,320)
    model.setInputScale(1.0/127.5)
    model.setInputMean((127.5,127.5,127.5))
    model.setInputSwapRB(True)
    timeStamps={}
    count=0
    object_detected=0
    while True:
        ret, frame = video.read()
        if ret is True:
            count+=1
            if (((np.sum(np.absolute(frame-prev_frame))/np.size(frame)) > threshold)):
                ClassIndex,confidence,bbox=model.detect(frame,confThreshold=0.5)
                if len(ClassIndex)>0:
                    unique=set()
                    for classInd,conf,boxes  in zip(ClassIndex.flatten(),confidence.flatten(),bbox):
                        if(classInd<=80):
                            object_detected+=1
                            unique.add( classLabels[classInd-1])
                    if(len(unique)>0):
                        td=timedelta(seconds=count//fps)
                        # print(str(td))
                        timeStamps[str(td)]=unique
                            
                writer.write(frame)
                prev_frame = frame
                a += 1
            else:
                prev_frame = frame
                b += 1
            c += 1
        else:
            break
    video.release()
    writer.release()
    cv2.destroyAllWindows()
    context={'path':"/media/"+str(Video.objects.all().last().video),'frames':c,'timeStamps':timeStamps,'timevalue':timeStamps.values(),'object_detected':object_detected,'t_time':str(timedelta(seconds=count//fps)),'processed_time':timedelta(seconds=a//fps)}
   
    return render(request,'DashBoard.html',{'context':context})

def access(request):
    return render(request,'access.html')

def previous(request):
    video=Video.objects.all()
    return render(request,'previous.html',{'video':video})

def setting(request):
    return render(request,'setting.html')
