from flask import Flask, render_template, request, jsonify
from recomendador import obtener_recomendacion

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'response': 'Petición no válida.'}), 400

        user_message = data.get('message', '').strip()
        personality = data.get('personality', 'otaku')

        if not user_message:
            return jsonify({'response': 'Por favor, escribe un mensaje.'}), 400

        # Llamada al recomendador pasando el mensaje y la personalidad
        respuesta = obtener_recomendacion(user_message, personalidad=personality)
        
        return jsonify({'response': respuesta})

    except Exception as e:
        return jsonify({'response': f'Error interno del servidor: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)rt=5000)
