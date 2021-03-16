#!/usr/bin/env python3
import threading
import time
import logging
import random
import queue as Queue
from utils import LogIt

logger = LogIt(logger_name="queue",logging_level='DEBUG',filename='queue.log',to_log=True)

BUF_SIZE = 0
q = Queue.Queue(BUF_SIZE)

class ProducerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ProducerThread,self).__init__()
        self.target = target
        self.name = name

    def run(self):
        while True:
            item = 0
            if not q.full():
                item = item + 1
                q.put(item)
                logger.log('Putting ' + str(item) + ' : ' + str(q.qsize()) + ' items in queue')
                time.sleep(1.0)
        return

class ConsumerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ConsumerThread,self).__init__()
        self.target = target
        self.name = name
        return

    def run(self):
        while True:
            if not q.empty():
                item = q.get()
                logger.log('Getting ' + str(item)  + ' : ' + str(q.qsize()) + ' items in queue')
                time.sleep(4.0)
        return

if __name__ == '__main__':
    
    p = ProducerThread(name='producer')
    c = ConsumerThread(name='consumer')

    p.start()
    c.start()

