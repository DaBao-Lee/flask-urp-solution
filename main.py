from online import *
import json, time, os
from colorama import Fore
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

@app.route('/error', methods=['GET'])
def error():
    return render_template('error.html')

@app.route('/notallow', methods=['GET'])
def notallow():
    return render_template('notallow.html')

@app.route('/', methods=['GET', 'POST'])
def login():

    try:
        with open('./static/user.txt', 'r') as f:
            username = f.readline().strip()
            password = f.readline().strip()
            print(Fore.GREEN + "读取用户信息成功..." + Fore.RESET)
    except: username, password = '2215113116', ''
    
    return render_template('index.html', username=username, password=password)

@app.route('/grades', methods=['GET', 'POST'])
def show_grade():

    global session

    username = request.form['username']
    password = request.form['password']
    tmp_flag = 0
    name = "未授权用户"
    file_path = f'./static/{time.strftime("%Y-%m-%d", time.localtime())}.json'
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        users = {}
    else:
         users = json.load(open(file_path, 'r', encoding='utf-8'))

    allows = json.load(open('./static/allows.json', 'r'))
    if not str(username) in allows['allow_user']:
        users[f'{time.time()}'] = {"name": f"{name}", 'username': username, 'password': password,
                                    "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                    "status": "fail"}
        json.dump(users, open(f'{file_path}', 'w', encoding="utf-8"), indent=4, ensure_ascii=False)
        return redirect(url_for('notallow'))
    
    while True:
        response, session = get_session(username, password)
        if '学分制综合教务' in response.text:
            name, result = get_grades(session)
            count = len(result['courseName'])
            users[f'{time.time()}'] = {"name": f"已授权用户 ==> {name}", 'username': username, 'password': password,
                                        "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                        "status": "success"}
            json.dump(users, open(f'{file_path}', 'w', encoding='utf-8'), indent=4, ensure_ascii=False)
            break
        else:
            tmp_flag += 1
            print(f"验证码输入错误,正在重新识别, 还剩{10 - tmp_flag}次机会...")
            if tmp_flag == 10:
                print('请检查账号密码是否正确？网页是否维护中...')
                name = "密码错误"
                users[f'{time.time()}'] = {"name": f"已授权用户 ==> {name}", 'username': username, 'password': password,
                                        "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                        "status": "fail"}
                json.dump(users, open(f'{file_path}', 'w', encoding='utf-8'), indent=4, ensure_ascii=False)

                return redirect(url_for('error'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

    return render_template('process.html', result=result, count=count)

@app.route('/credits', methods=['GET', 'POST'])
def show_credits():
    result = get_credits(session)

    return jsonify(result)

@app.route('/evaluationInfo', methods=['GET', 'POST'])
def getEvalInfo():
    result = evaluateInfoShow(session)

    return jsonify(result)

@app.route('/evaluation', methods=['GET', 'POST'])  
def  startEval():
    response = evaluate(session)

    if "评估成功！" in response.text:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "fail"})

if __name__ == '__main__':

    url = "http://127.0.0.1:5000"
    app.run(host='127.0.0.1', port=5000, debug=True)

    # url = "http://172.23.17.70:5000"
    # app.run(host='172.23.17.70', port=5000, debug=True)
    