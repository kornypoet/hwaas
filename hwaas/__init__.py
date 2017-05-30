import argparse
import logging
from multiprocessing import Process
import os
import sys
import time
import xmlrpclib
import yaml

if os.environ.get('SUPERVISOR_PROCESS_NAME'):
    format = '%(levelname)s - ' + os.environ.get('SUPERVISOR_PROCESS_NAME') + ': %(message)s'
else:
    format = '%(levelname)s - %(processName)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=format)
logger = logging.getLogger(__name__)

from .worker import Worker
from .client import Client
from .version import __version__

def main():
    parser = argparse.ArgumentParser(description='Hello World as a Service')
    parser.add_argument('workers', metavar='WORKERS', type=int, help='number of workers to start')
    parser.add_argument('clients', metavar='CLIENTS', type=int, help='number of clients to start')
    parser.add_argument('-c', '--config', type=argparse.FileType('r'), default='/etc/hwaas/config.yaml', help='configuration file')
    parser.add_argument('-m', '--message', default='hello world', help='message to print')
    parser.add_argument('-r', '--remote', action='store_true', default=False, help='run workers and clients in vms')
    parser.add_argument('-f', '--foreground', action='store_true', default=False,help='run in foreground')
    parser.add_argument('-s', '--single', action='store_true', default=True, help='run in single process')
    parser.add_argument('-v', '--version', action='version', version=__version__)
    args = parser.parse_args()

    with args.config as stream:
        config = yaml.load(stream)

    config['rq::message'] = args.message

    if args.foreground:
        run_in_foreground(args.workers, args.clients, config)
    elif args.remote:
        run_supervisor(args.workers, args.clients, config)
    elif args.single:
        run_in_single_process(args.workers, args.clients, config)

def construct_client(options):
    return Client(queue=options['rq::queue'], redis_host=options['redis::ip'], message=options['rq::message'])

def construct_worker(options):
    return Worker(queue=options['rq::queue'], redis_host=options['redis::ip'])

def run_in_single_process(num_workers, num_clients, options):
    processes = []
    try:
        logger.info('Starting %s workers', num_workers)
        for i in range(num_workers):
            worker = construct_worker(options)
            process = Process(target=worker.run, name='Worker-' + str(i))
            processes.append(process)
            process.start()

        logger.info('Starting %s clients', num_clients)
        for i in range(num_clients):
            client = construct_client(options)
            process = Process(target=client.run, name='Client-' + str(i))
            processes.append(process)
            process.start()

        for p in processes:
            p.join()
    except KeyboardInterrupt:
        logger.warn('Shutting down')

def run_in_foreground(num_workers, num_clients, options):
    if num_workers != 1 and num_clients != 1:
        logger.warn('Can only run either one client or one worker in the foreground at a time')
        sys.exit(1)
    if num_workers == 1:
        worker = construct_worker(options)
        worker.run()
    elif num_clients == 1:
        client = construct_client(options)
        client.run()

def run_supervisor(num_workers, num_clients, options):
    if num_clients > 0:
        logger.warn('Can only run workers remotely')
        sys.exit(1)
    if num_workers > 0:
        s = xmlrpclib.ServerProxy('http://' + options['worker::ip'] + ':9001')
        logger.info('Using twiddler %s', s.twiddler.getAPIVersion())
        logger.info('Clearing out old processes and restarting supervisor')
        s.supervisor.stopAllProcesses()
        s.supervisor.restart()
        time.sleep(3)
        logger.info('Starting %s workers', num_workers)
        result = s.twiddler.addProgramToGroup('hwaas', 'worker', {
            'command': 'hwaas 1 0 -f -c ' + options['hwaas::config_dir'] + '/config.yaml',
            'redirect_stderr': 'true',
            'stdout_logfile': options['hwaas::log_dir'] + '/worker.log',
            'numprocs': str(num_workers),
            'process_name': '%(program_name)s-%(process_num)03d'
        })
        logger.info('Result: %s', result)
