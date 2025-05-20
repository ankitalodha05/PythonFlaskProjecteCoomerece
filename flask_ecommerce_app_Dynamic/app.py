from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

# Initialize the Flask application
app = Flask(__name__)

# Database connection details (replace these with your RDS details)
db_config = {
    'host': 'database-1.c9gi28iw6c6y.ap-south-1.rds.amazonaws.com',  # Example: 'your-db-name.123456789012.us-west-1.rds.amazonaws.com'
    'user': 'admin',
    'password': 'adminadmin',
    'database': 'my_product',
}

# Function to connect to the database
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

# Route to display products
@app.route('/')
def home():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', products=products)

# Route to add a new product
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        image_url = request.form['image_url']

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO products (name, description, price, image_url) VALUES (%s, %s, %s, %s)",
                       (name, description, price, image_url))
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('home'))
    return render_template('add_product.html')

# Route to delete a product
@app.route('/delete_product/<int:product_id>', methods=['GET', 'POST'])
def delete_product(product_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('home'))
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


#if __name__ == '__main__':
    #app.run(debug=True)
