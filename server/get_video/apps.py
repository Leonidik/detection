from django.apps import AppConfig

import torch
import numpy as np
from collections import deque

class GetVideoConfig(AppConfig):
    name = 'get_video'
    
    model_dir  = 'yolov5'
    model_name = 'yolov5x'    
    model = torch.hub.load(repo_or_dir=model_dir, model=model_name, source='local')
    model.eval()   
    model.conf = 0.25    # NMS confidence threshold
    model.iou  = 0.45    # NMS IoU threshold
    model.classes = [0]  # persons only
    model.max_det = 25   # maximum number of detections per image
    model.agnostic    = False  # NMS class-agnostic
    model.multi_label = False  # NMS multiple labels per box
    model.amp         = False  # Automatic Mixed Precision (AMP) inference
    print('model.conf:', model.conf)
    print('model.iou :', model.iou)
          
    colors = {}
    colors[0] = (255,  0,  0)  # red
    colors[1] = (  0,  0,255)  # blue
    colors[2] = (255,255,  0)  # yellow
    colors[3] = (  0,255,  0)  # green
    colors[4] = (255,165,  0)  # orange
    colors[5] = (147,112,219)  # mediumpurple
    colors[6] = (204, 50,153)  # violet red
    colors[7] = (  0,191,255)  # deep sky blue
    colors[8] = (  0,  0,  0)  # black
    colors[9] = (255,255,255)  # white

    print('======= начальная инициализация в apps.py')
    tail_size  = 7   # Размер tracking window (8 => один разрыв)
    tail = deque()
    big_value  = 1.e25
    
    frame = {}
    frame['boxes']   = torch.FloatTensor([])             
    frame['ids']     = []
    empty_frame = frame.copy()
    
    for i in range(tail_size):
        tail.append(frame)

    print('-------------------------------------')

    snowboard_count = 4828 + 1  #frame_count + 1
    road_count      = 1165 + 1
    person_count    =  340 + 1
    diving_count    =  609 + 1
 


    
