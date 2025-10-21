from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.core.audio import SoundLoader
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.core.window import Window
import time

# Configurar el tamaño de la ventana para que sea más compacta
Window.size = (400, 535)  # Ventana más compacta

class CoffeeSimulator(BoxLayout):
    message_text = StringProperty("- Selecciona tu tipo de café -")
    current_coffee = StringProperty("")
    
    def __init__(self, **kwargs):
        super(CoffeeSimulator, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10  # Reducir padding
        self.spacing = 5   # Reducir espaciado al mínimo
        
        # Configurar el color de fondo
        with self.canvas.before:
            Color(0.82, 0.59, 0.09, 1)  # #D19617 en RGB
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        # Cargar sonidos
        self.coffee_sound = self.load_sound("sounds/coffe_sound.mp3")
        self.sugar_sound = self.load_sound("sounds/suggar_sound.mp3")
        
        # Cargar imágenes (en Kivy usamos rutas directas)
        self.coffee_machine_image = "images/image.png"
        self.milk_image = "images/añadir_leche.png"
        self.sugar_image = "images/añadir_azucar.png"
        
        # Diccionario de imágenes de café preparado
        self.coffee_images = {
            "Espresso": "images/cafe_espresso.png",
            "Cappuccino": "images/cafe_cappuccino.png",
            "Latte": "images/cafe_latte.png",
            "Americano": "images/cafe_americano.png",
            "Mocha": "images/cafe_mocha.png"
        }
        
        # Duración de los sonidos
        self.sound_duration_coffee = 5
        self.sound_duration_sugar = 3
        
        # Crear la interfaz
        self.create_interface()
    
    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos
    
    def load_sound(self, filename):
        try:
            sound = SoundLoader.load(filename)
            if sound:
                sound.volume = 1.0
            return sound
        except:
            print(f"No se pudo cargar el sonido: {filename}")
            return None
    
    def create_interface(self):
        # ROW 0: TÍTULO (más compacto)
        title = Label(
            text="Simulador de Café Virtual",
            font_size=20,  # Reducir tamaño de fuente
            size_hint_y=None,
            height=30,     # Reducir altura
            color=(0.93, 0.94, 0.95, 1)
        )
        self.add_widget(title)
        
        # ROW 1: IMAGEN (más compacta)
        self.coffee_image = Image(
            source=self.coffee_machine_image,
            size_hint=(1, None),
            height=150,    # Reducir altura de la imagen
            allow_stretch=True,
            keep_ratio=True
        )
        self.add_widget(self.coffee_image)
        
        # ROW 2: MENSAJE (más compacto)
        self.message_label = Label(
            text=self.message_text,
            font_size=18,  # Reducir tamaño de fuente
            size_hint_y=None,
            height=25,     # Reducir altura
            color=(0.93, 0.94, 0.95, 1)
        )
        self.bind(message_text=lambda instance, value: setattr(self.message_label, 'text', value))
        self.add_widget(self.message_label)
        
        # ROW 3: TÍTULO ADICIONES (más compacto)
        additions_title = Label(
            text="- Adiciones -", 
            font_size=16, 
            size_hint_y=None, 
            height=20,     # Reducir altura
            color=(0.93, 0.94, 0.95, 1)
        )
        self.add_widget(additions_title)
        
        # ROW 4: BOTONES DE ADICIONES (en horizontal, más compactos)
        additions_layout = BoxLayout(
            orientation='horizontal', 
            size_hint_y=None, 
            height=40,     # Reducir altura
            spacing=5      # Reducir espaciado
        )
        
        # Botón de añadir leche
        milk_btn = Button(
            text="Añadir Leche",
            size_hint=(0.5, 1),
            background_color=(0.35, 0.27, 0.02, 1),
            color=(0.93, 0.94, 0.95, 1),
            font_size=12   # Reducir tamaño de fuente
        )
        milk_btn.bind(on_press=lambda instance: self.add_milk())
        additions_layout.add_widget(milk_btn)
        
        # Botón de añadir azúcar
        sugar_btn = Button(
            text="Añadir Azúcar",
            size_hint=(0.5, 1),
            background_color=(0.35, 0.27, 0.02, 1),
            color=(0.93, 0.94, 0.95, 1),
            font_size=12   # Reducir tamaño de fuente
        )
        sugar_btn.bind(on_press=lambda instance: self.add_sugar())
        additions_layout.add_widget(sugar_btn)
        
        self.add_widget(additions_layout)
        
        # ROW 5: TÍTULO CAFÉS (más compacto)
        coffee_title = Label(
            text="- Cafés -", 
            font_size=16, 
            size_hint_y=None, 
            height=20,     # Reducir altura
            color=(0.93, 0.94, 0.95, 1)
        )
        self.add_widget(coffee_title)
        
        # ROWS 6-10: BOTONES DE CAFÉ (más compactos)
        coffee_types = ["Espresso", "Cappuccino", "Latte", "Americano", "Mocha"]
        for coffee in coffee_types:
            btn = Button(
                text=f"Preparar {coffee}",
                size_hint_y=None, 
                height=35,     # Reducir altura
                background_color=(0.35, 0.27, 0.02, 1),
                color=(0.93, 0.94, 0.95, 1),
                font_size=12   # Reducir tamaño de fuente
            )
            btn.bind(on_press=lambda instance, c=coffee: self.prepare_coffee(c))
            self.add_widget(btn)
    
    def prepare_coffee(self, coffee_type):
        self._update_image(self.coffee_machine_image)
        self.message_text = f"Preparando {coffee_type}..."
        Clock.schedule_once(lambda dt: self._play_coffee_sound_and_finish(coffee_type), 0.1)
    
    def _play_coffee_sound_and_finish(self, coffee_type):
        if self.coffee_sound:
            self.coffee_sound.play()
            Clock.schedule_once(lambda dt: self._finish_coffee_preparation(coffee_type), self.sound_duration_coffee)
        else:
            Clock.schedule_once(lambda dt: self._finish_coffee_preparation(coffee_type), 5)
    
    def _finish_coffee_preparation(self, coffee_type):
        if coffee_type in self.coffee_images:
            self._update_image(self.coffee_images[coffee_type])
        self.message_text = f"¡Tu {coffee_type} virtual está listo!"
        self.show_alert("¡Listo!", f"¡Tu {coffee_type} virtual está listo!")
        self.current_coffee = coffee_type
    
    def add_milk(self):
        self._update_image(self.milk_image)
        self.message_text = "Añadiendo leche..."
        Clock.schedule_once(lambda dt: self._play_milk_sound_and_finish(), 0.1)
    
    def _play_milk_sound_and_finish(self):
        if self.coffee_sound:
            self.coffee_sound.play()
            Clock.schedule_once(lambda dt: self._finish_adding_milk(), self.sound_duration_coffee)
        else:
            Clock.schedule_once(lambda dt: self._finish_adding_milk(), 4)
    
    def _finish_adding_milk(self):
        if self.current_coffee and self.current_coffee in self.coffee_images:
            self._update_image(self.coffee_images[self.current_coffee])
        else:
            self._update_image(self.coffee_machine_image)
        self.message_text = "¡Leche añadida!"
    
    def add_sugar(self):
        self._update_image(self.sugar_image)
        self.message_text = "Añadiendo azúcar..."
        Clock.schedule_once(lambda dt: self._play_sugar_sound_and_finish(), 0.1)
    
    def _play_sugar_sound_and_finish(self):
        if self.sugar_sound:
            self.sugar_sound.play()
            Clock.schedule_once(lambda dt: self._finish_adding_sugar(), self.sound_duration_sugar)
        else:
            Clock.schedule_once(lambda dt: self._finish_adding_sugar(), 2)
    
    def _finish_adding_sugar(self):
        if self.current_coffee and self.current_coffee in self.coffee_images:
            self._update_image(self.coffee_images[self.current_coffee])
        else:
            self._update_image(self.coffee_machine_image)
        self.message_text = "¡Azúcar añadido!"
    
    def _update_image(self, image_path):
        self.coffee_image.source = image_path
        try:
            self.coffee_image.reload()
        except:
            print(f"No se pudo cargar la imagen: {image_path}")
    
    def show_alert(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.7, 0.4))
        popup.open()

class CoffeeApp(App):
    def build(self):
        return CoffeeSimulator()

if __name__ == '__main__':
    CoffeeApp().run()