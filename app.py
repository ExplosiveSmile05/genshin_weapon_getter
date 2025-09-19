from flask import Flask, jsonify, Response
import requests

app = Flask(__name__)
url = "https://genshin.jmp.blue"

@app.route('/<character>', methods=['GET'])
def character(character):
    respuesta = requests.get(f"{url}/characters/{character}")
    if respuesta.status_code == 200:
        datos = respuesta.json()

        personaje = {
            "Nombre": datos["name"],
            "Tipo": datos["vision"],
            "Nación": datos["nation"],
            "Weapon": datos["weapon"]
        }
        
        arma_tipo = personaje["Weapon"]
        armas = requests.get(f"{url}/weapons").json()

        nombres_armas = []
        for nombre in armas:
            arma_info = requests.get(f"{url}/weapons/{nombre}").json()
            if arma_info.get("type") == arma_tipo:
                nombres_armas.append(arma_info["name"])
            if len(nombres_armas) >= 3:
                break

        salida = f"""
Personaje: {personaje['Nombre']}
Tipo: {personaje['Tipo']}
Nación: {personaje['Nación']}
Tipo de Arma: {personaje['Weapon']}

Armas disponibles:
- """ + "\n- ".join(nombres_armas)

        return Response(salida, mimetype="text/plain")

    else:
        return jsonify({"error": "No se pudo obtener el clima"}), respuesta.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)