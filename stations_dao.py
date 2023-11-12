import sqlite3


def fetch_stations():
    """
Получить все существующие станции
    :return: список кортежей
    """
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
    """
Получить граф связей существующих станции
    :return:
    """
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
    """
Получить граф связей существующих станции с их описанием
    :return:
    """
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

# still too slow
def fetch_dislocations():
    """
Получить граф связей существующих станции с их описанием
    :return:
    """
    connection = sqlite3.connect('sqll.db')
    try:
        cursor = connection.cursor()
        cursor.execute('''
        select DISTINCT *
        from DISLOCATIONS
        where STDISL == 1771
          and datetime(OPERDATE) == datetime('2023-08-31 23:49:00');
        ''')

        return cursor.fetchall()

    except Exception as e:
        print(e)
    finally:
        connection.close()


