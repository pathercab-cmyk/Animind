from recomendador import (
    obtener_recomendacion, 
    reiniciar_historial, 
    cambiar_personalidad, 
    guardar_recomendaciones,
    modo_actual
)

def mostrar_ayuda():
    print("""
📌 COMANDOS DISPONIBLES:
-------------------------------------------
 /limpiar o /reset  -> Borra la memoria del chat.
 /guardar           -> Exporta las recomendaciones a 'mis_recomendaciones.txt'.
 /modo <tipo>       -> Cambia de personalidad (entusiasta, tsundere, analista).
 /ayuda             -> Muestra esta lista de comandos.
 salir              -> Cierra la aplicación.
-------------------------------------------""")

def iniciar_consola():
    print("===========================================")
    print(" 🎌 ¡Senpai-Bot Local con Comandos! 🎌")
    print(" Escribe '/ayuda' para ver los comandos.")
    print("===========================================\n")

    while True:
        peticion = input("Tú: ").strip()
        
        if not peticion:
            continue
            
        # Control de salida
        if peticion.lower() in ["salir", "exit", "chao", "adios"]:
            print("\nSenpai-Bot: ¡Matane! 👋 Nos vemos en el club de anime.")
            break
            
        # Comando: Ayuda
        if peticion.lower() == "/ayuda":
            mostrar_ayuda()
            continue
            
        # Comando: Limpiar/Reset
        if peticion.lower() in ["/limpiar", "/reset"]:
            reiniciar_historial()
            print("\n🧹 Memoria reiniciada con éxito. ¡Empieza una nueva charla!\n")
            continue
            
        # Comando: Guardar
        if peticion.lower() == "/guardar":
            res = guardar_recomendaciones()
            print(f"\n{res}\n")
            continue
            
        # Comando: Cambiar Modo
        if peticion.lower().startswith("/modo"):
            partes = peticion.split()
            if len(partes) > 1:
                nuevo_modo = partes[1].lower()
                if cambiar_personalidad(nuevo_modo):
                    print(f"\n🎭 Personalidad cambiada a '{nuevo_modo.upper()}'. Memoria reiniciada.\n")
                else:
                    print("\n❌ Modo no válido. Opciones: entusiasta, tsundere, analista\n")
            else:
                print("\n⚠️ Uso correcto: /modo entusiasta | /modo tsundere | /modo analista\n")
            continue

        # Proceso estándar
        print("\n🤖 Senpai-Bot pensando...")
        respuesta = obtener_recomendacion(peticion)
        print(f"\nSenpai-Bot:\n{respuesta}\n")
        print("-" * 40)

if __name__ == "__main__":
    iniciar_consola()