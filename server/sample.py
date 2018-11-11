#!/usr/bin/env python
# coding: utf-8

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_restful.utils import cors
#mysql
import mysql.connector
import configparser

# 初期設定
app = Flask(__name__)
api = Api(app)
app.config['JSON_AS_ASCII'] = False #日本語文字化け対策
app.config["JSON_SORT_KEYS"] = False #ソートをそのまま
config = configparser.ConfigParser()
# 設定ファイルを読み込み
config.read('config.ini')

class Year(Resource):
    # GET時の挙動の設定
    @cors.crossdomain(origin='*')
    def get(self):
        conn = mysql.connector.connect(
            host = config['detabase_server']['host'],
            port = config['detabase_server']['port'],
            user = config['detabase_server']['user'],
            password = config['detabase_server']['password'],
            database = config['detabase_server']['database'],
        )
        connected = conn.is_connected()
        if (not connected):
            return make_response(jsonify({"DB ERROR": 'could not connect to db'}))
        conn.ping(reconnect=True)
        cur = conn.cursor()
        
        params = request.args
        if(params.get('year') is not None):
            print('yearが格納されている')
            print(params.get('year'))
            year = params.get('year')
            cur.execute('select tokuchou from tokuchou where date = %s',[year])
            table = cur.fetchall()
            print(table)
            table=table[0][0].split(' ')

            result = { 
                "year":year,
                "tokuchou": table
            }
            send_msg = jsonify(result)

            return send_msg

class YearWord(Resource):
    # GET時の挙動の設定
    @cors.crossdomain(origin='*')
    def get(self,year):
        conn = mysql.connector.connect(
            host = config['detabase_server']['host'],
            port = config['detabase_server']['port'],
            user = config['detabase_server']['user'],
            password = config['detabase_server']['password'],
            database = config['detabase_server']['database'],
        )
        connected = conn.is_connected()
        if (not connected):
            return make_response(jsonify({"DB ERROR": 'could not connect to db'}))
        conn.ping(reconnect=True)
        cur = conn.cursor()
        
        params = request.args
        print(params)
        # if((params.get('year') is not None) and (params.get('word') is not None)):
        print('year,wordが格納されている')
        print(year)
        # print(params.get('year'))
        print(params.get('word'))
        # year = params.get('year')
        word = params.get('word')
        word = '%'+word+'%'
        cur.execute('select * from origin partition(p%s) where dialogue like %s;',[year,word])
        table = cur.fetchall()
        # table=table[0][0].split(' ')
        print(table)

        result = { 
            "year":year,
            "word":word,
            "result": table
        }
        send_msg = jsonify(result)

        return send_msg


api.add_resource(Year, '/year')
api.add_resource(YearWord, '/yearWord/<int:year>')

if __name__ == '__main__':
    app.run()