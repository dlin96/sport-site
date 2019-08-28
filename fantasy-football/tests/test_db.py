import unittest
import pickle
import mongodb_ops


class DBTest(unittest.TestCase):
    def test_connection(self):
        _db, _connection = mongodb_ops._connect_db()
        self.assertIsNotNone(_connection.list_database_names())
        self.assertIsNotNone(_connection)
        self.assertIsNotNone(_db)

    def test_insert_db(self):
        with open("ravens_2018.pkl", "rb") as ravens_dc:
            dc = pickle.load(ravens_dc)
        mongodb_ops.insert_dc("ravens", dc)

        _db, _ = mongodb_ops._connect_db()
        self.assertIsNotNone(_db["ravens"])

