from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle


class Principal(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.contador_limpiar = 0
        self.campo_activo = None

        # --- FONDO DE LA PANTALLA ---
        with self.canvas.before:
            Color(0.92, 0.92, 0.98, 1)  # Morado pastel fijo
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._actualizar_fondo, pos=self._actualizar_fondo)

        # ScrollView principal para evitar que los elementos se aplasten en pantallas pequeñas
        scroll_principal = ScrollView(do_scroll_x=False, do_scroll_y=True)

        # Contenedor raíz centrado y con un ancho máximo adaptable
        contenedor_raiz = MDBoxLayout(
            orientation="vertical",
            padding=[16, 20, 16, 20],
            spacing=16,
            size_hint_y=None,
            pos_hint={"center_x": 0.5, "top": 1}
        )
        contenedor_raiz.bind(minimum_height=contenedor_raiz.setter('height'))

        # Título de la app
        titulo = MDLabel(
            text="Calculadora Dual",
            halign="center",
            font_style="H6",
            bold=True,
            theme_text_color="Custom",
            text_color="#000000",  
            size_hint_y=None,
            height=40
        )
        contenedor_raiz.add_widget(titulo)

        # Bloque de entrada de números (Cambiado a adaptable en lugar de altura fija rígida)
        bloque_superior = MDBoxLayout(
            orientation="vertical",
            spacing=12,
            size_hint_y=None
        )
        bloque_superior.bind(minimum_height=bloque_superior.setter('height'))

        # Campos de texto
        self.num1 = MDTextField(
            hint_text="Número 1",
            icon_left="numeric-1-box-outline",
            mode="rectangle",
            line_color_focus="#7F2DCC",
            hint_text_color_focus="#7F2DCC",
            text_color_normal="#000000",
            text_color_focus="#000000",
            readonly=True
        )
        self.num1.bind(on_touch_down=self.seleccionar_campo)

        self.num2 = MDTextField(
            hint_text="Número 2",
            icon_left="numeric-2-box-outline",
            mode="rectangle",
            line_color_focus="#7F2DCC",
            hint_text_color_focus="#7F2DCC",
            text_color_normal="#000000",
            text_color_focus="#000000",
            readonly=True
        )
        self.num2.bind(on_touch_down=self.seleccionar_campo)

        bloque_superior.add_widget(self.num1)
        bloque_superior.add_widget(self.num2)
        contenedor_raiz.add_widget(bloque_superior)

        self.campo_activo = self.num1

        # Rejilla del Teclado (Fijamos una altura cómoda en píxeles para que los botones mantengan su forma física)
        rejilla_teclado = MDGridLayout(
            cols=4,
            spacing=8,
            size_hint_y=None,
            height=280  # Altura perfecta para un teclado táctil móvil
        )

        botones_config = [
            ("7", "#000000", self.presionar_numero), ("8", "#000000", self.presionar_numero), ("9", "#000000", self.presionar_numero), ("Sumar", "#B283D1", self.sumar),
            ("4", "#000000", self.presionar_numero), ("5", "#000000", self.presionar_numero), ("6", "#000000", self.presionar_numero), ("Restar", "#B283D1", self.restar),
            ("1", "#000000", self.presionar_numero), ("2", "#000000", self.presionar_numero), ("3", "#000000", self.presionar_numero), ("Multiplicar", "#B283D1", self.multiplicar),
            (".", "#000000", self.presionar_numero), ("0", "#000000", self.presionar_numero), ("Limpiar", "#7F2DCC", self.limpiar), ("Dividir", "#B283D1", self.dividir),
            ("√", "#7C3AED", self.raiz), ("x²", "#7C3AED", self.potencia), ("%", "#7C3AED", self.porcentaje), ("", "#000000", None)
        ]

        for texto, color, funcion in botones_config:
            if texto == "":
                widget_vacio = MDBoxLayout()
                rejilla_teclado.add_widget(widget_vacio)
            else:
                btn = MDRaisedButton(
                    text=f"[b]{texto}[/b]",
                    md_bg_color=color,
                    size_hint=(1, 1),
                    on_press=funcion
                )
                rejilla_teclado.add_widget(btn)
        
        contenedor_raiz.add_widget(rejilla_teclado)

        # Sección de Resultados e Historial
        bloque_inferior = MDBoxLayout(
            orientation="vertical",
            spacing=6,
            size_hint_y=None,
            height=180 # Espacio fijo garantizado para las respuestas
        )

        self.resultado = MDLabel(
            text="Resultado:",
            halign="center",
            font_style="H6",
            bold=True,
            theme_text_color="Custom",
            text_color="#000000",  
            size_hint_y=None,
            height=32
        )

        historial_titulo = MDLabel(
            text="Historial de operaciones:",
            halign="left",
            font_style="Subtitle2",
            theme_text_color="Custom",
            text_color="#5D636D",  
            size_hint_y=None,
            height=20
        )

        caja_scroll = MDBoxLayout(padding=[8, 8, 8, 8])
        with caja_scroll.canvas.before:
            Color(1, 1, 1, 0.6) 
            self.rect_scroll = Rectangle(size=caja_scroll.size, pos=caja_scroll.pos)
        caja_scroll.bind(size=self._actualizar_fondo_scroll, pos=self._actualizar_fondo_scroll)

        scroll_historial = ScrollView(bar_width=4)

        self.historial = MDLabel(
            text="",
            size_hint_y=None,
            valign="top",
            halign="left",
            theme_text_color="Custom",
            text_color="#1C2028",  
            font_style="Body2"
        )
        self.historial.bind(texture_size=self.actualizar_altura)
        
        scroll_historial.add_widget(self.historial)
        caja_scroll.add_widget(scroll_historial)

        bloque_inferior.add_widget(self.resultado)
        bloque_inferior.add_widget(historial_titulo)
        bloque_inferior.add_widget(caja_scroll)
        
        contenedor_raiz.add_widget(bloque_inferior)
        
        scroll_principal.add_widget(contenedor_raiz)
        self.add_widget(scroll_principal)

    def _actualizar_fondo(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def _actualizar_fondo_scroll(self, instance, value):
        self.rect_scroll.size = instance.size
        self.rect_scroll.pos = instance.pos

    def seleccionar_campo(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.campo_activo = instance

    def presionar_numero(self, instance):
        texto_limpio = instance.text.replace("[b]", "").replace("[/b]", "").strip()
        if self.campo_activo:
            self.campo_activo.text += texto_limpio

    def actualizar_altura(self, instance, value):
        instance.height = value[1]

    def formatear(self, numero):
        if numero == int(numero):
            return str(int(numero))
        return str(numero)

    def obtener_numeros(self):
        try:
            n1 = float(self.num1.text)
            n2 = float(self.num2.text)
            return n1, n2
        except:
            self.resultado.text = "Resultado: Error de formato"
            return None, None

    def agregar_historial(self, texto):
        self.historial.text += f" •  {texto}\n"

    # ===== OPERACIONES =====
    def sumar(self, obj):
        self.contador_limpiar = 0
        n1, n2 = self.obtener_numeros()
        if n1 is not None:
            r = n1 + n2
            self.resultado.text = f"Resultado: {self.formatear(r)}"
            self.agregar_historial(f"{self.formatear(n1)} + {self.formatear(n2)} = {self.formatear(r)}")

    def evaluar_operacion(self, operacion, simbolo, n1, n2):
        r = operacion(n1, n2)
        self.resultado.text = f"Resultado: {self.formatear(r)}"
        self.agregar_historial(f"{self.formatear(n1)} {simbolo} {self.formatear(n2)} = {self.formatear(r)}")

    def restar(self, obj):
        self.contador_limpiar = 0
        n1, n2 = self.obtener_numeros()
        if n1 is not None:
            self.evaluar_operacion(lambda x, y: x - y, "-", n1, n2)

    def multiplicar(self, obj):
        self.contador_limpiar = 0
        n1, n2 = self.obtener_numeros()
        if n1 is not None:
            self.evaluar_operacion(lambda x, y: x * y, "×", n1, n2)

    def dividir(self, obj):
        self.contador_limpiar = 0
        n1, n2 = self.obtener_numeros()
        if n1 is not None:
            if n2 == 0:
                self.resultado.text = "Resultado: No se puede dividir por 0"
                return
            self.evaluar_operacion(lambda x, y: x / y, "÷", n1, n2)

    def raiz(self, obj):
        self.contador_limpiar = 0
        if self.campo_activo and self.campo_activo.text:
            try:
                n = float(self.campo_activo.text)
                if n < 0:
                    self.resultado.text = "Resultado: Raíz negativa"
                    return
                r = n ** 0.5
                self.resultado.text = f"Resultado: {self.formatear(r)}"
                self.agregar_historial(f"√{self.formatear(n)} = {self.formatear(r)}")
            except:
                self.resultado.text = "Resultado: Error"

    def potencia(self, obj):
        self.contador_limpiar = 0
        if self.campo_activo and self.campo_activo.text:
            try:
                n = float(self.campo_activo.text)
                r = n ** 2
                self.resultado.text = f"Resultado: {self.formatear(r)}"
                self.agregar_historial(f"{self.formatear(n)}² = {self.formatear(r)}")
            except:
                self.resultado.text = "Resultado: Error"

    def porcentaje(self, obj):
        self.contador_limpiar = 0
        n1, n2 = self.obtener_numeros()
        if n1 is not None:
            r = (n1 * n2) / 100
            self.resultado.text = f"Resultado: {self.formatear(r)}"
            self.agregar_historial(f"{self.formatear(n2)}% de {self.formatear(n1)} = {self.formatear(r)}")

    def limpiar(self, obj):
        self.contador_limpiar += 1
        if self.contador_limpiar == 1:
            self.resultado.text = "Resultado:"
            self.num1.text = ""
            self.num2.text = ""
        else:
            self.historial.text = ""
            self.resultado.text = "Resultado:"
            self.contador_limpiar = 0


class MiApp(MDApp):
    def build(self):
        self.theme_cls.theme_style_switch_animation = False
        self.theme_cls.theme_style = "Light"  
        self.theme_cls.primary_palette = "DeepPurple"

        sm = ScreenManager()
        sm.add_widget(Principal(name="principal"))
        return sm


if __name__ == "__main__":
    MiApp().run()
