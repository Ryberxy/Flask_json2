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

@app.route('/jugadores', methods=["GET", "POST"])
def jugadores():
    jugadores_filtrados = []
    nombre_filtro = ""
    equipo_filtro = ""
    busqueda_realizada = False

    if request.method == "POST":
        busqueda_realizada = True
        nombre_filtro = request.form.get("nombre", "").strip().lower()
        equipo_filtro = request.form.get("equipo", "").strip()
        jugadores_filtrados = obtener_jugadores()

        if nombre_filtro:
            jugadores_filtrados = [j for j in jugadores_filtrados if j["nombre"].lower().startswith(nombre_filtro)]
        if equipo_filtro:
            jugadores_filtrados = [j for j in jugadores_filtrados if j["equipo"] == equipo_filtro]

    return render_template("jugadores.html",
                           equipos=equipos_disponibles,
                           jugadores=jugadores_filtrados,
                           nombre=nombre_filtro,
                           equipo_seleccionado=equipo_filtro,
                           busqueda_realizada=busqueda_realizada)


@app.route('/jugador/<identificador>')
def detalle(identificador):
    jugadores = obtener_jugadores()
    for jugador in jugadores:
        if jugador["id"] == identificador:
            return render_template("detalle.html", jugador=jugador)
    return abort(404)

if __name__ == '__main__':
    app.run("0.0.0.0", 5000, debug=True)
