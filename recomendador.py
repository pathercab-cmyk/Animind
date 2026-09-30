import os
from groq import Groq

MODELOS_DISPONIBLES = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant"
]

def obtener_recomendacion(mensaje_usuario, personalidad="otaku"):
    if personalidad == "critico":
        estilo_personalidad = "Eres AniMind, un crítico de anime analítico, exigente y reflexivo. Valoras la narrativa, la animación y el desarrollo de personajes de forma técnica pero accesible."
    elif personalidad == "sensei":
        estilo_personalidad = "Eres AniMind, un sabio maestro Sensei de anime. Respondes con serenidad, ofreciendo lecciones de vida y reflexiones profundas sobre las historias."
    else:
        estilo_personalidad = "Eres AniMind, una IA entusiasta, alegre, amigable y apasionada por el anime. Hablas con energía y usas algún emoji de forma moderada."

    prompt_sistema = f"""
{estilo_personalidad}

REGLAS DE FORMATO Y PRESENTACIÓN (CUMPLIR ESTRICTAMENTE):
1. PROHIBIDO usar asteriscos (*), almohadillas (#) o cualquier otro símbolo de marcado Markdown en tu respuesta.
2. Si el usuario pide recomendaciones, ofrece SIEMPRE 3 opciones variadas:
   - Opción Popular / Imprescindible
   - Joya Oculta / Poco conocida
   - Opción Diferente / Alternativa única

3. Presenta las recomendaciones de forma limpia con sangría de espacios (3 espacios) en los detalles de cada opción, de esta manera:

---
🌟 Título Principal (Español / Japonés)
   Duración y Géneros: [Detalles]
   ¿De qué trata?: [Sinopsis breve en 2 frases]
   ¿Por qué te gustará?: [Punto fuerte principal]
---
"""

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return "Error: No se ha encontrado la variable GROQ_API_KEY en las variables de entorno de Render."

    client = Groq(api_key=api_key)

    ultimo_error = ""
    for modelo in MODELOS_DISPONIBLES:
        try:
            completion = client.chat.completions.create(
                model=modelo,
                messages=[
                    {"role": "system", "content": prompt_sistema},
                    {"role": "user", "content": mensaje_usuario}
                ],
                temperature=0.7,
                max_tokens=1024
            )
            return completion.choices[0].message.content
        except Exception as e:
            ultimo_error = str(e)
            continue

    return f"Error al conectar con Groq: {ultimo_error}"
