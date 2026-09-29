from flask import Flask, render_template, request, jsonify
from recomendador import (
    obtener_recomendacion, 
    reiniciar_historial, 
    cambiar_personalidad, 
    guardar_recomendaciones,
    modo_actual
)

app = Flask(__name__)

@app.route("/")
def home():
    """Carga la página principal del chat."""
    return render_template("index.html", modo=modo_actual)

@app.route("/chat", methods=["POST"])
def chat():
    """Procesa los mensajes enviados por el usuario desde la web."""
    datos = request.get_json()
    mensaje = datos.get("mensaje", "").strip()

    if not mensaje:
        return jsonify({"respuesta": "Por favor escribe una consulta válida."})

    # Procesar comandos desde la web
    if mensaje == "/reset":
        reiniciar_historial()
        return jsonify({"respuesta": "🧹 Memoria reiniciada. ¡Empieza una nueva consulta!"})

    if mensaje == "/guardar":
        res = guardar_recomendaciones()
        return jsonify({"respuesta": res})

    if mensaje.startswith("/modo "):
        nuevo_modo = mensaje.split(" ")[1].lower()
        if cambiar_personalidad(nuevo_modo):
            lemas_respuestas = {
                "entusiasta": "🎭 Modo ENTUSIASTA activado: ¡Hola! ✨ Soy AniMind, ¡tu IA personal de anime! 🎌",
                "tsundere": "🎭 Modo TSUNDERE activado: ¡N-no es como si quisiera ser tu IA personal de anime, baka! 😤",
                "analista": "🎭 Modo ANALISTA activado: Bienvenido. Soy AniMind, tu asistente de IA especializado en animación.",
                "kohai": "🎭 Modo KOHAI activado: ¡A sus órdenes, Senpai! 🙇‍♂️ AniMind está listo para ayudarte."
            }
            return jsonify({"respuesta": lemas_respuestas.get(nuevo_modo, f"🎭 Personalidad cambiada a '{nuevo_modo.upper()}'")})
        return jsonify({"respuesta": "❌ Modo no válido. Opciones: entusiasta, tsundere, analista, kohai"})
    # Proceso normal con Ollama
    respuesta = obtener_recomendacion(mensaje)
    return jsonify({"respuesta": respuesta})

if __name__ == "__main__":
    # Inicia el servidor en http://127.0.0.1:5000/
    app.run(debug=True, port=5000)