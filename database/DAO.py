from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct year (datetime) as year
                    from sighting 
                    order by year desc"""
            cursor.execute(query)

            for row in cursor:
                result.append(int(row["year"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllShapes(year: int):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct shape
                        from sighting 
                        where year(datetime)=%s and shape!=""
                        order by Shape"""
            cursor.execute(query, (year,))

            for row in cursor:
                result.append(row["shape"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllNodes(year, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select *
                    from sighting 
                    where year(datetime)=%s and shape=%s"""
            cursor.execute(query, (year, shape))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllEdges(idMapSighting, year, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s1.id as id1, s2.id as id2, (s2.longitude-s1.longitude) as peso
                    from sighting s1, sighting s2
                    where s1.state=s2.state
                    and s1.longitude<s2.longitude
                    and year(s1.datetime)=%s and s1.shape=%s
                    and year(s1.datetime)=year(s2.datetime) and s1.shape=s2.shape"""
            cursor.execute(query, (year, shape))

            for row in cursor:
                result.append((idMapSighting[row["id1"]], idMapSighting[row["id2"]],
                               float(row["peso"])))
            cursor.close()
            cnx.close()
        return result # sight, sight, peso_arco