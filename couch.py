from datetime import datetime
from couchdb import Server
from settings import COUCHDB, SERVER_ID


class Couch:
    def __init__(self, server=COUCHDB['SERVER'], database=COUCHDB['DATABASE'], server_id=SERVER_ID):
        self.server = Server(server)
        self.database_name = database
        self.server_id = server_id
        self.database = self.server[database]

    @property
    def db(self):
        return self.database

    def __getitem__(self, key):
        return self.db[key]

    def save(self, entity):
        if 'created' not in entity:
            entity['created'] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        entity['server'] = self.server_id
        entity['updated'] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        return self.db.save(entity)