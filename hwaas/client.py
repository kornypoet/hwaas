import logging
from multiprocessing import Process
from redis import Redis
from rq import Queue
import time

from .task import hello_world

class Client(Process):
    def __init__(self, queue='hwaas', message='hello world'):
        super(Client, self).__init__()
        self.queue = Queue(queue, connection=Redis())
        self.message = message
        self.logger = logging.getLogger(self.name)

    def run(self):
        self.logger.info('Started at %s', time.time())
        while True:
            self.queue.enqueue(hello_world, self.message)
            time.sleep(1)
