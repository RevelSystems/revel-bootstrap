from __future__ import division
import socket
from ..utils import local_run
import psutil
from .instance import Instance


class Server:
    name = None
    cpu_usage = None
    ram_free = None
    ram_used = None
    ram_total = None
    ram_usage = None
    hdd_free = None
    hdd_used = None
    hdd_total = None
    hdd_usage = None
    instance_count = None
    version = None

    @staticmethod
    def gatherInfo():
        server = Server()

        server.name = socket.gethostname()
        server.cpu_usage = psutil.cpu_percent()

        memory = psutil.virtual_memory()._asdict()
        server.ram_free = memory['free']
        server.ram_used = memory['used']
        server.ram_total = memory['total']
        server.ram_usage = memory['percent']

        disk_usage = psutil.disk_usage('/')._asdict()
        server.hdd_free = disk_usage['free']
        server.hdd_used = disk_usage['used']
        server.hdd_total = disk_usage['total']
        server.hdd_usage = disk_usage['percent']

        server.instance_count = len(Instance.get_instances())

        for line in local_run('git rev-parse --verify HEAD'):
            server.version = line.strip()
            break

        return server