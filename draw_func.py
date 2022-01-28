import math
import cv2
def calc_IR_line(ir_angle:float, cam_info:dict)->list:
    
    # cam info setting
    line_len=cam_info['line_length']
    cam_width=cam_info['frame_width']
    cam_height=cam_info['frame_height']
    ir_angle_limit=cam_info['ir_angle_limit']

    # frame under center
    cam_origin=(int(cam_width/2),int(cam_height))
    
    # limit check
    if ir_angle<=ir_angle_limit:
        
        calced_X=(cam_width/2)+math.sin(math.radians(ir_angle))*line_len
        calced_Y=cam_height-math.cos(math.radians(ir_angle))*line_len
        
        calced_coord=(int(calced_X),int(calced_Y))

        ir_line_coord=[cam_origin,calced_coord]
    else:
        ir_line_coord=[cam_origin,cam_origin]

    return ir_line_coord
    
def draw_IR_line(cam_frame,ir_line_coord:list,ir_color,ir_thick)->None:
    
    cv2.line(cam_frame,ir_line_coord[0],ir_line_coord[1],ir_color,ir_thick)
    