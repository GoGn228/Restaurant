from flask import Flask, render_template, request
import json
import sqlite3
app = Flask(__name__)

con = sqlite3.connect("food.db", check_same_thread=False)
cursor = con.cursor()

@app.route("/")
def main_page():
    return render_template("main_page.html")

@app.route("/menu/")
def menu():
    return render_template("menu_page.html")

@app.route("/change/")
def change():
    dish = request.args.get("dish")
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
    return render_template("change_page.html", dish=dish, description=description, img=img, add1=add1, add2=add2, add3=add3, add4=add4, add5=add5, add6=add6)

@app.route("/order/")
def order():
    quantity = request.args.get("quantity", type=int, default=1)
    return render_template("order_page.html")

app.run(debug=True)


#<button onclick="addToCart('Паста Карбонара')">Добавить в заказ</button>