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
        'frame_width':cap.get(cv2.CAP_PROP_FRAME_WIDTH),
        'frame_height':cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
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



    # Camera run
    if cap.isOpened():
        while True:
            #time.sleep(1)
            ret, frame=cap.read()
            
            if ret:
                # 오직 정수를 받아야하는 조건 추가하기!!!!!!!!!!!!!!1
                
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
                draw_func.draw_IR_line(frame,ir_lineCoord,ir_line_color,ir_line_thick)
                
                cv2.fillConvexPoly(frame,robot_body,(0,0,255)) # 외곽선 두께에 -1을 주면 내부가 색칳됨
                cv2.putText(frame,"asd",(600,40),cv2.FONT_HERSHEY_PLAIN,1,(0,0,0))


                cv2.imshow("Camera ",frame);
                if cv2.waitKey(1)!=-1:
                    return 0 # 정상 종료
            else:
                return -1                                                                                                                                                                                                                                                                                                                                                                                                                                                

    cap.release()
    cv2.destroyAllWindows()