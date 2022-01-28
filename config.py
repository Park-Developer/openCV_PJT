import numpy as np

'''
Vision Configuration
'''
vision_config={
    "VISION_USE":True, 
    "DEBUG_MODE":True,
    "OBJECT_DETECTION":True,
    # [1] Robot Body Setting
    "ROBOT":{
        "body_size":np.array([[0,480],[40,400],[600,400],[640,480]]),

    },

    # [2] Camera Setting
    "CAMERA":{
        'camera_index':0, # User Setting
        'line_length':400, # Unit : Frameasdasd
        'ir_angle_limit':50, # Unit : degree
        'ir_color':(255,0,0),
        'ir_thickness':10,
    },

    # [3] 
}

'''
Communication Configuration
'''
communi_config={
    "COMMUNICATION_USE":False, 
    "DEBUG_MODE":True,
    
    "CONNECT_TRY":3,
    "BUFFER_SIZE":1024,
    "IP_n_PORT":{
        "camera_client_ip":('169.254.42.20',8080), # Ethernet Camera IP
        "mainCon_server_ip":('169.254.42.23',8080),   # Ethernet Main Controller IP
    },

    "MESSAGE":{
        "UDP_req_msg":"Camera Connection OK",
        "UDP_ack_msg":"UDP Connection OK",
        "angle req":"angle req",
        "stop_msg":"STOP UDP",

    }
}

'''
Queue Configuration
'''
queue_config={
    "MAX_SIZE":2000,
    
}