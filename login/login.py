from flask import Flask, render_template, request, session
import mysql.connector
import json
import subprocess

app = Flask(__name__)
app.secret_key = 'asdaksjdhaskjd'

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        cnx = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='activity'
        )
        cursor = cnx.cursor()
        query = "SELECT username,pass FROM nurse_info"
        cursor.execute(query)
        rows = cursor.fetchall()

        if username == rows[0][0] and password == rows[0][1]:
            session['loggedin'] = True
            session['username'] = rows[0][0]

            query2 = "SELECT name,age,gender FROM patient_list"
            cursor.execute(query2)
            result = cursor.fetchall()
            serialized_data = json.dumps(result)
            cursor.close()
            cnx.close()

            return render_template('index.html', msg='Logged in successfully!', result=serialized_data)
        else:
            return render_template('login.html', msg='Incorrect username / password !')
        cursor.close()
        cnx.close()
    else:
        return render_template('login.html', msg='')


@app.route('/patient', methods=['GET', 'POST'])
def viewlog():
    name = request.args.get('name')

    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='activity'
    )
    cursor = cnx.cursor()
    query3 = "SELECT name FROM patient_list"
    cursor.execute(query3)
    names = cursor.fetchall()
    if name == names[0][0]:
        query4 = "SELECT time,activity FROM activity_log"
        cursor.execute(query4)
        result2 = cursor.fetchall()
        formatted_data = [(dt.strftime('%Y-%m-%d %H:%M:%S'), description) for dt, description in result2]
        json_data = json.dumps(formatted_data)
        cursor.close()
        cnx.close()
        return render_template('patient.html', result=json_data)

    cursor.close()
    cnx.close()


@app.route('/execute', methods=['GET', 'POST'])
def execute():
    subprocess.run(['python', 'clear_db.py'])

    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='activity'
    )
    cursor = cnx.cursor()
    query4 = "SELECT time,activity FROM activity_log"
    cursor.execute(query4)
    result2 = cursor.fetchall()
    formatted_data = [(dt.strftime('%Y-%m-%d %H:%M:%S'), description) for dt, description in result2]
    json_data = json.dumps(formatted_data)
    cursor.close()
    cnx.close()

    return render_template('patient.html', result=json_data)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    subprocess.run(['python', 'predict.py'])

    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='activity'
    )
    cursor = cnx.cursor()
    query4 = "SELECT time,activity FROM activity_log"
    cursor.execute(query4)
    result2 = cursor.fetchall()
    formatted_data = [(dt.strftime('%Y-%m-%d %H:%M:%S'), description) for dt, description in result2]
    json_data = json.dumps(formatted_data)
    cursor.close()
    cnx.close()

    return render_template('patient.html', result=json_data)


if __name__ == '__main__':
    app.run()
