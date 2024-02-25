#!/usr/bin/python
import mysql.connector
from models.state import State
from models.engine.db_storage import DBStorage


storage = DBStorage()
storage.reload()


def test_get_id():
    conn = mysql.connector.connect(host='localhost',
                            user='hbnb_test',
                            password='hbnb_test_pwd',
                            db='hbnb_test_db')
    cursor = conn.cursor()
    state_id = "0e391e25-dd3a-45f4-bce3-4d1dea83f3c7"
    query = ("SELECT * FROM states WHERE id = %s")
    cursor.execute(query, (state_id,))

    for name in cursor:
        print(name[len(name) - 1])
    result = storage.get(State, state_id)
    print("\n\n")
    print(result.name)
    # self.assertEqual(result, expected)
    cursor.close()
    conn.close()


if __name__ == "__main__":
    test_get_id()
