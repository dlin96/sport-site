import pymongo
import yaml
import logging

"""
TODO: this file should only return a connection obj. 
It's up to individual scripts as to what to do with the connection.
"""

# logging config
FORMAT = "%(asctime)-15s : %(message)s"
logging.basicConfig(format=FORMAT)
db_logger = logging.getLogger("db_logger")


def connect_db():
    with open("mongoconf.yaml", "r") as conf:
        mongodb_conf = yaml.load(conf, Loader=yaml.SafeLoader)
        ip_addr = mongodb_conf["ip_addr"]
        username = mongodb_conf["username"]
        password = mongodb_conf["password"]
        port = mongodb_conf["port"]

        _connection = pymongo.MongoClient(ip_addr,
                                          port,
                                          username=username,
                                          password=password,
                                          authSource="depth-chart"
                                          )

        _db = _connection["depth-chart"]
        return _db, _connection


