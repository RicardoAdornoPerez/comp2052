from flask import Flask, request, jsonify
import json
import os
import platform

app = Flask(__name__)
DATA_FILE = "estructura_datos.json"

# Cargar estructura desde archivo o crearla si no existe
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        datos = json.load(f)
else:
    datos = {"usuarios": [], "productos": []}

# Guardar cambios en el archivo
def guardar_datos():
    with open(DATA_FILE, "w") as f:
        json.dump(datos, f, indent=2)

# GET /info: información del sistema
@app.route("/info", methods=["GET"])
def info():
    return jsonify({
        "sistema_operativo": platform.system(),
        "version": platform.version(),
        "arquitectura": platform.machine()
    }), 200

# POST /crear_usuario: añadir un nuevo usuario
@app.route("/crear_usuario", methods=["POST"])
def crear_usuario():
    data = request.get_json()
    nombre = data.get("nombre")
    correo = data.get("correo")

    if not nombre or not correo:
        return jsonify({"error": "Faltan campos: 'nombre' y 'correo' son obligatorios."}), 400

    nuevo_usuario = {
        "id": len(datos["usuarios"]) + 1,
        "nombre": nombre,
        "correo": correo
    }
    datos["usuarios"].append(nuevo_usuario)
    guardar_datos()

    return jsonify({"mensaje": "Usuario creado correctamente", "usuario": nuevo_usuario}), 201

# GET /usuarios: listar usuarios
@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    return jsonify({"usuarios": datos["usuarios"]}), 200

# (Opcional extra) POST /crear_producto: añadir producto
@app.route("/crear_producto", methods=["POST"])
def crear_producto():
    data = request.get_json()
    nombre = data.get("nombre")
    precio = data.get("precio")

    if not nombre or precio is None:
        return jsonify({"error": "Faltan campos: 'nombre' y 'precio' son obligatorios."}), 400

    nuevo_producto = {
        "id": len(datos["productos"]) + 1,
        "nombre": nombre,
        "precio": float(precio)
    }
    datos["productos"].append(nuevo_producto)
    guardar_datos()

    return jsonify({"mensaje": "Producto creado correctamente", "producto": nuevo_producto}), 201

# GET /productos: listar productos
@app.route("/productos", methods=["GET"])
def listar_productos():
    return jsonify({"productos": datos["productos"]}), 200

if __name__ == "__main__":
    app.run(debug=True)
