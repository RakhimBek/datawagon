import sqlite3
import pandas as pd


def init_sqllite_stations():
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
                station_id = row['ST_ID']
                latitude = row['LATITUDE']
                longitude = row['LONGITUDE']

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
    connection = sqlite3.connect('sqll.db')
    try:
        cursor = connection.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS STATIONS_NET (
            START_ID INTEGER,
            END_ID INTEGER,
            DISTANCE REAL,
            PRIMARY KEY (START_ID, END_ID)
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

                cursor.execute('INSERT INTO STATIONS_NET(START_ID, END_ID, DISTANCE) VALUES (?, ?, ?)',
                               (int(start_id), int(end_id), float(distance)))

        connection.commit()
    except Exception as e:
        print(e)
    finally:
        connection.close()


if __name__ == '__main__':
    init_sqllite_stations()
    init_sqllite_stations_net()
