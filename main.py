from multiprocessing import Process, Queue
import config
import vision_part
import communi_part



# 1. UDP Communication Check

is_udpOK=communi_part.check_udp(config.communi_config)
print("[debug] udp connect check",is_udpOK)

# 2. Multitasking Excution
try:
    if is_udpOK==True:
        shared_que=Queue(maxsize=config.queue_config["MAX_SIZE"])


        vision_task=Process(target=vision_part.run_cam, args=(config.vision_config,shared_que))
        communi_task=Process(target=communi_part.run_udp, args=(config.communi_config,shared_que))

        vision_task.start()
        communi_task.start()

        vision_task.join()
        communi_task.join()


except Exception as e:
    print("main Errr : " , e)
