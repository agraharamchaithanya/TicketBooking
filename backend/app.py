from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__, template_folder='../templates')  # 👈 this is IMPORTANT
app.secret_key = 'your_secret_key'

# Path to DB (optional)
DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')
if not os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DB_PATH)
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()
        conn.close()
        if user:
            session['user'] = username
            return redirect(url_for('seat_selection'))
        else:
            return "Login Failed"
    return render_template('login.html')

@app.route('/seat_selection', methods=['GET', 'POST'])
def seat_selection():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        return redirect(url_for('form'))
    return render_template('seat_selection.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        return redirect(url_for('payment'))
    return render_template('form.html')

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        return redirect(url_for('ticket'))
    return render_template('payment.html')

@app.route('/ticket')
def ticket():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('ticket.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/casestudies')
def casestudies():
    return render_template('casestudies.html')

if __name__ == '__main__':
    app.run(debug=True)
