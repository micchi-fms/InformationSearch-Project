import csv
import mysql.connector
import configparser


config = configparser.ConfigParser()
# 設定ファイルを読み込み
config.read('config.ini')

# tsvFile 
f = open('gijiroku.tsv','r')
tsv = csv.reader(f, delimiter = '\t')

#databese
conn = mysql.connector.connect(
    host = config['detabase_server']['host'],
    port = config['detabase_server']['port'],
    user = config['detabase_server']['user'],
    password = config['detabase_server']['password'],
    database = config['detabase_server']['database'],
)

connected = conn.is_connected()
print(connected)
if (not connected):
    print('could not connect to db')
    sys.exit()

conn.ping(reconnect=True)
cur = conn.cursor()

for s in tsv:
    if len(s) != 6:
        print('not 6')
        continue

    print(s)
    print(len(s))
    try:
        cur.execute('insert into origin(date,nickname,fullname,position,dialogue,siturl) values(%s, %s, %s, %s, %s, %s)', s)
        conn.commit()
        break
    except Exception as err:
        conn.rollback()
        print('error:', err)
        raise

f.close()