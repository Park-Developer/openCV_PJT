from multiprocessing import Queue
def put_ir_angle(shared_que:Queue,angle_data:int)->None:
    if (shared_que.full()==True):
        # Error 처리ㅏ
        print("queue is full")
    else:
        print("ffffffffffffffffffffffffffffffffffffffffffffff")
        shared_que.put(angle_data)

def get_ir_angle(shared_que:Queue):
    is_empty=False
    
    if (shared_que.empty()==True):
        # Error 처리
        is_empty=True
        print("queue is empth")
        return is_empty,0;
    else:
        return is_empty, shared_que.get()
