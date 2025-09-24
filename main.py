from sys import orig_argv
from types import NoneType
from typing import final

from flask import Flask, render_template, request, session, redirect
import json
import sqlite3

app = Flask(__name__)
app.secret_key = "super_secret_key_123"

@app.route("/")
def main_page():
    return render_template("main_page.html")

@app.route("/menu/")
def menu():
    conn = sqlite3.connect('food.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, dish, quantity, total_price FROM cart")
    cart = cursor.fetchall()
    total = sum(item[3] or 0 for item in cart)
    conn.close()
    return render_template("menu_page.html", cart=cart, total=total)

@app.route('/change')
def change():
    dish = request.args.get('dish')
    quantity = int(request.args.get('quantity', 1))
    ingredients = int(request.args.get('ingredients', 0))
    conn = sqlite3.connect('food.db')
    cursor = conn.cursor()
    cursor.execute("SELECT description FROM dishes WHERE name=?", (dish,))
    description = cursor.fetchone()
    cursor.execute("SELECT image FROM dishes WHERE name=?", (dish,))
    img = cursor.fetchone()
    cursor.execute("SELECT name FROM ingredients ORDER BY id")
    add_names = cursor.fetchall()
    base_price = cursor.execute("SELECT base_price FROM dishes WHERE name=?", (dish,)).fetchone()[0]
    price = base_price * quantity + ingredients
    conn.close()
    return render_template("change_page.html",
                           dish=dish,
                           quantity=quantity,
                           ingredients=ingredients,
                           price=price,
                           description=description,
                           img=img,
                           add1=add_names[0:1],
                           add2=add_names[1:2],
                           add3=add_names[2:3],
                           add4=add_names[3:4],
                           add5=add_names[4:5],
                           add6=add_names[5:6])

@app.route('/add_to_cart')
def add_to_cart():
    dish = request.args.get('dish')
    quantity = int(request.args.get('quantity'))
    ingredients = int(request.args.get('ingredients'))

    conn = sqlite3.connect('food.db')
    cursor = conn.cursor()
    base_price = cursor.execute("SELECT base_price FROM dishes WHERE name=?", (dish,)).fetchone()[0]
    total_price = base_price * quantity + ingredients

    cursor.execute("INSERT INTO cart (dish, quantity, ingredients, total_price) VALUES (?, ?, ?, ?)",
                   (dish, quantity, ingredients, total_price))
    conn.commit()
    conn.close()
    return redirect('/menu/')

@app.route('/remove/<int:id>')
def remove(id):
    conn = sqlite3.connect('food.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/menu/')


@app.route("/order/", methods=['POST'])
def order():
    return render_template("order_page.html")

@app.route("/fullMenu/")
def fullMenu():
    return render_template("fullMenu_page.html")

@app.route("/reservation/")
def reservation():
    conn = sqlite3.connect('food.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, location, seats, reserved FROM tables")
    tables = cursor.fetchall()
    conn.close()
    return render_template("reservation_page.html", tables=tables)

@app.route("/booking")
def booking():
    table_id = request.args.get('table')
    return render_template("booking.html", table_id=table_id)

@app.route('/confirm', methods=['POST'])
def confirm():
    table_id = request.form['table_id']
    name = request.form['name']
    date = request.form['date']
    time = request.form['time']
    conn = sqlite3.connect('food.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reservations (table_id, name, date, time) VALUES (?, ?, ?, ?)",
                   (table_id, name, date, time))
    cursor.execute("UPDATE tables SET reserved = 1 WHERE id = ?", (table_id,))
    conn.commit()
    conn.close()
    return render_template("final_page.html")

@app.route("/final/", methods=['POST'])
def final():
    name = request.form['name']
    phone = request.form['phone']
    address = request.form['address']
    conn = sqlite3.connect('food.db')
    cursor = conn.cursor()
    cursor.execute("SELECT dish, quantity, ingredients, total_price FROM cart")
    cart = cursor.fetchall()
    for dish, quantity, ingredients, total_price in cart:
        cursor.execute("""
            INSERT INTO orders (dish, quantity, ingredients, total_price)
            VALUES (?, ?, ?, ?)
        """, (dish, quantity, ingredients, total_price))

    cursor.execute("DELETE FROM cart")  # очищаем корзину
    conn.commit()
    conn.close()
    return render_template("final_page.html", name=name)

@app.route("/resFinal/", methods=['POST'])
def resFinal():
    return render_template("final_page.html")


#app.run(debug=True)

# <ul>
#    {% for id, dish, quantity, price in cart %}
#        <li>{{ dish }} ({{ quantity }}) — {{ price }} BYN
#            <a href="{{ url_for('remove', id=id) }}" class="remove-btn">✕</a>
#        </li>
#    {% endfor %}
# </ul>