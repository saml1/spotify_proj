import sqlite3
from sqlite3 import Error
import os

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print("Error: " + str(e))

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        return True
    except AttributeError as e:
        print('(For debugging): ' + str(e))
        return False


def create_db(conn, database):
    """
    Create a new db into the databases table
    :param conn:
    :param database:
    :return: db id
    """

    cur = conn.cursor()
    sql = ''' INSERT INTO databases (local, name)
              VALUES (?,?) '''
    cur.execute(sql, database)
    conn.commit()
    return cur.lastrowid


def create_song(conn, song):
    """
    Create a new song into the db
    :param conn:
    :param song:
    :return: project id
    """
    sql = ''' INSERT INTO songs(name, artist, album, duration, database_id)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, song)
    conn.commit()
    return cur.lastrowid


# given db file, prints list of all songs in both db1 (name) and db2 (name)
def get_dupes(d1, d2):
    conn = create_connection(os.getcwd() + '/libraries.db')
    try:
        cur = conn.cursor()
    except AttributeError:
        return
    cur.execute('''SELECT * FROM databases WHERE name=?''', (d1,))
    # d1_id is database_id of database with name d1 and d2_id for for d2
    d1_id = cur.fetchall()[0][0]
    cur.execute('''SELECT * FROM databases WHERE name=?''', (d2,))
    d2_id = cur.fetchall()[0][0]
    cur.execute('''SELECT * from songs WHERE database_id=?''', (d1_id,))
    d1_songs = cur.fetchall()
    cur.execute('''SELECT * from songs WHERE database_id=?''', (d2_id,))
    d2_songs = cur.fetchall()
    for song in d1_songs:
        cur = conn.cursor()
        # selecting matches (but allowing for 10-second difference in duration)
        cur.execute("SELECT * FROM songs "
                    "WHERE database_id=? AND name=? AND artist=? AND album=? AND duration BETWEEN ? and ?",
                    (d2_id, song[1],song[2], song[3], song[4] - 10, song[4] + 10))
        match = cur.fetchall()
        if len(match) > 0:
            print(match[0])


