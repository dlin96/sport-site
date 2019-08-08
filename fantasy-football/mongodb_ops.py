import pymongo
import yaml
import logging


# logging config
FORMAT = "%(asctime)-15s : %(message)s"
logging.basicConfig(format=FORMAT)
db_logger = logging.getLogger("db_logger")


def _connect_db():
    with open("mongoconf.yaml", "r") as conf:
        mongodb_conf = yaml.load(conf, Loader=yaml.SafeLoader)
        ip_addr = mongodb_conf["ip_addr"]
        username = mongodb_conf["username"]
        password = mongodb_conf["password"]
        port = mongodb_conf["port"]
        db_name = mongodb_conf["db_name"]

        _connection = pymongo.MongoClient(ip_addr,
                                          port,
                                          username=username,
                                          password=password,
                                          authSource="admin"
                                          )

        _db = _connection[db_name]
        return _db, _connection


def insert_dc(collection_name, depth_chart_bson):
    db_logger.info("collection: {}".format(collection_name))
    db_logger.info("dc_bson: {}".format(depth_chart_bson))
    _db, _connection = _connect_db()
    collection = _db[collection_name]
    collection.replace_one({"team_name": collection_name}, depth_chart_bson, upsert=True)
    _connection.close()
