import random

# Conjunto de palabras para el juego
PALABRAS = [
    "python", "programacion", "computadora", "desarrollo", "juego",
    "ahorcado", "codigo", "variable", "funcion", "clase",
    "objeto", "algoritmo", "datos", "archivo", "sistema",
    "internet", "teclado", "pantalla", "software", "hardware"
]

# Dibujos del ahorcado
AHORCADO = [
    """
       ------
       |    |
       |
       |
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |    |
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   /
       |
    --------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   / \\
       |
    --------
    """
]

def seleccionar_palabra():
    """Selecciona una palabra al azar del conjunto"""
    return random.choice(PALABRAS).upper()

def mostrar_estado(palabra, letras_adivinadas, intentos_fallidos):
    """Muestra el estado actual del juego"""
    print("\n" + AHORCADO[intentos_fallidos])
    
    # Mostrar palabra con letras adivinadas
    palabra_mostrada = ""
    for letra in palabra:
        if letra in letras_adivinadas:
            palabra_mostrada += letra + " "
        else:
            palabra_mostrada += "_ "
    
    print(f"\nPalabra: {palabra_mostrada}")
    print(f"Intentos fallidos: {intentos_fallidos}/6")
    
    if letras_adivinadas:
        print(f"Letras usadas: {', '.join(sorted(letras_adivinadas))}")

def jugar():
    """Función principal del juego"""
    print("=" * 40)
    print("   BIENVENIDO AL JUEGO DEL AHORCADO")
    print("=" * 40)
    
    palabra = seleccionar_palabra()
    letras_adivinadas = set()
    intentos_fallidos = 0
    max_intentos = 6
    
    while intentos_fallidos < max_intentos:
        mostrar_estado(palabra, letras_adivinadas, intentos_fallidos)
        
        # Verificar si ganó
        if all(letra in letras_adivinadas for letra in palabra):
            print("\n" + "=" * 40)
            print(f"   ¡FELICIDADES! ¡GANASTE! 🎉")
            print(f"   La palabra era: {palabra}")
            print("=" * 40)
            return
        
        # Pedir letra al jugador
        letra = input("\nIngresa una letra: ").upper()
        
        # Validar entrada
        if len(letra) != 1 or not letra.isalpha():
            print("Por favor ingresa solo una letra válida.")
            continue
        
        if letra in letras_adivinadas:
            print("Ya usaste esa letra. Intenta con otra.")
            continue
        
        letras_adivinadas.add(letra)
        
        # Verificar si la letra está en la palabra
        if letra in palabra:
            print(f"¡Bien! La letra '{letra}' está en la palabra.")
        else:
            intentos_fallidos += 1
            print(f"Lo siento, la letra '{letra}' no está en la palabra.")
    
    # Perdió el juego
    mostrar_estado(palabra, letras_adivinadas, intentos_fallidos)
    print("\n" + "=" * 40)
    print(f"   GAME OVER 😢")
    print(f"   La palabra era: {palabra}")
    print("=" * 40)

def main():
    """Función principal con opción de jugar múltiples veces"""
    while True:
        jugar()
        
        respuesta = input("\n¿Quieres jugar otra vez? (s/n): ").lower()
        if respuesta != 's':
            print("\n¡Gracias por jugar! Hasta pronto. 👋")
            break

if __name__ == "__main__":
    main()
