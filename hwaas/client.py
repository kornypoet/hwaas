import logging
from redis import Redis
from rq import Queue
import time

from .task import hello_world

class Client():
    def __init__(self, queue='hwaas', redis_host='localhost', message='hello world'):
        self.queue = Queue(queue, connection=Redis(redis_host))
        self.message = message
        self.logger = logging.getLogger(__name__)

    def run(self):
        self.logger.info('Started at %s', time.time())
        try:
            while True:
                job = self.queue.enqueue_call(func=hello_world, args=(self.message,), result_ttl=30)
                self.logger.info('Submitted job %s', job.id)
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.warn('Shutting down')
