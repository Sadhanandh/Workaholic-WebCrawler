import sqlite3
 
def query(request_query):
    conn = sqlite3.connect("mydatabase.db") 
    cursor = conn.cursor()
    sql="""
    SELECT DISTINCT url 
    FROM iprecords
    WHERE url IN (%s)
    """ %','.join('?'*len(request_query))
    cursor.execute(sql,list(map(lambda x:str(x[0]),request_query)))
    data =  cursor.fetchall()
    formated_data =  map(lambda x:x[0],data)
    returndata = []
    for everyurl,i in request_query:
        if everyurl not in formated_data:
            returndata.append((everyurl,i+1))
    formated_data = returndata
    next_sql="""
    INSERT OR IGNORE INTO iprecords VALUES (:url, 0)
    """
    sub_sql="""
    UPDATE iprecords SET hits = hits + 1 WHERE url LIKE :url
    """
    for every_data,depth in request_query:
        cursor.execute(next_sql,dict(url=every_data))
        cursor.execute(sub_sql,dict(url=every_data))
    conn.commit()
    return formated_data




def init():
    conn = sqlite3.connect("mydatabase.db") 
    cursor = conn.cursor()
    sql_table = "SELECT name FROM sqlite_master WHERE type='table' AND name='iprecords'"
    cursor.execute(sql_table)
    data = cursor.fetchall()
    if len(data)==0:
        create()



def create():
    conn = sqlite3.connect("mydatabase.db") 
    cursor = conn.cursor()
    sql="""
    CREATE TABLE iprecords (url TEXT UNIQUE,hits INTEGER)
    """
    cursor.execute(sql)
    conn.commit()





