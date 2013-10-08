from contextlib import contextmanager
from datetime import timedelta
import subprocess
import signal
import os
from os.path import expanduser
import sys
import errno
import fcntl


def local_run(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    while True:
        ret_code = p.poll()  # returns None while subprocess is running
        line = p.stdout.readline()
        yield line
        if ret_code is not None:
            break


def date_iter(low, high):
    current = low
    while current <= high:
        yield current
        current += timedelta(days=1)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


@contextmanager
def timeout(seconds):
    def timeout_handler(signum, frame):
        pass

    original_handler = signal.signal(signal.SIGALRM, timeout_handler)

    try:
        signal.alarm(seconds)
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, original_handler)


class LocalPgpass:
    def __init__(self, database, user, password, file_path=".pgpass"):
        self.database = database
        self.user = user
        self.password = password
        self.access_key_template = 'localhost:5432:{}:{}'
        self.file = file_path

    def __read_from_file(self, f):
        entries = {}
        while True:
            line = f.readline()
            if not len(line):
                break
            line = line.replace("\n", "")
            items = line.split(":")
            key = items[:-1]
            value = items[-1]
            entries[":".join(key)] = value
        return entries

    def __write_to_file(self, f, entries):
        for key in sorted(entries.keys()):
            password = entries.get(key)
            line = "{}:{}\n".format(key, password)
            f.write(line)

    def save(self):
        os.chdir(expanduser("~"))
        with timeout(15):
            with open(self.file, "rw+") as f:
                try:
                    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                    entries = self.__read_from_file(f)

                    #fixing instance entry
                    access_key = self.access_key_template.format(self.database,
                        self.user)
                    entries[access_key] = self.password

                    #fixing postgres:instance entry
                    pg_entry = self.access_key_template.format("postgres", "postgres")
                    if entries.has_key(pg_entry):
                        postgres_password = entries.get(pg_entry)

                        new_key = self.access_key_template.format(self.database, "postgres")
                        entries[new_key] = postgres_password
                    else:
                        print ".pgpass does not contain postgres:posgres record"
                        sys.exit(2)

                    f.seek(0)
                    f.truncate()

                    self.__write_to_file(f, entries)
                except IOError, e:
                    if e.errno != errno.EINTR:
                        raise e
                    print "Timeout while acquiring lock on .pgpass"
                    sys.exit(1)
