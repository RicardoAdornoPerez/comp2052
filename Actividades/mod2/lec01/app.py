from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "estructura_datos.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        datos = json.load(f)
else:
    datos = {
        "tanques": [
            {"modelo": "Leopard 2", "pais": "Alemania", "blindaje": "Compuesto"},
            {"modelo": "Abrams M1A2", "pais": "EE.UU.", "blindaje": "Uranio empobrecido"}
        ],
        "productos": [
            {"nombre": "Aceite de motor", "precio": 29.99},
            {"nombre": "Camuflaje", "precio": 15.00}
        ]
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tanques")
def tanques():
    return render_template("tanques.html", tanques=datos["tanques"])

@app.route("/productos")
def productos():
    return render_template("productos.html", productos=datos["productos"])

if __name__ == "__main__":
    app.run(debug=True)
