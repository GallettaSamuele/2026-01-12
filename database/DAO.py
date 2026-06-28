from database.DB_connect import DBConnect
from model.Constructor import Constructor


class DAO:

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct(year(r.`date`)) as anno
                from races r
                order by r.date asc
                """
        cursor.execute(query)
        results = []
        for row in cursor:
            results.append(row["anno"])
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllConstructor():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
                select *
                from constructors c 
                """
        cursor.execute(query)
        results = []
        for row in cursor:
            results.append(Constructor(row["constructorId"], row["constructorRef"], row["name"], row["nationality"], row["url"]))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getNodiGrafo(anno1, anno2):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary = True)
        query = """
                select distinct(r.constructorId)
                from results r , races rs
                where r.raceId = rs.raceId and year(rs.`date`) between %s and %s and r.position is not null
                order by r.constructorId asc
                """
        cursor.execute(query, (anno1, anno2))
        results = []
        for row in cursor:
            results.append(row["constructorId"])
        cnx.close()
        cursor.close()
        return results

    @staticmethod
    def getArchiGrafo( anno1, anno2):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """
                SELECT 
                    r.constructorId AS costruttore1, 
                    r2.constructorId AS costruttore2, 
                    COUNT(distinct(r.driverId)) AS peso
                FROM results r
                JOIN races rs ON r.raceId = rs.raceId
                JOIN results r2 ON r.driverId = r2.driverId
                JOIN races rs2 ON r2.raceId = rs2.raceId
                WHERE r.constructorId < r2.constructorId  
                  AND YEAR(rs.`date`) BETWEEN %s AND %s
                  AND YEAR(rs2.`date`) BETWEEN %s AND %s
                  and r.`position` is not null 
                  and r2.`position` is not null
                  and r.constructorId in (select distinct(r.constructorId)
                                         from results r , races rs
                                         where r.raceId = rs.raceId and year(rs.`date`) between %s and %s and r.position is not null
                                         order by r.constructorId asc)	
                GROUP BY 
                    r.constructorId, 
                    r2.constructorId
                having peso >= 1
                ORDER by peso desc
                """
        cursor.execute(query, (anno1, anno2, anno1, anno2, anno1, anno2))
        results = []
        for row in cursor:
            results.append((row["costruttore1"], row["costruttore2"], row["peso"]))
        cnx.close()
        cursor.close()
        return results

    @staticmethod
    def getMaxAgeConstructor():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """
                select r.constructorId , min(d.dob) as età
                from results r
                join drivers d on r.driverId = d.driverId 
                group by r.constructorId
                order by r.constructorId asc
                """
        cursor.execute(query)
        results = []
        for row in cursor:
            results.append((row["constructorId"], row["età"]))
        cnx.close()
        cursor.close()
        return results
