import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(name)s: %(message)s')
logger = logging.getLogger(__name__)

from .worker import Worker
from .client import Client
from .version import __version__

def main():
    parser = argparse.ArgumentParser(description='Hello World as a Service')
    parser.add_argument('workers', metavar='WORKERS', type=int, help='number of workers to start')
    parser.add_argument('clients', metavar='CLIENTS', type=int, help='number of clients to start')
    parser.add_argument('-v', '--version', action='version', version=__version__)
    args = parser.parse_args()

    logger.info('Starting %s workers', args.workers)
    for i in range(args.workers):
        worker = Worker(queue='hwaas')
        worker.start()

    logger.info('Starting %s clients', args.clients)
    for i in range(args.clients):
        client = Client(queue='hwaas', message='hello world')
        client.start()
