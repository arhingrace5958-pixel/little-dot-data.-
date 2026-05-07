from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = "grace_little_dot_2026" # Keeps your login secure

# --- SET YOUR PRICES HERE ---
PRICING = {
    "2GB": {"sell": 11, "cost": 8},   # You sell for 11, you pay 8. Profit = 3
    "3GB": {"sell": 15, "cost": 11},
    "4GB": {"sell": 21, "cost": 16}
}

# This list clears if Render restarts (Free Tier), but tracks your daily sales.
sales_history = []

@app.route('/')
def home():
    items = [
        {"name": "2GB Bundle", "price": PRICING["2GB"]["sell"]},
        {"name": "3GB Bundle", "price": PRICING["3GB"]["sell"]},
        {"name": "4GB Bundle", "price": PRICING["4GB"]["sell"]}
    ]
    return render_template('index.html', items=items)

@app.route('/record_sale', methods=['POST'])
def record_sale():
    data = request.get_json()
    # Extract "2GB" from "2GB Bundle"
    size_key = data['name'].split(' ')[0] 
    
    # Calculate profit
    profit = PRICING[size_key]["sell"] - PRICING[size_key]["cost"]
    
    sale_entry = {
        "size": data['name'],
        "price": data['price'],
        "phone": data['phone'],
        "profit": profit
    }
    sales_history.append(sale_entry)
    return {"status": "success"}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == "GraceAdmin2026": # Your Password
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
    return render_template('login.html')

@app.route('/admin')
def admin():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    
    total_revenue = sum(s['price'] for s in sales_history)
    total_profit = sum(s['profit'] for s in sales_history)
    return render_template('admin.html', sales=sales_history, rev=total_revenue, prof=total_profit)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
