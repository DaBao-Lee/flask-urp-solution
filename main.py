import json, time, os, threading
from flask import Flask, render_template, request, jsonify, redirect, url_for, session as flask_session

app = Flask(__name__)
app.secret_key = "a_random_secret_key_please_change"

# 全局存放 requests.Session 对象，key=用户名
user_sessions = {}
lock = threading.Lock()  # 写文件时加锁，防止并发问题


@app.route('/allowance', methods=['POST'])
def allowance():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    allowList = json.load(open('./static/allows.json', 'r'))
    if username in allowList['allow_user']:
        return jsonify({"status": "success"})
    else:
        if str(password) == "B11-406":
            allowList['allow_user'].append(username)
            json.dump(allowList, open('./static/allows.json', 'w'), indent=4)
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "fail"})


@app.route('/error.html', methods=['GET'])
def error():
    return render_template('error.html')


@app.route('/notallow.html', methods=['GET'])
def notallow():
    return render_template('notallow.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for("login"))


@app.route('/login.html', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/home.html', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/grades', methods=['GET', 'POST'])
def show_grade():
    username = request.form['username']
    password = request.form['password']
    mode = request.form.get('net', 'offline')

    flask_session['username'] = username
    flask_session['mode'] = mode

    if mode == 'online':
        from src.online import get_session, get_grades
    else:
        from src.offline import get_session, get_grades

    tmp_flag = 0
    name = "未授权用户"
    file_path = f'./static/logs/{time.strftime("%Y-%m-%d", time.localtime())}.json'
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        users = {}
    else:
        users = json.load(open(file_path, 'r', encoding='utf-8'))

    allows = json.load(open('./static/allows.json', 'r'))
    if not str(username) in allows['allow_user']:
        users[f'{time.time()}'] = {"name": f"{name}", 'username': username, 'password': password,
                                   "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                   "status": "fail", 'mode': mode}
        with lock:
            json.dump(users, open(f'{file_path}', 'w', encoding="utf-8"), indent=4, ensure_ascii=False)
        return redirect(url_for('notallow'))

    for _ in range(10):
        response, user_session = get_session(username, password)
        if '学分制综合教务' in response.text:
            name, result = get_grades(user_session)
            count = len(result['courseName'])
            users[f'{time.time()}'] = {"name": f"已授权用户 ==> {name}", 'username': username, 'password': password,
                                       "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                       "status": "success", 'mode': mode}
            with lock:
                json.dump(users, open(f'{file_path}', 'w', encoding='utf-8'), indent=4, ensure_ascii=False)

            # 保存到全局字典，供后续接口使用
            user_sessions[username] = user_session
            flask_session['name'] = name
            flask_session['result'] = result
            return render_template('process.html', result=result, count=count)
        else:
            tmp_flag += 1

    name = "密码错误"
    users[f'{time.time()}'] = {"name": f"已授权用户 ==> {name}", 'username': username, 'password': password,
                               "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                               "status": "fail"}
    with lock:
        json.dump(users, open(f'{file_path}', 'w', encoding='utf-8'), indent=4, ensure_ascii=False)
    return redirect(url_for('error'))


@app.route('/evaluationInfo', methods=['GET', 'POST'])
def getEvalInfo():
    username = flask_session.get('username')
    mode = flask_session.get('mode', 'offline')
    if not username or username not in user_sessions:
        return jsonify({"error": "未登录"}), 403

    if mode == 'online':
        from src.online import evaluateInfoShow
    else:
        from src.offline import evaluateInfoShow

    result = evaluateInfoShow(user_sessions[username])
    return jsonify(result)


@app.route('/evaluation', methods=['GET', 'POST'])
def startEval():
    username = flask_session.get('username')
    mode = flask_session.get('mode', 'offline')
    if not username or username not in user_sessions:
        return jsonify({"error": "未登录"}), 403

    if mode == 'online':
        from src.online import evaluate
    else:
        from src.offline import evaluate

    response = evaluate(user_sessions[username])
    if "评估成功！" in response.text:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "fail"})


@app.route('/about.html', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@app.route('/credits', methods=['GET', 'POST'])
def show_credits():
    username = flask_session.get('username')
    mode = flask_session.get('mode', 'offline')
    if not username or username not in user_sessions:
        return jsonify({"error": "未登录"}), 403

    if mode == 'online':
        from src.online import get_credits
    else:
        from src.offline import get_credits

    result = get_credits(user_sessions[username])
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='172.23.29.244', port=5888, debug=True, use_reloader=False)
