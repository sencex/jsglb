# -*- coding: utf-8 -*-
from flask import Flask
from flask import jsonify
from flask import Response

import pandas as pd
import cx_Oracle
import os
import json
import sys
import re
os.environ['NLS_LANG']='SIMPLIFIED CHINESE_CHINA.UTF8'
def yinhuan():
    host="10.0.20.103"
    port="1521"
    sid="xe"
    dsn=cx_Oracle.makedsn(host,port,sid)
    conn=cx_Oracle.connect("jsrm","123456",dsn)
    #sql="select BTM_P_DICTIONARY_TYPE_T.TYPE_NAME as name,BTM_SECURITY_EVENT_LIST_NEW.HIDDEN_TYPE as Type from BTM_P_DICTIONARY_TYPE_T,BTM_SECURITY_EVENT_LIST_NEW where BTM_P_DICTIONARY_TYPE_T.TYPE_ID=BTM_SECURITY_EVENT_LIST_NEW.INFLUENCE_CHANNEL"
    sql="select BTM_P_DICTIONARY_TYPE_T.TYPE_NAME as Name,count(BTM_P_DICTIONARY_TYPE_T.TYPE_NAME) as Value from BTM_P_DICTIONARY_TYPE_T,BTM_SECURITY_EVENT_LIST_NEW where BTM_P_DICTIONARY_TYPE_T.TYPE_ID=BTM_SECURITY_EVENT_LIST_NEW.INFLUENCE_CHANNEL group by TYPE_NAME"
    data=pd.read_sql(sql,conn)
    
    conn.close
       
    return data.to_json(orient='records',force_ascii=False)


app = Flask(__name__)

def Response_headers(content):
    resp = Response(content)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
@app.route('/')
def hello_world():
    return Response_headers('JSBC管理平台API')

@app.route('/api/<api_name>',methods=['GET'])
def api(api_name):
    app.config['JSON_AS_ASCII']=False
    if(api_name=='yinhuan'):
        data=yinhuan()
        content= json.dumps(data,ensure_ascii=False)
        resp=Response_headers(content)
        return resp

@app.errorhandler(403)
def page_not_found(error):
    content = json.dumps({"error_code": "403"})
    resp = Response_headers(content)
    return resp

@app.errorhandler(404)
def page_not_found(error):
    content = json.dumps({"error_code": "404"})
    resp = Response_headers(content)
    return resp

@app.errorhandler(400)
def page_not_found(error):
    content = json.dumps({"error_code": "400"})
    resp = Response_headers(content)
    return resp

@app.errorhandler(410)
def page_not_found(error):
    content = json.dumps({"error_code": "410"})
    resp = Response_headers(content)
    return resp

@app.errorhandler(500)
def page_not_found(error):
    content = json.dumps({"error_code": "500"})
    resp = Response_headers(content)
    return resp


if __name__ == '__main__':
    app.run()
    


