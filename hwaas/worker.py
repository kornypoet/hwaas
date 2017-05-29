import logging
from redis import Redis
import rq
import time

class Worker():
    def __init__(self, queue='hwaas', redis_host='localhost'):
        self.queue = queue
        self.redis_host = redis_host
        self.logger = logging.getLogger(__name__)

    def run(self):
        self.logger.info('Started at %s', time.time())
        with rq.Connection(Redis(self.redis_host)):
            rq_worker = rq.Worker([self.queue])
            rq_worker.work()
