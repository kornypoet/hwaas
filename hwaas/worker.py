import logging
from multiprocessing import Process
import rq
import time

rq_logger = logging.getLogger('rq.worker')
rq_logger.setLevel(logging.WARN)

class Worker(Process):
    def __init__(self, queue='hwaas'):
        super(Worker, self).__init__()
        self.queue = queue
        self.logger = logging.getLogger(self.name)

    def run(self):
        self.logger.info('Started at %s', time.time())
        with rq.Connection():
            rq_worker = rq.Worker([self.queue])
            rq_worker.work()
