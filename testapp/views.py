import os
from flask import render_template, request, redirect, url_for  # 追加
from testapp import app
from testapp import db
from testapp.models.employee import Employee

# 写真のデータ授受
from werkzeug.utils import secure_filename
# static/imageデータリスト作成
import pathlib
# import cv2
import numpy as np

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


# サンプルデータリストページ 削除ボタン追加
@app.route('/sampledatalist/<int:id>/delete', methods=['POST'])  
def sampledatalist_delete(id):  
    sampledatalist = Sampledata.query.get(id)   
    db.session.delete(sampledatalist)  
    db.session.commit()  
    return redirect(url_for('data_list'))


# 写真データのアップロード
#-----ファイルのアップロード-----#
#GETの処理
# @app.route('/up/', methods=['GET'])
# def up_get():
#     return render_template('testapp/up.html', message = '画像を選択しよう', flag = False)

#GET,POSTの処理
@app.route('/up/', methods=['GET','POST'])
def up_post():
    if request.method == 'GET':
        return render_template('testapp/up.html', message = '画像を選択しよう', flag = False)
    if request.method == 'POST':
        # ファイルのリクエストパラメータを取得
        f = request.files.get('image')
        # ファイル名を取得
        filename = secure_filename(f.filename)
        # ファイルを保存するディレクトリを指定
        filepath = 'testapp/static/image/' + filename
        # ファイルを保存する
        f.save(filepath)
        return render_template('testapp/up.html', title = 'Form Sample(post)', message = 'アップロードされた画像({})'.format(filename), flag = True, image_name = filename)

#画像一覧
@app.route('/uploadlist')
def uploadlist():
    input_dir = "testapp/static/image"
    input_list = list(pathlib.Path(input_dir).glob('**/*.jpg'))

    for i in range(len(input_list)):
        img_file_name = str(input_list[i])
        img_np = np.fromfile(img_file_name, dtype=np.uint8)
        img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print("-------------------------------------------")
        print(img_file_name)

    return render_template('testapp/uploadlist.html')