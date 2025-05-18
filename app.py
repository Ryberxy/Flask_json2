from flask import Flask, render_template, request, abort
import json

app = Flask(__name__)

with open("futbol.json", encoding="utf-8") as f:
    datos = json.load(f)

# Extraer todos los equipos para el desplegable
equipos_disponibles = list(datos["equipos"].keys())

def obtener_jugadores():
    jugadores = []
    for equipo, info in datos["equipos"].items():
        for jugador in info["jugadores"]:
            jugador["equipo"] = equipo
            jugador["posicion"] = jugador["detalles"]["posicion"]
            jugador["id"] = f"{equipo}_{jugador['nombre']}"
            jugadores.append(jugador)
    return jugadores

@app.route('/')
def portada():
    return render_template("portada.html")

@app.route('/jugadores', methods=["GET"])
def jugadores():
    return render_template("jugadores.html", equipos=equipos_disponibles)

@app.route('/listajugadores', methods=["POST"])
def lista_jugadores():
    jugadores = obtener_jugadores()
    nombre_filtro = request.form.get("nombre", "").strip().lower()
    equipo_filtro = request.form.get("equipo", "").strip()

    if nombre_filtro:
        jugadores = [j for j in jugadores if j["nombre"].lower().startswith(nombre_filtro)]

    if equipo_filtro:
        jugadores = [j for j in jugadores if j["equipo"] == equipo_filtro]

    return render_template("lista_jugadores.html",
                           jugadores=jugadores,
                           nombre=nombre_filtro,
                           equipos=equipos_disponibles,
                           equipo_seleccionado=equipo_filtro)

@app.route('/jugador/<identificador>')
def detalle(identificador):
    jugadores = obtener_jugadores()
    for jugador in jugadores:
        if jugador["id"] == identificador:
            return render_template("detalle.html", jugador=jugador)
    return abort(404)

if __name__ == '__main__':
    app.run("0.0.0.0", 5000, debug=True)
