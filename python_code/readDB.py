# -*- coding: cp936 -*-
import pandas as pd
import cx_Oracle
import os
import json
import sys
import re

os.environ['NLS_LANG']='SIMPLIFIED CHINESE_CHINA.UTF8'


#reload(sys)
#sys.setdefaultencoding('utf8') 

def readDB():
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
