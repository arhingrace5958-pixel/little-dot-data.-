from flask import Flask, render_template

app = Flask(__name__)

# This is our "Database" - a list of your products
products = [
    {"name": "Software Junior Setup", "price": "GHS 50", "desc": "Custom business tech setup."},
    {"name": "Python Tutoring", "price": "GHS 100", "desc": "Learn Python for utility projects."},
    {"name": "Phone Optimization", "price": "GHS 30", "desc": "Speed up your Android device."}
]

@app.route('/')
def home():
    # This sends the product list to the HTML file
    return render_template('index.html', items=products)

if __name__ == '__main__':
    app.run(debug=True)
