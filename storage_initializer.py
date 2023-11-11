import sqlite3

import pandas as pd


# todo: move to Redis or PostgreSQL someday ?

def init_sqllite_stations():
    """
Инициализация таблицы "Координаты станций."
    """
    connection = sqlite3.connect('sqll.db')
    try:
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS STATIONS (
            ID INTEGER PRIMARY KEY,
            LATITUDE REAL,
            LONGITUDE REAL
        )
        ''')

        cursor.execute('CREATE INDEX IF NOT EXISTS IDX_LATITUDE ON STATIONS (LATITUDE)')
        cursor.execute('CREATE INDEX IF NOT EXISTS IDX_LONGITUDE ON STATIONS (LONGITUDE)')

        # tood: to settings file
        stations_path = '~/Downloads/STATION_COORDS_HACKATON.xlsx'

        with pd.ExcelFile(stations_path) as xls:
            stations_df = pd.read_excel(xls, "Sheet 1")
            for index, row in stations_df.iterrows():
                station_id = row['ST_ID']  # ST_ID – станция ЖД сети
                latitude = row['LATITUDE']  # LATITUDE – широта
                longitude = row['LONGITUDE']  # LONGITUDE – долгота.

                if latitude != None and longitude != None:
                    cursor.execute('INSERT INTO STATIONS(ID, LATITUDE, LONGITUDE) VALUES (?, ?, ?)',
                                   (int(station_id), float(latitude), float(longitude)))

        connection.commit()
        connection.close()
    except Exception as e:
        print(e)
    finally:
        connection.close()


def init_sqllite_stations_net():
    """
Инициализация таблицы "Графы ж/д сети."
    """
    connection = sqlite3.connect('sqll.db')
    try:
        cursor = connection.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS STATIONS_NET (
            STARTID INTEGER,   --- START_CODE – станция начала ребра графа
            ENDID INTEGER,   --- END_CODE – станция окончания ребра графа
            DISTANCE REAL,   --- LEN – длительность ребра в км.
            PRIMARY KEY (STARTID, ENDID),
            FOREIGN KEY(STARTID) REFERENCES STATIONS(ID),
            FOREIGN KEY(ENDID) REFERENCES STATIONS(ID)
        )
        ''')

        # tood: to settings file
        stations_path = '~/Downloads/PEREGON_HACKATON.xlsx'

        with pd.ExcelFile(stations_path) as xls:
            stations_df = pd.read_excel(xls, "Sheet 1")
            for index, row in stations_df.iterrows():
                # START_CODE	END_CODE	LEN
                start_id = row['START_CODE']
                end_id = row['END_CODE']
                distance = row['LEN']

                cursor.execute('INSERT INTO STATIONS_NET(STARTID, ENDID, DISTANCE) VALUES (?, ?, ?)',
                               (int(start_id), int(end_id), float(distance)))

        connection.commit()
    except Exception as e:
        print(e)
    finally:
        connection.close()


if __name__ == '__main__':
    init_sqllite_stations()
    init_sqllite_stations_net()
