import os
from groq import Groq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")
client = Groq(api_key=GROQ_API_KEY)

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
Tu lema es: "¡Un gusto conocerte, Senpai! 🙇‍♂ Soy AniMind, ¡tu IA personal de anime lista para dar lo mejor de sí!"
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
   - ⏱️ Duración y Género
   - 💡 Por qué te gustará / Punto fuerte
"""

modo_actual = "entusiasta"
historial = [
    {'role': 'system', 'content': PERSONALIDADES[modo_actual] + REGLAS_FORMATO}
]

def obtener_recomendacion(peticion_usuario):
    global historial
    historial.append({'role': 'user', 'content': peticion_usuario})
    
    try:
        chat_completion = client.chat.completions.create(
            messages=historial,
            model="llama-3.2-3b-preview",
        )
        
        respuesta_texto = chat_completion.choices[0].message.content
        historial.append({'role': 'assistant', 'content': respuesta_texto})
        return respuesta_texto
        
    except Exception as e:
        return f"❌ Error al conectar con la IA: {e}"

def reiniciar_historial():
    global historial
    historial = [
        {'role': 'system', 'content': PERSONALIDADES[modo_actual] + REGLAS_FORMATO}
    ]

def cambiar_personalidad(nuevo_modo):
    global modo_actual, historial
    if nuevo_modo in PERSONALIDADES:
        modo_actual = nuevo_modo
        reiniciar_historial()
        return True
    return False
