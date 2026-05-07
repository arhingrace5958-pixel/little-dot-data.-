from flask import Flask, render_template, request, redirect, url_for, session
import random
import string
import os

app = Flask(__name__)
app.secret_key = "grace_secret_key_123" # This protects your login session

# Simple password for you (Change this to something only you know!)
ADMIN_PASSWORD = "GraceAdmin2026"

# This list will store sales during this session
sales_history = []

def generate_order_code():
    return "LD-" + "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))

@app.route('/')
def home():
    data_bundles = [
        {"size": "2GB", "price": "11", "code": generate_order_code()},
        {"size": "3GB", "price": "15", "code": generate_order_code()},
        {"size": "4GB", "price": "21", "code": generate_order_code()}
    ]
    return render_template('index.html', products=data_bundles)

# Route to record a sale when the button is clicked
@app.route('/record_sale', methods=['POST'])
def record_sale():
    data = request.get_json()
    sales_history.append(data)
    return {"status": "success"}

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
    return render_template('login.html')

# Admin Dashboard
@app.route('/admin')
def admin():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    return render_template('admin.html', sales=sales_history)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
