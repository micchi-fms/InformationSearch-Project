# 必要なモジュールの読み込み
from flask import Flask, jsonify, abort, make_response,request
from flask_cors import CORS, cross_origin
import mysql.connector
import configparser

# Flaskクラスのインスタンスを作成
# __name__は現在のファイルのモジュール名
app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False #日本語文字化け対策
app.config["JSON_SORT_KEYS"] = False #ソートをそのまま
config = configparser.ConfigParser()
# 設定ファイルを読み込み
config.read('config.ini')

def getConnection():
    return mysql.connector.connect(
        host = config['detabase_server']['host'],
        port = config['detabase_server']['port'],
        user = config['detabase_server']['user'],
        password = config['detabase_server']['password'],
        database = config['detabase_server']['database'],
    )


# POSTの実装
@app.route('/year', methods=['GET'])
def post():
    #POST通信
    # if request.method == 'GET':
    conn = getConnection()
    connected = conn.is_connected()
    if (not connected):
        return make_response(jsonify({"DB ERROR": 'could not connect to db'}))
    conn.ping(reconnect=True)
    cur = conn.cursor()
    
    #年データから
    params = request.args
    if(params.get('year') is not None):
        print('yearが格納されている')
        print(params.get('year'))
        year = params.get('year')
        cur.execute('select tokuchou from tokuchou where date = %s',[year])
        table = cur.fetchall()
        table=table[0][0].split(' ')
        print(table)

        result = { 
            "year":year,
            "tokuchou": table
        }
        return make_response(jsonify(result))
    # else:
    #     return make_response(jsonify({"POST ERROR": 'could not connect to api by post'}))

# エラーハンドリング
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# ファイルをスクリプトとして実行した際に
# ホスト0.0.0.0, ポート3001番でサーバーを起動
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=3001)