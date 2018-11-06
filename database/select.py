import mysql.connector
import configparser

config = configparser.ConfigParser()
# 設定ファイルを読み込み
config.read('config.ini')
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
cur.execute('select count(*) from origin')
table = cur.fetchall()
print(table)