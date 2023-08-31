# get_video/views.py

from django.shortcuts import render

from django.views.decorators import gzip
from django.http import StreamingHttpResponse
from .apps import GetVideoConfig
from .models import *

import cv2
import os
import numpy as np
from time import sleep

model = GetVideoConfig.model
tail  = GetVideoConfig.tail

snowboard_count = GetVideoConfig.snowboard_count 
road_count      = GetVideoConfig.road_count
person_count    = GetVideoConfig.person_count
diving_count    = GetVideoConfig.diving_count

def select_video(request,  *args, **kwargs):
    host = request.META['HTTP_HOST']
    return render(request, 'get_video/select_video.html', locals())

def index(request, *args, **kwargs):
    host = request.META['HTTP_HOST']
    path = request.GET.get('path') 
    print('index.html path:', path)
    path_to_video = '@'
    path_to_X_map = '@'
    X_map_h = 0
       
    if  path == '1':
        path_to_video = 'media/get_video/snowboard.mp4'
    elif path == '11':
        path_to_X_map = 'media/get_video/snowboard_matrix.jpg'
        X_map_h = snowboard_count
    elif path == '2' :
        path_to_video = 'media/get_video/road.mp4'
    elif path == '22' :
        path_to_X_map = 'media/get_video/road_matrix.jpg'
        X_map_h = road_count       
    elif path == '3' :
        path_to_video = 'media/get_video/persons.mp4'        
    elif path == '33' :
        path_to_X_map = 'media/get_video/persons_matrix.jpg'
        X_map_h = person_count
    elif path == '4' :
        path_to_video = 'media/get_video/diving.mp4'
    elif path == '44' :
        path_to_X_map = 'media/get_video/diving_matrix.jpg'
        X_map_h = diving_count                    
    else:
        path_to_video = 'VVVVVVVV'
        path_to_X_map = 'XXXXXXXX'
    
    print('path_to_video:', path_to_video)
    print('path_to_X_map:', path_to_X_map)
    print('X_map_h      :', X_map_h)
    
    return render(request, 'get_video/index.html', locals())

def gen(cap,tail):
    frame_count = -1
    person_id   = -1
    while(cap.isOpened()):
        (ret, frame) = cap.read()
        if ret == True:
            frame_count += 1
            os.system('clear')
            print('frame_count:', frame_count)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)        
            results = model(image)
            boxes = results.xyxy[0].to('cpu')           
           
            frame, boxes, tail, person_id = boxes_processing(\
            image, boxes, tail, person_id)

            image = draw_boxes(image=image, boxes=boxes)
                                                                              
            _, jpeg = cv2.imencode('.jpg', image[:,:,::-1])
            frame = jpeg.tobytes()

            yield(b'--frameg\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')                     
 
#            if frame_count == 500:    # Ограничение числа кадров !!!!!
#                break

        else:
            print('End of video file')
            break

@gzip.gzip_page
def livefe(request, path_to_video):
    try:
        if path_to_video == '0': path_to_video = 0  
        cap = cv2.VideoCapture(path_to_video)                     
        stream = gen(cap,tail)         
        response = StreamingHttpResponse(stream, content_type="multipart/x-mixed-replace;boundary=frame")
        return response
    except:  # This is bad!
        print('This is bad!')
        pass


