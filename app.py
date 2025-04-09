from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL connection settings
db_config = {
    'host': 'rds.cr6wicc44n7f.us-east-2.rds.amazonaws.com',
    'user': 'admin',
    'password': 'mysql123',  # Change this to your actual MySQL password
    'database': 'project'
    
}

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Handle cake selection
@app.route('/order', methods=['POST'])
def order():
    cake = request.form['cake']
    quantity = request.form['quantity']
    return render_template('order.html', cake=cake, quantity=quantity)

# Handle order submission
@app.route('/submit', methods=['POST'])
def submit():
    cake = request.form['cake']
    quantity = request.form['quantity']
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    address = request.form['address']

    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Insert data into MySQL
        cursor.execute("""
            INSERT INTO orders (cake, quantity, name, email, phone, address)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (cake, quantity, name, email, phone, address))

        conn.commit()
        cursor.close()
        conn.close()
        return "Order Placed Successfully!"

    except mysql.connector.Error as err:
        return f"Database error: {err}"

if __name__ == '__main__':
    app.run(debug=True)
