import logging
import rq
import time

class Worker():
    def __init__(self, queue='hwaas', name='name'):
        self.queue = queue
        self.logger = logging.getLogger(__name__)

    def run(self):
        self.logger.info('Started at %s', time.time())
        with rq.Connection():
            rq_worker = rq.Worker([self.queue])
            rq_worker.work()
