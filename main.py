import cv2
import numpy as np
import socket
import draw_func

cap=cv2.VideoCapture(0)

print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Robot Body Setting
robot_body=np.array([[0,480],[40,400],[600,400],[640,480]])

# Camera Setting
camera_info={
'line_length':400, # Unit : Frame
'frame_width':cap.get(cv2.CAP_PROP_FRAME_WIDTH),
'frame_height':cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
'ir_angle_limit':50, # Unit : degree
}

ir_info={
    'color':(255,0,0),
    'thickness':10,
}

# UDP Communication(Client) Setting
clientSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
clientSock.bind(('127.0.0.1',8080))

received_data=clientSock.recv(1024)
ir_angle=int(received_data.decode('utf-8'))
clientSock.sendto("OK".encode(),('127.0.0.1',8080))
if cap.isOpened():
    while True:
        

        ret, frame=cap.read()
        
        if ret:
            ir_lineCoord= draw_func.calc_IR_line(ir_angle, camera_info)
            draw_func.draw_IR_line(frame,ir_lineCoord,ir_info)
            
            cv2.fillConvexPoly(frame,robot_body,(0,0,255)) # 외곽선 두께에 -1을 주면 내부가 색칳됨
            cv2.putText(frame,"asd",(600,40),cv2.FONT_HERSHEY_PLAIN,1,(0,0,0))
            cv2.imshow("Camera ",frame);
            if cv2.waitKey(1)!=-1:
                break
        else:
            break                                                                                                                                                                                                                                                                                                                                                                                                                                                

cap.release()
cv2.destroyAllWindows()
