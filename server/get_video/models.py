from django.db import models
# Create your models here.

import torch
import cv2
import numpy as np
from itertools import combinations, combinations_with_replacement
from collections import deque, Counter

from .apps import GetVideoConfig

colors    = GetVideoConfig.colors
big_value = GetVideoConfig.big_value
tail_size = GetVideoConfig.tail_size
tail      = GetVideoConfig.tail

frame = GetVideoConfig.frame
empty_frame = GetVideoConfig.empty_frame

#frame = {}
#frame['boxes']   = torch.FloatTensor([])             
#frame['ids']     = []         
#empty_frame = frame.copy()

for i in range(tail_size):
    tail.append(frame)

def draw_boxes(image, boxes):
    boxes_len = boxes.shape[0]
    if boxes_len>0: 
        for i in range(boxes_len):
            person_id = int(boxes[i][5])
            color = colors[int(str(person_id)[-1])]
            # извлекаем координаты ограничивающего прямоугольника
            x1, y1 = int(boxes[i][0].item()), int(boxes[i][1].item())
            x2, y2 = int(boxes[i][2].item()), int(boxes[i][3].item())
            # рисуем прямоугольник ограничивающей рамки
            image = cv2.rectangle(image, (x1, y1), (x2, y2),
                          color=color, thickness=2)                
    return image
#=========================================================================    
def boxes_processing(image, boxes, tail, person_id):
    tail_filling = sum([len(xx['ids']) for xx in tail])
    
    if tail_filling != 0 and len(boxes) != 0:        
        # Загрузка и распаковка содержания окна текущего кадра            
        all_tail_ids    = np.concatenate([x['ids'] for x in tail]).astype('int')
        unique_tail_ids = list(set(all_tail_ids))
        all_tail_ids    = list(all_tail_ids)        
        
        all_tail_boxes  = torch.cat([x['boxes']  for x in tail])             
 
        # Группировка boxes по значениям person_id
        persons_tail_boxes = []
        tmp = torch.cat([all_tail_boxes], 1)         
        for person in unique_tail_ids:
            x = tmp[tmp[:, 5] == person]
            b = x[:,0:6].clone()
            persons_tail_boxes.append(b) 
     
        # Сортировка объектов на текущем кадре по возрастанию X1 координады бокса
        boxes = boxes[boxes[:, 0].argsort()]    

        # Вычисление мер сходства боксов: расстояние                  
        dist_list = []      
        ids_dist_list = []       
        for i, box in enumerate(boxes):
            # Расстояния от новых объектов на текущем кадре до
            # идентифицированных объектов в окне tail                
            xx = (box[0] + box[2])/2.
            yy =  box[3]
            ww = box[2] - box[0]
            hh = box[3] - box[1]

            dists = []
            for k in range(len(persons_tail_boxes)):
                # Расстояния от новых объектов на текущем кадре до последнего из
                # совокупности идентифицированных объектов в окне для каждого person_id
                bb = persons_tail_boxes[k]
                bb = bb[-1,:]
                x = (bb[0] + bb[2])/2.
                y =  bb[3]
                w = box[2] - box[0]
                h = box[3] - box[1]                
                person = bb[5]
                dist = abs(xx-x)/(ww+w) + abs(yy-y)/(hh+h)
                dists.append(dist.item())                     

            # Идентификация новых объектов на текущем кадре по мере Min расстояния
            dist_min_value = min(dists)
            dist_min_index = dists.index(dist_min_value)                               
            dist_list.append(dist_min_value)

            boxes5_dist = unique_tail_ids[dist_min_index]
            ids_dist_list.append(int(boxes5_dist))

        for i, box in enumerate(boxes):
            box[5] = ids_dist_list[i]

        ids_list = ids_dist_list
        sim_list = dist_list
        # Анализ дублирования person_id'
        counter = Counter(ids_list)
        rep_id_list = [item for item, count in counter.items() if count > 1]  
        if len(rep_id_list) > 0:                  
            
            for r in rep_id_list:
                dup_id_index = [x[0] for x in enumerate(ids_list) if x[1] == r]
                dup_sims = []
                
                for w in dup_id_index:
                    dup_sims.append(sim_list[w])               

                sim_min_value = min(dup_sims)
                sim_min_index = dup_sims.index(sim_min_value)
           
                for i in dup_id_index:
                    if i != dup_id_index[sim_min_index]:
                        person_id += 1
                        boxes[i][5] = person_id
                        ids_list[i] = person_id
                        sim_list[i] = big_value
        else:
#            print('No duplication of person_id')               
            pass            
#----------------------------------------------------------------------------------
        frame = {}
        frame['boxes']   = boxes        
        frame['ids']     = ids_list # список person_id, уникальных для данного кадра       
        
        tail.popleft()
        tail.append(frame)              
#-------------------------------------------------------------         
    else:
        if tail_filling == 0 and len(boxes)!= 0:
            boxes = boxes[boxes[:, 1].argsort()] 
            # Идентификация объектов текущего кадра с случае пустого окна
            new_ids_list = []
            img_list = []
            
            # Составление батча изображений текущего кадра                       
            for i, box in enumerate(boxes):
                person_id += 1
                box[5] = person_id
                new_ids_list.append(person_id)
                x1 = int(box[0].item())
                x2 = int(box[2].item())
                y1 = int(box[1].item())
                y2 = int(box[3].item())
                w  = x2 - x1
                h  = y2 - y1
        
            frame = {}
            frame['boxes']   = boxes             
            frame['ids']     = new_ids_list         
            
            tail.popleft()
            tail.append(frame)            
            
        else:
            frame = empty_frame
            tail.popleft()
            tail.append(frame) 

    return frame, boxes, tail, person_id















