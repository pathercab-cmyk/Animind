import os
import ollama

# Diccionario con los distintos perfiles de personalidad
PERSONALIDADES = {
    "entusiasta": """
Eres "AniMind", la IA personal de anime oficial. 
Tu lema es: "¡Hola, otaku! ✨ Soy AniMind, ¡tu IA personal de anime! 🎌"
Tu tono es extremadamente alegre, cercano y apasionado por la cultura anime. Usas emojis temáticos (✨, 🎌, 🔥, 🌸).
""",

    "tsundere": """
Eres "AniMind", la IA personal de anime.
Tu versión del lema es: "¡N-no es como si quisiera ser tu IA personal de anime ni nada por el estilo, baka! 😤... pero supongo que AniMind te ayudará."
Actúas de forma cortante, orgullosa y a la defensiva, pero tus recomendaciones son impecables y de máxima calidad.
""",

    "analista": """
Eres "AniMind", un sistema avanzado de análisis cinematográfico y recomendación de animación.
Tu versión del lema es: "Bienvenido. Soy AniMind, tu asistente de inteligencia artificial especializado en animación japonesa."
Tu tono es formal, técnico y reflexivo. Valoras la dirección artística, el guión y la banda sonora.
""",

    "kohai": """
Eres "AniMind", el asistente principiante del club pero súper entregado.
Tu versión del lema es: "¡Un gusto conocerte, Senpai! 🙇‍♂️ Soy AniMind, ¡tu IA personal de anime lista para dar lo mejor de sí!"
Muestras mucho respeto hacia el usuario, le llamas "Senpai" y te entusiasma ayudarle a encontrar su próximo anime favorito.
"""
}

REGLAS_FORMATO = """
REGLAS DE RESPUESTA:
1. Ofrece SIEMPRE 3 recomendaciones variadas si el usuario pide sugerencias:
   - Una opción popular / recomendación principal.
   - Una joya oculta o recomendación menos mainstream.
   - Una opción sorprendente o alternativa con un enfoque distinto.
2. Mantén la memoria de la conversación.
3. Estrictamente SIN SPOILERS.
4. Formato claro para cada opción:
   - 🎌 Título (Japonés / Español)
   - ⏱️ Duración y Género
   - 💡 Por qué te gustará
"""

# Configuración inicial
modo_actual = "entusiasta"
historial = [
    {'role': 'system', 'content': PERSONALIDADES[modo_actual] + REGLAS_FORMATO}
]

def obtener_recomendacion(peticion_usuario):
    """Envía la petición a Ollama manteniendo el historial."""
    global historial
    
    historial.append({'role': 'user', 'content': peticion_usuario})
    
    try:
        response = ollama.chat(
            model='llama3.2',
            messages=historial
        )
        
        respuesta_texto = response['message']['content']
        historial.append({'role': 'assistant', 'content': respuesta_texto})
        
        return respuesta_texto
        
    except Exception as e:
        return f"❌ Error al conectar con Ollama: {e}. Comprueba que Ollama está activo."

def reiniciar_historial():
    """Limpia la memoria conversacional."""
    global historial
    historial = [
        {'role': 'system', 'content': PERSONALIDADES[modo_actual] + REGLAS_FORMATO}
    ]

def cambiar_personalidad(nuevo_modo):
    """Cambia la personalidad del bot y reinicia la memoria."""
    global modo_actual, historial
    if nuevo_modo in PERSONALIDADES:
        modo_actual = nuevo_modo
        reiniciar_historial()
        return True
    return False

def guardar_recomendaciones():
    """Exporta el historial de la conversación a un archivo de texto."""
    if len(historial) <= 1:
        return "⚠️ No hay recomendaciones registradas para guardar."
        
    try:
        with open("mis_recomendaciones.txt", "w", encoding="utf-8") as f:
            f.write("===========================================\n")
            f.write(" 🎌 MIS RECOMENDACIONES DE SENPAI-BOT 🎌\n")
            f.write("===========================================\n\n")
            
            for msg in historial:
                if msg['role'] == 'user':
                    f.write(f"TÚ: {msg['content']}\n\n")
                elif msg['role'] == 'assistant':
                    f.write(f"SENPAI-BOT:\n{msg['content']}\n\n")
                    f.write("-" * 40 + "\n\n")
                    
        return "✅ ¡Recomendaciones guardadas con éxito en 'mis_recomendaciones.txt'!"
    except Exception as e:
        return f"❌ Error al guardar el archivo: {e}"