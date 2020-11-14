import pymysql.cursors


SQL_INFO = {
    'HOST': 'k3a306.p.ssafy.io',
    'USER': 'root',
    'PW': 'ssafy306',
    'DB': 'matchon',
    'PORT': 3306
}


def time_check(now_date, now_time):
    global SQL_INFO
    conn = pymysql.connect(host=SQL_INFO['HOST'], port=SQL_INFO['PORT'], user=SQL_INFO['USER'], password=SQL_INFO['PW'], db=SQL_INFO['DB'], charset='utf8mb4')
    print(conn)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    print(cursor)
    sql = "select id, status FROM `users_beforematch`;"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    # sql = f'''update users_beforematch set status = 4 where id IN (select ext_id FROM (select b.id AS ext_id from users_beforematch b left join users_aftermatch a ON b.id = a.before_match_id where b.status = 3 and a.fixed_time < '{now_time}' and b.date = '{now_date}') c);'''
    sql = f'''update users_beforematch set status = 4 where id IN (select ext_id FROM (select b.id AS ext_id from users_beforematch b left join users_aftermatch a ON b.id = a.before_match_id where b.status = 3 and a.fixed_time < '{now_time}' and b.date = '2020-11-15') c);'''
    cursor.execute(sql)
    conn.commit()
    conn.close()