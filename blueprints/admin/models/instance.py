import os
from ConfigParser import RawConfigParser as ConfParser
import imp
from settings import INSTANCES_CONFIG_PATH
from ..utils import local_run


class Instance:
    def __init__(self, name):
        self.name = name
        self.__dns_names = None
        self.__process_count = None
        self.__export_timeout = None
        self.__status = None
        self.__db_settings = None
        self.__gunicorn_log_file = None
        self.__nginx_error_log_file = None
        self.__nginx_access_log_file = None

    @property
    def supervisor_file_name(self):
        return os.path.join(INSTANCES_CONFIG_PATH, self.name, 'supervisord.conf')

    @property
    def nginx_file_name(self):
        return os.path.join(INSTANCES_CONFIG_PATH, self.name, 'nginx.conf')

    @property
    def settings_file_name(self):
        return os.path.join(INSTANCES_CONFIG_PATH, self.name, 'settings.py')

    @property
    def folder(self):
        return os.path.join(INSTANCES_CONFIG_PATH, self.name)

    @property
    def db_settings(self):
        if not self.__db_settings:
            settings = imp.load_source('settings', self.settings_file_name)

            database = settings.DATABASES['default']['NAME']
            user = settings.DATABASES['default']['USER']
            password = settings.DATABASES['default']['PASSWORD']

            self.__db_settings = (database, user, password)
        return self.__db_settings

    @property
    def db_name(self):
        return self.db_settings[0]

    @property
    def db_user(self):
        return self.db_settings[1]

    @property
    def db_password(self):
        return self.db_settings[2]

    @property
    def status(self):
        if not self.__status:
            gunicorn_status = local_run("sudo supervisorctl status %s:%sGunicorn | awk '{print $2;}'" % (self.name, self.name))
            celery_status = local_run("sudo supervisorctl status %s:%sCelery | awk '{print $2;}'" % (self.name, self.name))

            ok = ["RUNNING", "STARTING", "STARTED"]
            self.__status = gunicorn_status in ok and celery_status in ok
        return self.__status

    @property
    def is_running(self):
        return self.status

    @property
    def export_timeout(self):
        if not self.__export_timeout:
            with open(self.nginx_file_name, 'r') as f:
                value = f.read()

                pattern = "proxy_connect_timeout"
                if not pattern in value:
                    return None
                start = value.find(pattern) + len(pattern)
                end = value.find(";", start)
                self.__export_timeout = int(value[start:end])
        return self.__export_timeout

    @property
    def process_count(self):
        if not self.__process_count:
            section = "program:{}Gunicorn".format(self.name)
            option = "command"

            p = ConfParser()
            p.read(self.supervisor_file_name)
            if p.has_section(section):
                value = p.get(section, option)
                pattern = " -w "
                if not pattern in value:
                    return None
                start = value.find(pattern) + len(pattern)
                end = value.find("-", start)
                self.__process_count = int(value[start:end])
        return self.__process_count

    @property
    def dns_names(self):
        if not self.__dns_names:
            with open(self.nginx_file_name, 'r') as f:
                value = f.read()

                pattern = "server_name"
                if not pattern in value:
                    return None
                start = value.find(pattern) + len(pattern)
                end = value.find(";", start)
                server_name = value[start:end].strip()
                dns = server_name.split(" ")
                #ignore nginx misc name
                if '""' in dns:
                    dns.remove('""')
                self.__dns_names = dns
        return self.__dns_names

    @property
    def dns_name(self):
        if self.dns_names and len(self.dns_names):
            return self.dns_names[0]
        return None

    @property
    def dns_aliases(self):
        if self.dns_names and len(self.dns_names) > 1:
            return self.dns_names[1:]
        return []

    @property
    def gunicorn_log_file(self):
        if not self.__gunicorn_log_file:
            section = "program:{}Gunicorn".format(self.name)
            option = "stdout_logfile"

            p = ConfParser()
            p.read(self.supervisor_file_name)
            if p.has_section(section):
                value = p.get(section, option)
                self.__gunicorn_log_file = value
        return self.__gunicorn_log_file

    @property
    def nginx_access_log_file(self):
        if not self.__nginx_access_log_file:
            with open(self.nginx_file_name, 'r') as f:
                value = f.read()

                pattern = "access_log"
                if not pattern in value:
                    return None
                start = value.find(pattern) + len(pattern)
                end = value.find(";", start)
                self.__nginx_access_log_file = value[start:end].strip()
        return self.__nginx_access_log_file

    @property
    def nginx_error_log_file(self):
        if not self.__nginx_error_log_file:
            with open(self.nginx_file_name, 'r') as f:
                value = f.read()

                pattern = "error_log"
                if not pattern in value:
                    return None
                start = value.find(pattern) + len(pattern)
                end = value.find(";", start)
                self.__nginx_error_log_file = value[start:end].strip()
        return self.__nginx_error_log_file

    @staticmethod
    def get_instances():
        basedir = os.path.abspath(INSTANCES_CONFIG_PATH)
        instance_folders = os.listdir(basedir)
        if 'common' in instance_folders:
            instance_folders.pop(instance_folders.index('common'))

        instances = []
        for folder in sorted(instance_folders):
            i = Instance(folder)
            instances.append(i)
        return instances

    @staticmethod
    def get_instance(host):
        for instance in Instance.get_instances():
            if host in instance.dns_names:
                return instance
        return None