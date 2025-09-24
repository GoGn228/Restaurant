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
    cart = session.get('cart', {})  # получаем корзину из session
    return render_template("menu_page.html", cart=cart)

@app.route("/change/")
def change():
    dish = request.args.get("dish")
    conn = sqlite3.connect('food.db')
    cursor = conn.cursor()
    def get_price():
        cursor.execute("SELECT price FROM food_menu WHERE name = ?", (dish,))
        price = cursor.fetchone()
        return price[0] if price else 0  # Гарантируем, что вернётся число
    cursor.execute('SELECT description FROM food_menu WHERE name=(?)', (dish,))
    description = cursor.fetchall()
    cursor.execute('SELECT img FROM food_menu WHERE name=(?)', (dish,))
    img = cursor.fetchall()
    cursor.execute('SELECT add1 FROM food_menu WHERE name=(?)', (dish,))
    add1 = cursor.fetchall()
    cursor.execute('SELECT add2 FROM food_menu WHERE name=(?)', (dish,))
    add2 = cursor.fetchall()
    cursor.execute('SELECT add3 FROM food_menu WHERE name=(?)', (dish,))
    add3 = cursor.fetchall()
    cursor.execute('SELECT add4 FROM food_menu WHERE name=(?)', (dish,))
    add4 = cursor.fetchall()
    cursor.execute('SELECT add5 FROM food_menu WHERE name=(?)', (dish,))
    add5 = cursor.fetchall()
    cursor.execute('SELECT add6 FROM food_menu WHERE name=(?)', (dish,))
    add6 = cursor.fetchall()
    cursor.execute('SELECT price FROM food_menu WHERE name=(?)', (dish,))
    price = get_price()
    ingredients = request.args.get("ingredients", type=int, default=0)
    if "price" not in session or session["price"] is None:
        session["price"] = get_price() # Сохраняем цену в session
    base_price = float(price) if price else 0  # Проверяем, есть ли число
    quantity = request.args.get("quantity", type=int, default=1)
    total_price = (session["price"]*quantity) + ingredients
    return render_template("change_page.html", dish=dish, description=description, img=img, add1=add1, add2=add2, add3=add3, add4=add4, add5=add5, add6=add6, quantity=quantity, price=total_price, ingredients=ingredients)

@app.route('/add', methods=['POST'])
def add():
    dish = request.form['dish']
    quantity = int(request.form['quantity'])
    # Инициализируем корзину, если её нет
    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']
    # Если блюдо уже есть — увеличиваем количество
    if dish in cart:
        cart[dish] += quantity
    else:
        cart[dish] = quantity
    session['cart'] = cart  # сохраняем обратно
    return redirect('/menu/')


@app.route("/order/")
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
    #dish = request.form['dish']
    #quantity = request.form['quantity']
    conn = sqlite3.connect('food.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO food_order (name, phone, address) VALUES (?, ?, ?)", (name, phone, address))
    conn.commit()
    conn.close()
    return render_template("final_page.html")

@app.route("/resFinal/", methods=['POST'])
def resFinal():
    return render_template("final_page.html")


app.run(debug=True)


#<button onclick="addToCart('Паста Карбонара')">Добавить в заказ</button>
