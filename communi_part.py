import socket
import queue_handler
from multiprocessing import Queue

def check_udp(communi_config:dict)->bool:
    if (communi_config["COMMUNICATION_USE"]==True):
        is_udpOK=False # UDP 통신 접속 여부

        # UDP Connection Check
        for i in range(communi_config["CONNECT_TRY"]):
            camera_Sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            camera_Sock.bind(communi_config["IP_n_PORT"]["camera_client_ip"])
            camera_Sock.sendto(communi_config["MESSAGE"]["UDP_req_msg"].encode(),communi_config["IP_n_PORT"]["mainCon_server_ip"])


            received_data=camera_Sock.recv(communi_config["BUFFER_SIZE"])

            # debug
            print(received_data.decode('utf-8'),str(received_data.decode('utf-8'))==communi_config["MESSAGE"]["UDP_ack_msg"])

            if(str(received_data.decode('utf-8'))==communi_config["MESSAGE"]["UDP_ack_msg"]):
                is_udpOK=True
                break
    else:
        return True # Noy use udp, just return true

    return is_udpOK

def read_irangle(recv_data:bytes)->tuple:
    is_readOK=True # 정상 동작 여부
    ir_angle=0
    # 1. Decoding
    
    recv_data=recv_data.decode('utf-8')
    print("[debug]received_Data",recv_data)
    
    # 2. remove '\n'
    if "\n" in recv_data:
        recv_data=recv_data.replace('\n',"")
    
    # 3. Convert to Int
    if (recv_data.isdecimal()==True):
        ir_angle=int(recv_data)
        return is_readOK, ir_angle

        #queue_handler.put_ir_angle(shared_que,int(recv_data))
    else:
        #    print(recv_data,"conversion Error")
        #    print("err info : ")
        is_readOK=False

        return is_readOK,-999


def run_udp(communi_config:dict,shared_que:Queue)->int:
    '''
    Communicaton Sequence
    1. send req_msg
    2. recv ack_msg
    3. start udp communication(send->recv->send->recv)
    '''
    # UDP Setting
    if (communi_config["COMMUNICATION_USE"]==True):
        camera_Sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        camera_Sock.bind(communi_config["IP_n_PORT"]["camera_client_ip"])
    
    # UDP Run
    while communi_config["COMMUNICATION_USE"]:
        # Trans/Recv
        camera_Sock.sendto("Angle Req".encode(),communi_config["IP_n_PORT"]["mainCon_server_ip"])
        received_data=camera_Sock.recv(communi_config["BUFFER_SIZE"])

        is_readOK, ir_angle=read_irangle(received_data)

        # Queue Handling
        if (is_readOK==True):
            queue_handler.put_ir_angle(shared_que,ir_angle)
        else:
            print("conversion Error")

        # Cam End Condition
        if(received_data==communi_config["MESSAGE"]["stop_msg"]):
            return 0
   

              