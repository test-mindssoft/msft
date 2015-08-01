import MySQLdb as mysql

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "123456"
MYSQL_DATABASE = "msft"

__all__ = [
    "connect_db",
    "getCursor",
    "close_connection",
]

TABLES = {}

TABLES['taskactivity'] = (
    "CREATE TABLE IF NOT EXISTS `taskactivity` ("
    "  `taskid` int(11) NOT NULL AUTO_INCREMENT,"
    "  `activityname` varchar(45) NOT NULL,"
    "  `activitytype` varchar(45) NOT NULL,"
    "  `duration` varchar(45) NOT NULL,"
    "  `repeats` varchar(45) NOT NULL,"
    "  `authority` varchar(45) NOT NULL,"
    "  `slaprate` varchar(45) NOT NULL,"
    "  `penaltyrate` varchar(45) NOT NULL,"
    "  PRIMARY KEY (`taskid`)"
    ") ENGINE=InnoDB")

TABLES['state'] = (
    "CREATE TABLE IF NOT EXISTS `state` ("
    "  `state_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `state_name` varchar(45) NOT NULL,"
    "  PRIMARY KEY (`state_id`)"
    ") ENGINE=InnoDB")

TABLES['district'] = (
    "CREATE TABLE IF NOT EXISTS `district` ("
    "  `district_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `district_name` varchar(45) NOT NULL,"
    "  PRIMARY KEY (`district_id`)"
    ") ENGINE=InnoDB")

TABLES['province'] = (
    "CREATE TABLE IF NOT EXISTS `province` ("
    "  `province_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `province_name` varchar(45) NOT NULL,"
    "  PRIMARY KEY (`province_id`)"
    ") ENGINE=InnoDB")

TABLES['region'] = (
    "CREATE TABLE IF NOT EXISTS `region` ("
    "  `region_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `region_name` varchar(45) NOT NULL,"
    "  PRIMARY KEY (`region_id`)"
    ") ENGINE=InnoDB")


def connect():
	return  mysql.connect(
        MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD
    )

def connect_db():
    return  mysql.connect(
        MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, 
        MYSQL_DATABASE
    )

def getCursor(conn):
	return conn.cursor()

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(MYSQL_DATABASE))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

def create_tables(cur):
    for name, ddl in TABLES.iteritems():
        cur.execute(ddl)
        

def close_connection(cur, conn):
	cur.close()
	conn.close()

def initialize_db():
    try:
        conn = connect()
        cur = getCursor(conn)
        create_database(cur)
    except mysql.Error as err:
        if err[0] == 1049:
            print "hai"
        else:
            print(err)
            exit(1)
    conn = connect_db()
    cur = getCursor(conn)
    create_tables(cur)
    close_connection(cur, conn)