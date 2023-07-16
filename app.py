from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3
import os
import base64

app = Flask(__name__)
app.config['DATABASE'] = os.path.join(app.root_path, 'products.db')


# Database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Routes
@app.route('/')
def index():
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return render_template('index.html', products=products)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'klh' and password == 'qwerty123':
            return redirect(url_for('product_management'))
        else:
            return "Invalid credentials"
    else:
        return render_template('login.html')


@app.route('/product-management', methods=['GET', 'POST'])
def product_management():
    if request.method == 'POST':
        image = request.files['image']
        description = request.form['description']
        contact_number = request.form['contact_number']

        # Convert the image to base64 string
        image_data = base64.b64encode(image.read()).decode('utf-8')

        cursor = get_db().cursor()
        cursor.execute("INSERT INTO products (image_data, description, contact_number) VALUES (?, ?, ?)",
                       (image_data, description, contact_number))
        get_db().commit()

        return redirect(url_for('product_management'))
    else:
        cursor = get_db().cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        return render_template('product_management.html', products=products)


@app.route('/product/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    cursor = get_db().cursor()
    cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
    get_db().commit()

    return redirect(url_for('product_management'))


if __name__ == '__main__':
    app.run()
