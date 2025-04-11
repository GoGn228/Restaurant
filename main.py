from flask import Flask, render_template, request
import json
import sqlite3
app = Flask(__name__)

@app.route("/")
def main_page():
    return render_template("main_page.html")

app.run(debug=True)