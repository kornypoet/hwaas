# Hello World as a Service

## Requirements

In order to run the subsequent commands, you will need the following dependencies:

* Virtualbox (tested with version 5.1.22)

* Vagrant (tested with version 1.9.5)

* Ruby (tested with version 2.3.0)

## Preparation

The code uses three different virtual machines to mimic a production setup and deploy.

Bring up the Redis machine first:

```
vagrant up redis
```

All of the vm's use an Ubuntu Xenial base box; if you don't have it, this will download it for you.

Once the Redis machine is up bring up the worker vm and then the client vm:

```
vagrant up worker
vagrant up client
```

## Testing

Once the vm's have been started, you can run the infrastructure tests to confirm they have been provisioned correctly:

```
bundle install
bundle exec rake spec:all
```

(This will start each vm if it is not currently running)

## Usage

Log into the client vm:

```
vagrant ssh client
```

A command, `hwaaa` will have been installed:

```
client $ hwaas --help
usage: hwaas [-h] [-c CONFIG] [-m MESSAGE] [-r] [-f] [-s] [-v] WORKERS CLIENTS

Hello World as a Service

positional arguments:
  WORKERS               number of workers to start
  CLIENTS               number of clients to start

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        configuration file
  -m MESSAGE, --message MESSAGE
                        message to print
  -r, --remote          run workers and clients in vms
  -f, --foreground      run in foreground
  -s, --single          run in single process
  -v, --version         show program's version number and exit
```

You can start client and worker processes in several different ways. Having both clients and workes running inside one process is good for debugging (and is the default):

```
client $ hwaas 1 1
INFO - MainProcess: Starting 1 workers
INFO - MainProcess: Starting 1 clients
INFO - Worker-0: Started at 1496115945.18
INFO - Worker-0: RQ worker u'rq:worker:client.9070' started, version 0.8.0
INFO - Worker-0: Cleaning registries for queue: hwaas
INFO - Worker-0: 
INFO - Worker-0: *** Listening on hwaas...
INFO - Client-0: Started at 1496115945.18
INFO - Client-0: Submitted job 8a03eff9-a20d-46fa-95ae-0bdebb350c6d
INFO - Worker-0: hwaas: hwaas.task.hello_world('hello world') (8a03eff9-a20d-46fa-95ae-0bdebb350c6d)
hello world
INFO - Worker-0: hwaas: Job OK (8a03eff9-a20d-46fa-95ae-0bdebb350c6d)
INFO - Worker-0: Result is kept for 30 seconds
INFO - Worker-0: 
INFO - Worker-0: *** Listening on hwaas...
INFO - Client-0: Submitted job 0ec49c4c-064b-41f4-b2a5-432df7d4941b
INFO - Worker-0: hwaas: hwaas.task.hello_world('hello world') (0ec49c4c-064b-41f4-b2a5-432df7d4941b)
hello world
```

You can change the value of the message that is printed:

```
client $ hwaas 1 1 --message 'howdy partner'
INFO - MainProcess: Starting 1 workers
INFO - MainProcess: Starting 1 clients
INFO - Worker-0: Started at 1496116016.46
INFO - Worker-0: RQ worker u'rq:worker:client.9079' started, version 0.8.0
INFO - Worker-0: Cleaning registries for queue: hwaas
INFO - Worker-0: 
INFO - Worker-0: *** Listening on hwaas...
INFO - Client-0: Started at 1496116016.46
INFO - Worker-0: hwaas: hwaas.task.hello_world('howdy partner') (2dc0e92c-97e9-41a9-bd7f-d4446add49b3)
INFO - Client-0: Submitted job 2dc0e92c-97e9-41a9-bd7f-d4446add49b3
howdy partner
```

Once you are ready to bring up more substantial numbers of workers, use the `--remote` option (only for workers):

```
client $ hwaas 25 0 --remote
INFO - MainProcess: Using twiddler 1.0
INFO - MainProcess: Clearing out old processes and restarting supervisor
INFO - MainProcess: Starting 25 workers
INFO - MainProcess: Result: True
```

This will start 25 workers on the worker vm, managed by supervisor.

```
vagrant ssh worker
worker $ sudo supervisorctl status
hwaas:worker-000                 RUNNING   pid 9921, uptime 0:01:02
hwaas:worker-001                 RUNNING   pid 9920, uptime 0:01:02
hwaas:worker-002                 RUNNING   pid 9919, uptime 0:01:02
hwaas:worker-003                 RUNNING   pid 9918, uptime 0:01:02
hwaas:worker-004                 RUNNING   pid 9925, uptime 0:01:02
hwaas:worker-005                 RUNNING   pid 9924, uptime 0:01:02
hwaas:worker-006                 RUNNING   pid 9923, uptime 0:01:02
hwaas:worker-007                 RUNNING   pid 9922, uptime 0:01:02
hwaas:worker-008                 RUNNING   pid 9917, uptime 0:01:02
hwaas:worker-009                 RUNNING   pid 9916, uptime 0:01:02
hwaas:worker-010                 RUNNING   pid 9910, uptime 0:01:02
hwaas:worker-011                 RUNNING   pid 9911, uptime 0:01:02
hwaas:worker-012                 RUNNING   pid 9912, uptime 0:01:02
hwaas:worker-013                 RUNNING   pid 9913, uptime 0:01:02
hwaas:worker-014                 RUNNING   pid 9906, uptime 0:01:02
hwaas:worker-015                 RUNNING   pid 9907, uptime 0:01:02
hwaas:worker-016                 RUNNING   pid 9908, uptime 0:01:02
hwaas:worker-017                 RUNNING   pid 9909, uptime 0:01:02
hwaas:worker-018                 RUNNING   pid 9914, uptime 0:01:02
hwaas:worker-019                 RUNNING   pid 9915, uptime 0:01:02
hwaas:worker-020                 RUNNING   pid 9927, uptime 0:01:02
hwaas:worker-021                 RUNNING   pid 9926, uptime 0:01:02
hwaas:worker-022                 RUNNING   pid 9929, uptime 0:01:02
hwaas:worker-023                 RUNNING   pid 9928, uptime 0:01:02
hwaas:worker-024                 RUNNING   pid 9930, uptime 0:01:02

worker $ tail -f /var/log/hwaas/worker.log
INFO - worker-004: *** Listening on hwaas...
INFO - worker-024: RQ worker u'rq:worker:worker.9930' started, version 0.8.0
INFO - worker-024: Cleaning registries for queue: hwaas
INFO - worker-024: 
INFO - worker-024: *** Listening on hwaas...
INFO - worker-020: Started at 1496116151.43
INFO - worker-020: RQ worker u'rq:worker:worker.9927' started, version 0.8.0
INFO - worker-020: Cleaning registries for queue: hwaas
INFO - worker-020: 
INFO - worker-020: *** Listening on hwaas...
```


