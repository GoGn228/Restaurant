from flask import Flask, render_template, request
import json
import sqlite3
app = Flask(__name__)

@app.route("/")
def main_page():
    return render_template("main_page.html")

@app.route("/menu/")
def menu():
    return render_template("menu_page.html")

@app.route("/change/")
def change():
    return render_template("change_page.html")

@app.route("/order/")
def order():
    return render_template("order_page.html")

app.run(debug=True)


#<button onclick="addToCart('Паста Карбонара')">Добавить в заказ</button>