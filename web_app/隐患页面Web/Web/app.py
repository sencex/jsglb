from flask import Flask,render_template,url_for,request,redirect, jsonify
from pyecharts import Bar, Pie, Line
from pyecharts_javascripthon.api import TRANSLATOR
import pandas as pd
import os, sys
import json

app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

# read json and prepare
jsonFilePath = 'file://localhost//'+sys.path[0]+'\static\json\safe.json'
dataFromJson = pd.read_json(jsonFilePath, orient='records', convert_dates=True, encoding='utf-8')
dataFromJson = dataFromJson.reindex(columns=['date','channal','program','type','reason','attr','dept','handle','id'])
dataFromJson['year']=dataFromJson.date.values.astype('datetime64[Y]').astype('str')
dataFromJson['month']=dataFromJson.date.values.astype('datetime64[M]').astype('str')
dataFromJson['date']=dataFromJson.date.values.astype('datetime64[D]').astype('str')
colNameMap = {'date':'发生日期','channal':'影响频道、频率','program':'影响节目','type':'隐患类型','reason':'隐患原因','attr':'隐患性质','dept':'责任部门','handle':'处理措施','year':'年份'}

# preProgress for chart1
yearFilter = '2018'
colSel = 'channal'
dataSub = dataFromJson[dataFromJson['year']==yearFilter]
dataGroup = dataSub.groupby(colSel).count() 
# preProgress for chart2
yearFilter2 = '2018'
dataSub2 = dataFromJson[dataFromJson['year']==yearFilter]
dataGroupbyMonth = dataSub2.pivot_table(index='month',columns='dept',values='type',aggfunc='count')
dataGroupbyMonth = dataGroupbyMonth.fillna(0)

def pie_chart():
    pie = Pie(title=colNameMap[colSel])
    pie.add(colNameMap[colSel],list(dataGroup.index),[int(i) for i in list(dataGroup.date)],radius=[15, 60], is_label_show=True,rosetype='radius',is_legend_show=False)
    return pie

def bar_chart():
    if yearFilter2 == '0':
        title ='全部'
    else: title = yearFilter2+'年'
    bar = Bar(title=title)
    for dept in dataGroupbyMonth.columns:
        bar.add(dept, list(dataGroupbyMonth.index), [int(i) for i in list(dataGroupbyMonth[dept])],is_more_utils=True, legend_orient='horizontal', legend_pos='center', legend_top='top') 
    return bar

_pie = pie_chart()
_bar = bar_chart()
script_list = []
script_list.extend(_pie.get_js_dependencies())
script_list.extend(_bar.get_js_dependencies())
script_list = list(set(script_list))
dictMap = {'chart1':_pie,'chart2':_bar}

@app.route('/',methods=['GET','POST'])
def index():
    global _pie, _bar, dictMap
    _pie = pie_chart()
    _bar = bar_chart()
    dictMap = {'chart1':_pie,'chart2':_bar}
    return render_template(
        'safe_t.html', 
        host = 'static/js/pyecharts',
        script_list=script_list,
        )

# API取表格数据，可改成通用的取表格数据方法，表格id做为参数，类似做图
@app.route('/data/tableSafe',methods=['GET','POST'])
def data_tableSafe():  
    tableJson = dataFromJson.to_json(orient='records',force_ascii=True)
    return(tableJson)

# 异步取图表数据
@app.route('/data/<chartName>',methods=['GET','POST'])
def my_echart(chartName):  
    chart = dictMap[chartName]
    option = TRANSLATOR.translate(chart.options).option_snippet
    j = jsonify(option) 
    return(j)

@app.route('/getPieSel', methods=['POST'])
def getPieSel():
    global yearFilter, colSel, dataSub, dataGroup
    yearFilter = request.form.get('yearFilter')
    colSel = request.form.get('colSel')
    print("yearFilter: "+ yearFilter + " colSel:"+ colSel)
    if yearFilter == '0':
        dataSub = dataFromJson
    else:
        dataSub = dataFromJson[dataFromJson['year']==yearFilter]
    dataGroup = dataSub.groupby(colSel).count()  
    return redirect(url_for('index'))

@app.route('/getBarSel', methods=['POST'])
def getBarSel():
    global yearFilter2, dataSub2, dataGroupbyMonth
    yearFilter2 = request.form.get('yearFilter2')
    if yearFilter2 == '0':
        dataSub2 = dataFromJson
    else:
        dataSub2 = dataFromJson[dataFromJson['year']==yearFilter2]
    dataGroupbyMonth = dataSub2.pivot_table(index='month',columns='dept',values='type',aggfunc='count')
    dataGroupbyMonth = dataGroupbyMonth.fillna(0)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=True) 调试模式
    # app.run(host='0.0.0.0') 公网访问