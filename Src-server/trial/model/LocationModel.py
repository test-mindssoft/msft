from trial.model import getCursor
import trial.model as db

def getStates():
    try:
        conn = db.connect_db()
        cur = getCursor(conn)
        qry = "SELECT state_id, state_name from state"
        cur.execute(qry)
        result = cur.fetchall()
        return result
    except ValueError:
        print("Error getting States : ".format(ValueError))


def getDistricts():
    try:
        conn = db.connect_db()
        cur = getCursor(conn)
        qry = "SELECT district_id, district_name from district"
        cur.execute(qry)
        result = cur.fetchall()
        return result
    except ValueError:
        print("Error getting districts : ".format(ValueError))

def getProvinces():
    try:
        conn = db.connect_db()
        cur = getCursor(conn)
        qry = "SELECT province_id, province_name from province"
        cur.execute(qry)
        result = cur.fetchall()
        return result
    except ValueError:
        print("Error getting provinces : ".format(ValueError))

def getRegions():
    try:
        conn = db.connect_db()
        cur = getCursor(conn)
        qry = "SELECT region_id, region_name from region"
        cur.execute(qry)
        result = cur.fetchall()
        return result
    except ValueError:
        print("Error getting regions : ".format(ValueError))