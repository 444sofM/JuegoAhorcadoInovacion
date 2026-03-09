import tkinter as tk
from tkinter import messagebox, ttk
import random

# Conjunto de palabras para el juego
PALABRAS = [
    "PYTHON", "PROGRAMACION", "COMPUTADORA", "DESARROLLO", "JUEGO",
    "AHORCADO", "CODIGO", "VARIABLE", "FUNCION", "CLASE",
    "OBJETO", "ALGORITMO", "DATOS", "ARCHIVO", "SISTEMA",
    "INTERNET", "TECLADO", "PANTALLA", "SOFTWARE", "HARDWARE"
]

class JuegoAhorcado:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Juego del Ahorcado")
        self.root.geometry("900x700")  # Ventana más pequeña
        self.root.configure(bg="#1a1a2e")
        self.root.resizable(True, True)  # Permitir redimensionar
        
        self.palabra = ""
        self.letras_adivinadas = set()
        self.intentos_fallidos = 0
        self.max_intentos = 6
        self.botones_letras = {}
        
        self.crear_interfaz_con_scroll()
        self.nuevo_juego()
    
    def crear_interfaz_con_scroll(self):
        # Canvas principal con scrollbar
        main_canvas = tk.Canvas(self.root, bg="#1a1a2e", highlightthickness=0)
        
        # Scrollbar personalizada
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Vertical.TScrollbar", 
                       background="#16213e",
                       troughcolor="#0f3460",
                       bordercolor="#1a1a2e",
                       arrowcolor="#00d4ff")
        
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        
        # Frame scrollable
        self.scrollable_frame = tk.Frame(main_canvas, bg="#1a1a2e")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        # Centrar el frame en el canvas
        canvas_window = main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n")
        
        def center_window(event):
            canvas_width = event.width
            main_canvas.coords(canvas_window, canvas_width // 2, 0)
        
        main_canvas.bind("<Configure>", center_window)
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar canvas y scrollbar
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        main_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Crear contenido
        self.crear_contenido()
    
    def crear_contenido(self):
        # Espaciado superior reducido
        tk.Label(self.scrollable_frame, text="", bg="#1a1a2e", height=1).pack()
        
        # Contenedor principal con borde decorativo - más compacto
        main_container = tk.Frame(self.scrollable_frame, bg="#16213e", relief="ridge", bd=3)
        main_container.pack(anchor="center", padx=30, pady=10)
        
        # Espaciado interno reducido
        tk.Label(main_container, text="", bg="#16213e", height=1).pack()
        
        # Título con efecto de sombra - más pequeño
        titulo_shadow = tk.Label(
            main_container,
            text="🎮 EL AHORCADO 🎮",
            font=("Arial Black", 32, "bold"),
            bg="#16213e",
            fg="#0a0a0a"
        )
        titulo_shadow.pack(anchor="center", pady=(10, 0))
        
        titulo = tk.Label(
            main_container,
            text="🎮 EL AHORCADO 🎮",
            font=("Arial Black", 32, "bold"),
            bg="#16213e",
            fg="#00d4ff"
        )
        titulo.pack(anchor="center", pady=(0, 5))
        
        # Subtítulo más pequeño
        subtitulo = tk.Label(
            main_container,
            text="¡Adivina la palabra antes de que sea tarde!",
            font=("Arial", 11, "italic"),
            bg="#16213e",
            fg="#e94560"
        )
        subtitulo.pack(anchor="center", pady=(0, 10))
        
        # Frame para el canvas con borde - más pequeño
        canvas_frame = tk.Frame(main_container, bg="#0f3460", relief="solid", bd=2)
        canvas_frame.pack(anchor="center", pady=10)
        
        self.canvas = tk.Canvas(
            canvas_frame,
            width=320,
            height=260,
            bg="#16213e",
            highlightthickness=0
        )
        self.canvas.pack(padx=5, pady=5)
        
        # Frame para la palabra con efecto - más compacto
        palabra_frame = tk.Frame(main_container, bg="#0f3460", relief="solid", bd=2)
        palabra_frame.pack(anchor="center", pady=10, padx=30)
        
        self.label_palabra = tk.Label(
            palabra_frame,
            text="",
            font=("Courier New", 28, "bold"),
            bg="#0f3460",
            fg="#00d4ff",
            height=2,
            padx=20
        )
        self.label_palabra.pack()
        
        # Label para intentos con estilo - más pequeño
        intentos_frame = tk.Frame(main_container, bg="#16213e")
        intentos_frame.pack(anchor="center", pady=8)
        
        self.label_intentos = tk.Label(
            intentos_frame,
            text="",
            font=("Arial", 14, "bold"),
            bg="#16213e",
            fg="#e94560"
        )
        self.label_intentos.pack()
        
        # Separador decorativo
        separator = tk.Frame(main_container, bg="#00d4ff", height=2)
        separator.pack(fill="x", padx=40, pady=12)
        
        # Label para instrucciones - más pequeño
        instrucciones = tk.Label(
            main_container,
            text="Selecciona una letra:",
            font=("Arial", 13, "bold"),
            bg="#16213e",
            fg="#ffffff"
        )
        instrucciones.pack(anchor="center", pady=(5, 10))
        
        # Frame para los botones de letras con fondo - más compacto
        frame_letras_bg = tk.Frame(main_container, bg="#0f3460", relief="solid", bd=2)
        frame_letras_bg.pack(anchor="center", pady=8)
        
        frame_letras_container = tk.Frame(frame_letras_bg, bg="#0f3460")
        frame_letras_container.pack(padx=15, pady=15)
        
        # Crear botones para cada letra del abecedario - más pequeños
        letras = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        fila = 0
        columna = 0
        
        for letra in letras:
            btn = tk.Button(
                frame_letras_container,
                text=letra,
                font=("Arial", 13, "bold"),
                width=4,
                height=2,
                bg="#00d4ff",
                fg="#1a1a2e",
                activebackground="#00a8cc",
                activeforeground="#ffffff",
                cursor="hand2",
                relief="raised",
                bd=3,
                command=lambda l=letra: self.adivinar_letra(l)
            )
            btn.grid(row=fila, column=columna, padx=5, pady=5)
            
            # Efecto hover
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#00a8cc", fg="#ffffff"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#00d4ff", fg="#1a1a2e") if b['state'] == 'normal' else None)
            
            self.botones_letras[letra] = btn
            
            columna += 1
            if columna > 6:
                columna = 0
                fila += 1
        
        tk.Label(main_container, text="", bg="#16213e", height=1).pack()
        
        # Botón de nuevo juego con estilo mejorado - más compacto
        btn_nuevo = tk.Button(
            main_container,
            text="🔄 NUEVO JUEGO",
            font=("Arial", 15, "bold"),
            bg="#e94560",
            fg="white",
            activebackground="#c23a4f",
            activeforeground="#ffffff",
            cursor="hand2",
            relief="raised",
            bd=4,
            command=self.nuevo_juego,
            padx=30,
            pady=12
        )
        btn_nuevo.pack(anchor="center", pady=15)
        
        # Efecto hover para botón nuevo juego
        btn_nuevo.bind("<Enter>", lambda e: btn_nuevo.config(bg="#c23a4f"))
        btn_nuevo.bind("<Leave>", lambda e: btn_nuevo.config(bg="#e94560"))
        
        # Espaciado final reducido
        tk.Label(main_container, text="", bg="#16213e", height=1).pack()
        
        # Espacio adicional al final
        tk.Label(self.scrollable_frame, text="", bg="#1a1a2e", height=2).pack()
    
    def dibujar_ahorcado(self):
        """Dibuja el ahorcado según los intentos fallidos con mejor diseño"""
        self.canvas.delete("all")
        
        # Base con sombra - ajustado para canvas más pequeño
        self.canvas.create_line(50, 235, 150, 235, width=5, fill="#444444")
        self.canvas.create_line(50, 230, 150, 230, width=6, fill="#00d4ff")
        
        # Poste vertical con degradado
        self.canvas.create_line(100, 230, 100, 50, width=6, fill="#444444")
        self.canvas.create_line(98, 230, 98, 50, width=8, fill="#00d4ff")
        
        # Poste horizontal
        self.canvas.create_line(98, 50, 200, 50, width=6, fill="#444444")
        self.canvas.create_line(98, 48, 200, 48, width=8, fill="#00d4ff")
        
        # Cuerda
        self.canvas.create_line(200, 48, 200, 85, width=4, fill="#e94560")
        
        if self.intentos_fallidos >= 1:
            # Cabeza con detalles
            self.canvas.create_oval(180, 85, 220, 125, width=4, outline="#e94560", fill="#16213e")
            # Ojos X
            self.canvas.create_line(188, 98, 193, 103, width=3, fill="#ff6b6b")
            self.canvas.create_line(193, 98, 188, 103, width=3, fill="#ff6b6b")
            self.canvas.create_line(207, 98, 212, 103, width=3, fill="#ff6b6b")
            self.canvas.create_line(212, 98, 207, 103, width=3, fill="#ff6b6b")
        
        if self.intentos_fallidos >= 2:
            # Cuerpo
            self.canvas.create_line(200, 125, 200, 180, width=5, fill="#e94560")
        
        if self.intentos_fallidos >= 3:
            # Brazo izquierdo
            self.canvas.create_line(200, 140, 175, 160, width=4, fill="#e94560")
        
        if self.intentos_fallidos >= 4:
            # Brazo derecho
            self.canvas.create_line(200, 140, 225, 160, width=4, fill="#e94560")
        
        if self.intentos_fallidos >= 5:
            # Pierna izquierda
            self.canvas.create_line(200, 180, 180, 215, width=4, fill="#e94560")
        
        if self.intentos_fallidos >= 6:
            # Pierna derecha
            self.canvas.create_line(200, 180, 220, 215, width=4, fill="#e94560")
    
    def actualizar_palabra(self):
        """Actualiza la visualización de la palabra"""
        palabra_mostrada = ""
        for letra in self.palabra:
            if letra in self.letras_adivinadas:
                palabra_mostrada += letra + " "
            else:
                palabra_mostrada += "_ "
        
        self.label_palabra.config(text=palabra_mostrada)
    
    def actualizar_intentos(self):
        """Actualiza el contador de intentos"""
        self.label_intentos.config(
            text=f"💀 Intentos fallidos: {self.intentos_fallidos}/{self.max_intentos}"
        )
    
    def adivinar_letra(self, letra):
        """Procesa el intento de adivinar una letra"""
        if letra in self.letras_adivinadas:
            return
        
        self.letras_adivinadas.add(letra)
        btn = self.botones_letras[letra]
        
        if letra in self.palabra:
            # Letra correcta - verde
            btn.config(state="disabled", bg="#2ecc71", fg="white", relief="sunken")
            self.actualizar_palabra()
            self.verificar_victoria()
        else:
            # Letra incorrecta - rojo
            btn.config(state="disabled", bg="#95a5a6", fg="#444444", relief="sunken")
            self.intentos_fallidos += 1
            self.dibujar_ahorcado()
            self.actualizar_intentos()
            self.verificar_derrota()
    
    def verificar_victoria(self):
        """Verifica si el jugador ganó"""
        if all(letra in self.letras_adivinadas for letra in self.palabra):
            messagebox.showinfo(
                "¡VICTORIA! 🎉",
                f"¡FELICIDADES! ¡GANASTE!\n\n✨ La palabra era: '{self.palabra}' ✨\n\n¡Eres un campeón! 🏆"
            )
            self.deshabilitar_botones()
    
    def verificar_derrota(self):
        """Verifica si el jugador perdió"""
        if self.intentos_fallidos >= self.max_intentos:
            messagebox.showinfo(
                "Game Over 💀",
                f"¡Oh no! Te quedaste sin intentos.\n\n😢 La palabra era: '{self.palabra}'\n\n¡Intenta de nuevo! 💪"
            )
            self.deshabilitar_botones()
    
    def deshabilitar_botones(self):
        """Deshabilita todos los botones de letras"""
        for btn in self.botones_letras.values():
            if btn['state'] == 'normal':
                btn.config(state="disabled", bg="#95a5a6", fg="#444444")
    
    def nuevo_juego(self):
        """Inicia un nuevo juego"""
        self.palabra = random.choice(PALABRAS)
        self.letras_adivinadas = set()
        self.intentos_fallidos = 0
        
        # Rehabilitar y resetear botones
        for letra, btn in self.botones_letras.items():
            btn.config(state="normal", bg="#00d4ff", fg="#1a1a2e", relief="raised")
        
        # Actualizar interfaz
        self.dibujar_ahorcado()
        self.actualizar_palabra()
        self.actualizar_intentos()

def main():
    root = tk.Tk()
    juego = JuegoAhorcado(root)
    root.mainloop()

if __name__ == "__main__":
    main()
