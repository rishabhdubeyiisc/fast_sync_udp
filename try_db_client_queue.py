from cl_utils import *
import time
import threading

Q = Thread_safe_queue(to_log_queue=True)
cl = db_client_cls(IFDbname='PMU_31')

def consumer(Q : Thread_safe_queue):
    while True:
        x = Q.remove_from_queue()
        print(x)
        time.sleep(5)

def producer(cl : db_client_cls , Q : Thread_safe_queue ):
    while True:
        entry = cl.create_me_json(field_value=123)
        Q.put_in_queue(entry)
        time.sleep(2.5)

producer_TH = threading.Thread(target=producer , args=(cl , Q , ))
consumer_TH = threading.Thread(target=consumer , args=(Q , ))

producer_TH.start()
consumer_TH.start()