from sys import orig_argv
from flask import Flask, render_template, request, session
import json
import sqlite3

app = Flask(__name__)
app.secret_key = "super_secret_key_123"

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
    def get_price():
        conn = sqlite3.connect('food.db')
        cursor = conn.cursor()
        cursor.execute("SELECT price FROM food_menu WHERE name = ?", (dish,))
        price = cursor.fetchone()
        conn.close()
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
    selected_ingredients = request.args.getlist("ingredientss")
    if "price" not in session:
        session["price"] = get_price() # Сохраняем цену в session
    print(selected_ingredients, price)
    base_price = float(price[0][0]) if price and price[0][0] else 0  # Проверяем, есть ли число
    selected_ingredients = [float(ing) for ing in selected_ingredients if ing.replace('.', '', 1).isdigit()]
    total_price = price + sum(selected_ingredients)
    print("Итоговая цена:", total_price)  # Проверяем финальное значение
    quantity = request.args.get("quantity", type=int, default=1)
    return render_template("change_page.html", dish=dish, description=description, img=img, add1=add1, add2=add2, add3=add3, add4=add4, add5=add5, add6=add6, quantity=quantity, total_price=total_price, price=session["price"])

@app.route("/order/")
def order():
    return render_template("order_page.html")


app.run(debug=True)


#<button onclick="addToCart('Паста Карбонара')">Добавить в заказ</button>