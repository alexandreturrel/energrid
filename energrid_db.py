#!/usr/bin/python

#########################################
#               ENERGRID_DB             #
#########################################


from __future__ import print_function
import mysql.connector as mariadb
from mysql.connector import errorcode


neighborhood_config = {
        'user': 'root',
        'password': 'raspberry',
        'host': '127.0.0.1',
        'database': 'Neighborhood'
}
houses_config = {
        'user': 'root',
        'password': 'raspberry',
        'host': '127.0.0.1',
        'database': 'House'
}
generation_config = {
        'user': 'root',
        'password': 'raspberry',
        'host': '127.0.0.1',
        'database': 'Generation'
}
consommation_config = {
        'user': 'root',
        'password': 'raspberry',
        'host': '127.0.0.1',
        'database': 'Consommation',
}

neighborhood_tables = {}

neighborhood_tables['Neighborhood'] = (
        "CREATE TABLE `Neighborhood` ("
        "`neighborhood_id` int(11) NOT NULL,"
        "`house_list` ,"
        ""
        )


def create_database(cursor, db_name):
    try:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
        print('{} database created.'.format(db_name))
    except mariadb.Error as err:
        print('Failed creating database {}'.format(err))
        exit(1)

n_cnx = mariadb.connect(**neighborhood_config)
n_cursor = n_cnx.cursor()
try:
    n_cursor.execute("USE {}".format(n_cnx.database))
except mariadb.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        print('Database {} does not exist. Creating...'.format(n_cnx.database))
        create_database(n_cursor, n_cnx.database)
    else:
        print(err)
else:
    n_cnx.close()

h_cnx = mariadb.connect(**houses_config)
h_cursor = h_cnx.cursor()
try:
    h_cursor.execute("USE {}".format(h_cnx.database))
except mariadb.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        print('Database Houses does not exist. Creating...')
        create_database(h_cursor, h_cnx.database)
    else:
        print(err)
else:
    h_cnx.close()

g_cnx = mariadb.connect(**generation_config)
g_cursor = g_cnx.cursor()
try:
    g_cursor.execute("USE {}".format(g_cnx.database))
except mariadb.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        print('Database Generators does not exist. Creating...')
        create_database(g_cursor, g_cnx.database)
    else:
        print(err)
else:
    g_cnx.close()

c_cnx = mariadb.connect(**consommation_config)
c_cursor = c_cnx.cursor()
try:
    c_cursor.execute("USE {}".format(c_cnx.database))
except mariadb.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        print('Database Consomators does not exist. Creating...')
        create_database(c_cursor, c_cnx.database)
    else:
        print(err)
else:
    c_cnx.close()


