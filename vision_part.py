from multiprocessing import Queue
import cv2
import numpy as np
import draw_func
import queue_handler
import time

# for obejct detection
import tensorflow_hub as hub
import tensorflow as tf
import pandas as pd

def run_cam(vision_config:dict,shared_que:Queue)->int:#,ir_que:Queue):
    # Initial Settting
    cap=cv2.VideoCapture(vision_config['CAMERA']['camera_index'])
    
    draw_setting={
        'line_length':vision_config["CAMERA"]['line_length'],
        'frame_width':int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'frame_height':int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        'ir_angle_limit':vision_config["CAMERA"]['ir_angle_limit'],
    }

    ir_line_color=vision_config["CAMERA"]['ir_color']
    ir_line_thick=vision_config["CAMERA"]['ir_thickness']

    robot_body=vision_config["ROBOT"]['body_size']
    # Vision 
    ir_angle=0
    cur_angle=0 # current IR angle value

    # Object Detection
    is_obj_detect=False
    if (vision_config['OBJECT_DETECTION']==True):
        is_obj_detec=True
        # Carregar modelos
        detector = hub.load("https://tfhub.dev/tensorflow/efficientdet/lite2/detection/1")
        labels = pd.read_csv('labels.csv',sep=';',index_col='ID')
        labels = labels['OBJECT (2017 REL.)']

    print(draw_setting['frame_width'] , draw_setting['frame_height'])
    # Camera run
    if cap.isOpened():
        while True:
            #time.sleep(1)
            ret, frame=cap.read()
            
            if ret:
                # 오직 정수를 받아야하는 조건 추가하기!!!!!!!!!!!!!!1
                
                # Image Conversion
                #1. Resize to respect the input_shape

                inp = cv2.resize(frame, (draw_setting['frame_width'] , draw_setting['frame_height']))

                #Convert img to RGB
                rgb = cv2.cvtColor(inp, cv2.COLOR_BGR2RGB)

                #Is optional but i recommend (float convertion and convert img to tensor image)
                rgb_tensor = tf.convert_to_tensor(rgb, dtype=tf.uint8)

                #Add dims to rgb_tensor
                rgb_tensor = tf.expand_dims(rgb_tensor , 0)
                
                boxes, scores, classes, num_detections = detector(rgb_tensor)
                
                pred_labels = classes.numpy().astype('int')[0]
                
                pred_labels = [labels[i] for i in pred_labels]
                pred_boxes = boxes.numpy()[0].astype('int')
                pred_scores = scores.numpy()[0]

                 #loop throughout the detections and place a box around it  
                for score, (ymin,xmin,ymax,xmax), label in zip(pred_scores, pred_boxes, pred_labels):
                    if score < 0.5:
                        continue
                        
                    score_txt = f'{100 * round(score,0)}'
                    img_boxes = cv2.rectangle(rgb,(xmin, ymax),(xmax, ymin),(0,255,0),1)      
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(img_boxes,label,(xmin, ymax-10), font, 0.5, (255,0,0), 1, cv2.LINE_AA)
                    cv2.putText(img_boxes,score_txt,(xmax, ymax-10), font, 0.5, (255,0,0), 1, cv2.LINE_AA)


                # IR Sensor Part
                is_Qempty, ir_angle=queue_handler.get_ir_angle(shared_que)
                if is_Qempty==True:
                    ir_angle=cur_angle # empty default : 0
                else:
                    cur_angle=ir_angle

                print("ir angle",ir_angle)
                if(str(type(ir_angle))=="<class 'int'>"):
                    print("debug pp ", ir_angle)
                else:
                    print("[debug1]",ir_angle)
                    print("[debug2]",int.from_bytes(ir_angle,byteorder='big'))

                ir_lineCoord= draw_func.calc_IR_line(ir_angle, draw_setting)
                draw_func.draw_IR_line(img_boxes,ir_lineCoord,ir_line_color,ir_line_thick)
                
                cv2.fillConvexPoly(img_boxes ,robot_body,(0,0,255)) # 외곽선 두께에 -1을 주면 내부가 색칳됨
                cv2.putText(img_boxes ,"Normal Mode",(600,40),cv2.FONT_HERSHEY_PLAIN,1,(0,0,0))


                cv2.imshow("Camera ",img_boxes)
                if cv2.waitKey(1)!=-1:
                    return 0 # 정상 종료
            else:
                return -1                                                                                                                                                                                                                                                                                                                                                                                                                                                

    cap.release()
    cv2.destroyAllWindows()