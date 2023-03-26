from flask import render_template, request, redirect, url_for  # 追加
from testapp import app
from testapp import db
from testapp.models.employee import Employee

# 新規DB(sampledataテーブル)追加に伴うデータ書き込み処理============
from testapp.models.sampledata import Sampledata
import datetime
# ==============================================================

# chart.js テスト========================================
# https://qiita.com/kubochiro/items/874ccddb564c7e684000
import os
@app.route('/graph')
def chart_do():
    c = {
        'chart_labels': "項目1, 項目２, 項目３, 項目４,項目５",
        'chart_data': "4, 7, 1, 3, 6",
        'chart_title': "グラフサンプル",
        'chart_target': "タイトル"
    }
    return render_template('testapp/graph.html', c=c)
# =======================================================


@app.route('/')
def index():
    my_dict = {
        'insert_something1': 'テスト用従業員登録ページです。',
        'insert_something2': 'Navbarから従業員登録・従業員一覧を表示することができます。',
        'test_titles': ['title1', 'title2', 'title3']
    }
    return render_template('testapp/index.html', my_dict=my_dict)

@app.route('/test')
def other1():
    return render_template('testapp/index2.html')

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'GET':
        return render_template('testapp/add_employee.html')
    if request.method == 'POST':
        form_name = request.form.get('name')  # str
        form_mail = request.form.get('mail')  # str
        # チェックなしならFalse。str -> bool型に変換
        form_is_remote = request.form.get('is_remote', default=False, type=bool)
        form_department = request.form.get('department')  # str
        # int, データないとき０
        form_year = request.form.get('year', default=0, type=int)

        employee = Employee(
            name=form_name,
            mail=form_mail,
            is_remote=form_is_remote,
            department=form_department,
            year=form_year
        )
        db.session.add(employee)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/employees')
def employee_list():
    employees = Employee.query.all()
    return render_template('testapp/employee_list.html', employees=employees)


#====================================#
#=========サンプルデータ追加==========#
#====================================#
@app.route('/add_sampledata', methods=['GET', 'POST'])
def add_sampledata():
    if request.method == 'GET':
        return render_template('testapp/add_sampledata.html')
    if request.method == 'POST':
        nowdatetime = datetime.datetime(2017, 11, 14, 11, 25, 28)
        form_speed = request.form.get('speed', default=0, type=int)
        form_peak = request.form.get('peak', default=0, type=int)
        form_itemno = request.form.get('itemno', default=0, type=int)

        sampledata = Sampledata(
            getdate = nowdatetime.date(),
            gettime = nowdatetime.time(),
            speed = form_speed,
            itemno = form_itemno,
            peak = form_peak
        )
        db.session.add(sampledata)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/sampledatalist')
def data_list():
    sampledatalist = Sampledata.query.all()
    return render_template('testapp/sampledata_list.html', sampledatalist=sampledatalist)

@app.route('/linechart')
def line():
    getdatalist = Sampledata.query.all()
    list_1 = []
    list_2 = []
    list_3 = []
    list_4 = []

    for getdata_1 in getdatalist:
        list_1.append(getdata_1.speed)
    # print(list_1)

    for getdata_2 in getdatalist:
        list_2.append(getdata_2.peak)
    # print(list_2)

    for getdata_3 in getdatalist:
        list_3.append(str(getdata_3.getdate))
    # print(list_3)
    
    for x in range(len(list_3)):
        list_4.append(x)
        x += 1
    # print(list_4)


    return render_template('testapp/linechart.html', list_1 = list_1, list_2 = list_2, list_4 = list_4)
