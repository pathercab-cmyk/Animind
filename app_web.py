from flask import Flask, render_template, request, jsonify
from recomendador import (
    obtener_recomendacion,
    reiniciar_historial,
    cambiar_personalidad,
    guardar_recomendaciones
)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# Soportar ambas rutas para evitar errores de frontend
@app.route('/chat', methods=['POST'])
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json or {}
    mensaje = data.get('message', '') or data.get('mensaje', '')
    if not mensaje:
        return jsonify({'error': 'Mensaje vacío'}), 400
    
    respuesta = obtener_recomendacion(mensaje)
    return jsonify({'response': respuesta, 'respuesta': respuesta})

@app.route('/personality', methods=['POST'])
@app.route('/api/personality', methods=['POST'])
def set_personality():
    data = request.json or {}
    modo = data.get('mode', 'entusiasta')
    exito = cambiar_personalidad(modo)
    return jsonify({'success': exito})

@app.route('/reset', methods=['POST'])
@app.route('/api/reset', methods=['POST'])
def reset_chat():
    reiniciar_historial()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
