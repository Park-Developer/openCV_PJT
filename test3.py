from queue import Queue
import queue_handler

# Initializing a queue
q = Queue(maxsize = 3)

queue_handler.put_ir_angle(q,12)

print(queue_handler.get_ir_angle(q))