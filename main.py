import json, time, os
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)
mode = None

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


# @app.route('/index', methods=['GET', 'POST'])
# def index():
#     username, password = '2215113116', ''
#
#     return render_template('index.html', username=username, password=password)


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
    global session, mode

    username = request.form['username']
    password = request.form['password']
    mode = request.form.get('net', 'offline')

    if mode == 'online':
        print("online")
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
        json.dump(users, open(f'{file_path}', 'w', encoding="utf-8"), indent=4, ensure_ascii=False)
        return redirect(url_for('notallow'))

    while True:
        response, session = get_session(username, password)
        if '学分制综合教务' in response.text:
            name, result = get_grades(session)
            count = len(result['courseName'])
            users[f'{time.time()}'] = {"name": f"已授权用户 ==> {name}", 'username': username, 'password': password,
                                       "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                       "status": "success", 'mode': mode}
            json.dump(users, open(f'{file_path}', 'w', encoding='utf-8'), indent=4, ensure_ascii=False)
            break
        else:
            tmp_flag += 1
            if tmp_flag == 10:
                name = "密码错误"
                users[f'{time.time()}'] = {"name": f"已授权用户 ==> {name}", 'username': username, 'password': password,
                                           "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                           "status": "fail"}
                json.dump(users, open(f'{file_path}', 'w', encoding='utf-8'), indent=4, ensure_ascii=False)

                return redirect(url_for('error'))

    return render_template('process.html', result=result, count=count)



@app.route('/evaluationInfo', methods=['GET', 'POST'])
def getEvalInfo():

    if mode == 'online':
        from src.online import evaluateInfoShow, evaluate, get_credits
    else:
        from src.offline import evaluateInfoShow, evaluate, get_credits

    result = evaluateInfoShow(session)

    return jsonify(result)


@app.route('/evaluation', methods=['GET', 'POST'])
def startEval():

    if mode == 'online':
        from src.online import evaluateInfoShow, evaluate, get_credits
    else:
        from src.offline import evaluateInfoShow, evaluate, get_credits

    response = evaluate(session)
    if "评估成功！" in response.text:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "fail"})



@app.route('/about.html', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@app.route('/credits', methods=['GET', 'POST'])
def show_credits():

    if mode == 'online':
        from src.online import evaluateInfoShow, evaluate, get_credits
    else:
        from src.offline import evaluateInfoShow, evaluate, get_credits

    result = get_credits(session)

    return jsonify(result)


if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)
    # app.run(host='172.23.17.70', port=5000, debug=True, use_reloader=False)
    app.run(host='192.168.110.121', port=5000, debug=True, use_reloader=False)
