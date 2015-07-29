import MySQLdb as mysql

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "123456"
MYSQL_DATABASE = "trial"

TABLES = {}

TABLES['employees'] = (
    "CREATE TABLE IF NOT EXISTS `employees` ("
    "  `emp_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `birth_date` date NOT NULL,"
    "  `first_name` varchar(14) NOT NULL,"
    "  `last_name` varchar(16) NOT NULL,"
    "  `gender` enum('M','F') NOT NULL,"
    "  `hire_date` date NOT NULL,"
    "  PRIMARY KEY (`emp_no`)"
    ") ENGINE=InnoDB")

TABLES['test'] = (
    "CREATE TABLE IF NOT EXISTS `test` ("
    "  `emp_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `birth_date` date NOT NULL,"
    "  `first_name` varchar(14) NOT NULL,"
    "  `last_name` varchar(16) NOT NULL,"
    "  `gender` enum('M','F') NOT NULL,"
    "  `hire_date` date NOT NULL,"
    "  PRIMARY KEY (`emp_no`)"
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