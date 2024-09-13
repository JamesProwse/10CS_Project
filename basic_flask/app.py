from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import sqlite3


#flask - the web application framework used to build the web application
#render_template - renders the HTML template
#repeat - handles http repeats (or input) from the browser(client) to send back to the app.py (server)
#redirect and url_for - used for URL redirection to direct the user to a web page
#session - manages the user information
# flash - used to display messages to the user
# datetime - handles date and time operations
# sqlite 3 - used for interacting
#have to put "app = Flask(__name__)" in
# execute a cursor object to interact with the database using SQL comments

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisaskibiditoiletecuadoriansquat' #this sets secret key for session management

def init_db(): # aq fucntion to initialize the database and create the users table if it doesnt exist
    conn = sqlite3.connect('basic_flask.db')
    cursor = conn.cursor() # creates a cursor object to interact with the database using SQL comments
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        age INTEGER NOT NULL
    )
    ''')
    conn.commit()
    conn.close()
# create a connection to the SQLite3 database

# create routes for the web application

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            age = request.form['age']

            conn = sqlite3.connect('basic_flask.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password, age) VALUES (?, ?, ?)', (username, password, age))
            conn.commit()
            conn.close()

            flash('User registered successfully!', 'success')
            return redirect(url_for('login'))

        except KeyError as e:
            flash('Error: Form field missing', 'error')
            return render_template('register.html')

    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect('basic_flask.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    # ? is a placeholder for values that will be paseed in execute function
    #(username, password), are the values that will be passed in the execute() function
    # THIS IS A PARAMETERIZED query to prevent sql injection attacks
    user = cursor.fetchone()
    conn.close()
    if user:
        session['user'] = user[1]
        print(user)
        session['age'] = user[3]
        return redirect(url_for('welcome'))
    return 'Login Failed'



@app.route('/hello_world')
def hello_world():
    return 'Hello, Year 10!'

@app.route('/welcome')
def welcome():
    if 'user' in session:
        user = session['user']
        age = session['age']
        return render_template('welcome.html', user=user, age=age)
    return redirect(url_for('login'))

#Calculator page route
@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    result = None
    if request.method == 'POST':
        num1 = int(request.form['num1'])
        num2 = int(request.form['num2'])
        operator = request.form['operator']
        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 != 0:
                result = num1 / num2
            else:
                result = "Error: Division by zero is undefined"
        else:
            result = "Invalid operator"
    return render_template('calculator.html', result=result)

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('age', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(port=5000, debug=True)


    # when in sqlite you can use '%number%' and it will return, for instance if e was in place of niumber it will return the data the has an e in it
