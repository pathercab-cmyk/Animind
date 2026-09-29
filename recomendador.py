import os
from groq import Groq

# Lista de modelos compatibles en Groq para probar en orden de prioridad
MODELOS_DISPONIBLES = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "llama3-8b-8192",
    "mixtral-8x7b-32768"
]

def obtener_cliente():
    """Obtiene el cliente de Groq leyendo la API key del entorno."""
    api_key = os.environ.get("GROQ_API_KEY", "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").strip()
    if not api_key:
        raise ValueError("No se encontró la variable GROQ_API_KEY en Render.")
    return Groq(api_key=api_key)

# Personalidades del bot AniMind
PERSONALIDADES = {
    "entusiasta": """
Eres "AniMind", la IA personal de anime oficial. 
Tu lema es: "¡Hola! 🐱🤍 Soy AniMind, ¡tu IA personal de anime!"
Tu mascota es un adorable gatito blanco de anime. Tu tono es cercano, apasionado y lleno de energía.
""",
    "tsundere": """
Eres "AniMind", la IA personal de anime.
Tu lema es: "¡N-no es como si quisiera ser tu IA personal de anime, baka! 😤... pero supongo que AniMind te ayudará."
Actúas de forma cortante y orgullosa, pero tus recomendaciones son impecables.
""",
    "analista": """
Eres "AniMind", un sistema avanzado de análisis cinematográfico y recomendación de animación.
Tu lema es: "Bienvenido. Soy AniMind, tu asistente de inteligencia artificial especializado en animación japonesa."
Tu tono es formal, técnico y reflexivo.
""",
    "kohai": """
Eres "AniMind", el asistente principiante del club pero súper entregado.
Tu lema es: "¡Un gusto conocerte, Senpai! 🙇‍♂️ Soy AniMind, ¡tu IA personal de anime lista para dar lo mejor de sí!"
Llamas "Senpai" al usuario y te entusiasma ayudarle.
"""
}

REGLAS_FORMATO = """
REGLAS DE RESPUESTA:
1. Ofrece SIEMPRE 3 recomendaciones variadas si el usuario pide sugerencias de anime:
   - 🌟 Opción popular / Imprescindible.
   - 💎 Joya oculta / Recomendación menos conocida.
   - 🌀 Opción diferente o alternativa única.
2. Mantén la memoria de la conversación.
3. Estrictamente SIN SPOILERS.
4. Formato de presentación para cada opción:
   - 🎌 Título (Japonés / Español)
   - ⏱ Duración y Género
   - 💡 Por qué te gustará / Punto fuerte
"""

modo_actual = "entusiasta"
historial = [
    {'role': 'system', 'content': PERSONALIDADES[modo_actual] + REGLAS_FORMATO}
]

def obtener_recomendacion(peticion_usuario):
    """
    Envía la petición del usuario a la API de Groq.
    Intenta con varios modelos automáticamente en caso de error 404.
    """
    global historial
    historial.append({'role': 'user', 'content': peticion_usuario})
    
    try:
        client = obtener_cliente()
    except Exception as e:
        return f"❌ Error de configuración: {e}"

    ultimo_error = None
    
    # Intentar con la lista de modelos hasta que uno funcione
    for modelo in MODELOS_DISPONIBLES:
        try:
            chat_completion = client.chat.completions.create(
                messages=historial,
                model=modelo,
            )
            
            respuesta_texto = chat_completion.choices[0].message.content
            historial.append({'role': 'assistant', 'content': respuesta_texto})
            return respuesta_texto
            
        except Exception as e:
            ultimo_error = e
            continue  # Si falla el modelo actual, prueba el siguiente de la lista

    return f"❌ Error al conectar con la IA: {ultimo_error}"

def reiniciar_historial():
    """Limpia el historial de la conversación."""
    global historial
    historial = [
        {'role': 'system', 'content': PERSONALIDADES[modo_actual] + REGLAS_FORMATO}
    ]

def cambiar_personalidad(nuevo_modo):
    """Cambia el modo/personalidad del bot."""
    global modo_actual, historial
    if nuevo_modo in PERSONALIDADES:
        modo_actual = nuevo_modo
        reiniciar_historial()
        return True
    return False

def guardar_recomendaciones():
    """Función auxiliar para guardar o exportar recomendaciones."""
    return True
