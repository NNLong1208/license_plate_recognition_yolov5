import psycopg2
import datetime

conn = psycopg2.connect(host = 'localhost', database="license_plate", user="postgres", password="long12")
conn.autocommit = True

def insert_in_out(cur, plate):
    time_in = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql_insert = "insert into in_out values('{}', '{}')".format(plate, time_in)
    cur.execute(sql_insert)
    conn.commit()

def check_in_out(cur, plate):
    sql_query = "select time_in_out from in_out where plate = '{}'".format(plate)
    cur.execute(sql_query)
    date_time = cur.fetchall()
    if len(date_time) == 0:
        return None
    else:
        return date_time[0][0]

def insert_history(cur, plate, time_in):
    time_out = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql_insert = "insert into history values('{}', '{}', '{}')".format(plate, time_in, time_out)
    cur.execute(sql_insert)
    conn.commit()

def delete_data(cur, plate):
    sql_delete = "delete from in_out where plate ='{}'".format(plate)
    cur.execute(sql_delete)
    conn.commit()

def store_data(plate):
    cur = conn.cursor()
    check = check_in_out(cur, plate)
    if check == None:
        insert_in_out(cur, plate)
    else:
        insert_history(cur, plate, check)
        delete_data(cur, plate)
    cur.close()

def get_data(plate):
    time_out = None
    cur = conn.cursor()
    time_in = check_in_out(cur, plate)
    if time_in == None:
        cur.execute("select * from in_out where plate = '{}'".format(plate))
        res = cur.fetchall()
        if len(res) == 0:
            cur.execute("select * from history where plate = '{}'".format(plate))
            res_his = cur.fetchall()
            cur.close()
            if len(res_his) == 0:
                return time_in, time_out
            else:
                plate,time_in, time_out = res_his[-1]
                return time_in, time_out
        else:
            plate, time_in = res
            return time_in, time_out
    else:
        return time_in, time_out
