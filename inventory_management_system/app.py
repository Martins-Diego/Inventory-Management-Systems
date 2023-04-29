import pymysql
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def db_connection():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="admin",
        database="inventory_db",
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    products = get_all_products()
    return render_template('index.html', products=products)

def get_all_products():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products


@app.route('/add', methods=['POST'])
def add_product():
    conn = db_connection()
    cursor = conn.cursor()
    
    #Get the data from the submitted form
    product_code = request.form['product_code']
    description = request.form['description']
    price_per_unit = request.form['price_per_unit']
    quantity = request.form['quantity']

    # Calculate stock values and inventory amount
    stock = int(quantity) 
    inventory_amount = float(price_per_unit) * stock

    # Verify if the product already exists in the db
    cursor.execute("SELECT * FROM inventory WHERE product_code = %s", (product_code,))
    product_exists = cursor.fetchone()

    if not product_exists:
        # If the product does not exist, insert the data into the database table
        cursor.execute("INSERT INTO inventory (product_code, descrip, price_per_unit, entries, issues, stock, inventory_amount) VALUES (%s, %s, %s, %s, 0, %s, %s)", (product_code, description, price_per_unit, quantity, stock, inventory_amount))
        conn.commit()
        status = "success"
    else:
        status = "error"

    # Close the conecction
    cursor.close()
    conn.close()
    
    # Returns a success or error response depending on the case
    return jsonify({"status": status})

@app.route('/issue', methods=['POST'])
def issue_product():
    conn = db_connection()
    cursor = conn.cursor()
    
    # Get the submitted form data
    product_code = request.form['product_code']
    quantity = int(request.form['quantity'])

    # Gets the corresponding product from the database
    cursor.execute("SELECT * FROM inventory WHERE product_code = %s", (product_code,))
    product = cursor.fetchone()

    if product:
        # Check if there is enough stock to extract
        if quantity > product['stock']:
            # Close the connection
            cursor.close()
            conn.close()

            # Return an error response
            return jsonify({"status": "error", "message": "There's not enough stock"})
        
        # Updates the 'issues' field in the database
        issues = product['issues'] + quantity
        cursor.execute("UPDATE inventory SET issues = %s WHERE product_code = %s", (issues, product_code))

        # Gets the updated product from the database
        cursor.execute("SELECT * FROM inventory WHERE product_code = %s", (product_code,))
        product = cursor.fetchone()

        # Calculates updated stock values and inventory amount
        stock = product['entries'] - product['issues']
        inventory_amount = stock * product['price_per_unit']

        # Update database values
        cursor.execute("UPDATE inventory SET stock = %s, inventory_amount = %s WHERE product_code = %s", (stock, inventory_amount, product_code))
        conn.commit()

        # Cierra la conexión
        cursor.close()
        conn.close()

        # Retorna una respuesta exitosa
        return jsonify({"status": "success"})
    else:
        # Close the connection
        cursor.close()
        conn.close()

        # Return an error response
        return jsonify({"status": "error", "message": "Product not found"})



if __name__ == "__main__":
    app.run(debug=True)
