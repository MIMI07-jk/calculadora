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

        # Contenedor raíz con márgenes limpios en los bordes de la pantalla
        contenedor_raiz = MDBoxLayout(
            orientation="vertical",
            padding=[20, 15, 20, 15],
            spacing=10,  
            size_hint=(1, 1)
        )
        
        # Fondo morado pastel
        with contenedor_raiz.canvas.before:
            Color(0.95, 0.95, 0.98, 1) 
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        contenedor_raiz.bind(size=self._actualizar_fondo, pos=self._actualizar_fondo)

        # Título de la app (Separado correctamente)
        titulo = MDLabel(
            text="Calculadora Dual",
            halign="center",
            font_style="H5",
            bold=True,
            theme_text_color="Custom",
            text_color="#2D3748",  
            size_hint_y=None,
            height=50
        )
        contenedor_raiz.add_widget(titulo)

        # Bloque de entrada de números (Cambiado a tamaño proporcional para evitar que se pise con el título)
        bloque_superior = MDBoxLayout(
            orientation="vertical",
            spacing=10,
            size_hint_y=0.20  
        )

        self.num1 = MDTextField(
            hint_text="Número 1",
            icon_left="numeric-1-box-outline",
            mode="rectangle",
            line_color_focus="#7F2DCC",
            hint_text_color_focus="#7F2DCC",
            text_color_normal="#000000",
            text_color_focus="#000000",
            readonly=True,
            halign="center"
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
            readonly=True,
            halign="center"
        )
        self.num2.bind(on_touch_down=self.seleccionar_campo)

        bloque_superior.add_widget(self.num1)
        bloque_superior.add_widget(self.num2)
        contenedor_raiz.add_widget(bloque_superior)

        self.campo_activo = self.num1

        # Rejilla del Teclado
        rejilla_teclado = MDGridLayout(
            cols=4,
            spacing=6, 
            size_hint_y=0.45  
        )

        botones_config = [
            ("7", "#1A1D20", self.presionar_numero), ("8", "#1A1D20", self.presionar_numero), ("9", "#1A1D20", self.presionar_numero), ("Sumar", "#B283D1", self.sumar),
            ("4", "#1A1D20", self.presionar_numero), ("5", "#1A1D20", self.presionar_numero), ("6", "#1A1D20", self.presionar_numero), ("Restar", "#B283D1", self.restar),
            ("1", "#1A1D20", self.presionar_numero), ("2", "#1A1D20", self.presionar_numero), ("3", "#1A1D20", self.presionar_numero), ("Multiplicar", "#B283D1", self.multiplicar),
            (".", "#1A1D20", self.presionar_numero), ("0", "#1A1D20", self.presionar_numero), ("Limpiar", "#7F2DCC", self.limpiar), ("Dividir", "#B283D1", self.dividir),
            ("√", "#7C3AED", self.raiz), ("x²", "#7C3AED", self.potencia), ("%", "#7C3AED", self.porcentaje), ("C", "#7F2DCC", self.limpiar)
        ]

        for texto, color, funcion in botones_config:
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
            size_hint_y=0.25  
        )

        self.resultado = MDLabel(
            text="Resultado:",
            halign="center",
            font_style="H6",
            bold=True,
            theme_text_color="Custom",
            text_color="#1A202C",  
            size_hint_y=None,
            height=30
        )

        historial_titulo = MDLabel(
            text="Historial de operaciones:",
            halign="center",
            font_style="Subtitle2",
            theme_text_color="Custom",
            text_color="#718096",  
            size_hint_y=None,
            height=20
        )

        caja_scroll = MDBoxLayout(padding=[10, 10, 10, 10], size_hint_y=1)
        with caja_scroll.canvas.before:
            Color(1, 1, 1, 0.85) 
            self.rect_scroll = Rectangle(size=caja_scroll.size, pos=caja_scroll.pos)
        caja_scroll.bind(size=self._actualizar_fondo_scroll, pos=self._actualizar_fondo_scroll)

        scroll = ScrollView(bar_width=4)

        self.historial = MDLabel(
            text="",
            size_hint_y=None,
            valign="top",
            halign="center",
            theme_text_color="Custom",
            text_color="#2D3748",  
            font_style="Body1"
        )
        self.historial.bind(texture_size=self.actualizar_altura)
        
        scroll.add_widget(self.historial)
        caja_scroll.add_widget(scroll)

        bloque_inferior.add_widget(self.resultado)
        bloque_inferior.add_widget(historial_titulo)
        bloque_inferior.add_widget(caja_scroll)
        
        contenedor_raiz.add_widget(bloque_inferior)
        self.add_widget(contenedor_raiz)

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
        if texto_limpio in ["Sumar", "Restar", "Multiplicar", "Dividir", "Limpiar", "√", "x²", "%", "C"]:
            return
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
        self.historial.text += f"{texto}\n"

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
