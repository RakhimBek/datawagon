import sqlite3
from pydantic import BaseModel


class Station(BaseModel):
    id: int
    latitude: float
    longitude: float


class StationEdge(BaseModel):
    start: Station
    end: Station
    distance: float


def fetch_stations():
    connection = sqlite3.connect('sqll.db')
    try:
        cursor = connection.cursor()
        cursor.execute('''select ID, LATITUDE, LONGITUDE from STATIONS''')

        return cursor.fetchall()

    except Exception as e:
        print(e)
    finally:
        connection.close()


def fetch_stations_net():
    connection = sqlite3.connect('sqll.db')
    try:
        cursor = connection.cursor()
        cursor.execute('''select STARTID, ENDID, DISTANCE from STATIONS_NET''')
        return cursor.fetchall()

    except Exception as e:
        print(e)
    finally:
        connection.close()


def fetch_stations_net_with_positions():
    connection = sqlite3.connect('sqll.db')
    try:
        cursor = connection.cursor()
        cursor.execute('''
        select S1.ID AS LID,
               S1.LATITUDE AS LLATITUDE,
               S1.LONGITUDE AS LLONGITUDE,
               S2.ID AS RID,
               S2.LATITUDE AS RLATITUDE,
               S2.LONGITUDE AS RLONGITUDE,
               DISTANCE
        from STATIONS_NET
                 join STATIONS S1 on S1.ID = STATIONS_NET.STARTID
                 join STATIONS S2 on S2.ID = STATIONS_NET.ENDID
        ''')

        return cursor.fetchall()

    except Exception as e:
        print(e)
    finally:
        connection.close()


def wrap(fetched_data):
    edges = []
    for row in fetched_data:
        edges.append(StationEdge(
            start=Station(id=row[0], latitude=row[1], longitude=row[2]),
            end=Station(id=row[3], latitude=row[4], longitude=row[5]),
            distance=row[6]
        ))
    return edges
