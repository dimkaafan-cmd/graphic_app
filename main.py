from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
import numpy as np
import math

Window.size = (400, 700)

class GraphWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.function = "x**2"
        self.x_min = -5
        self.x_max = 5
        self.points = []
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        if self.width > 0 and self.height > 0:
            self.draw_graph()

    def set_function(self, func_text, x_min, x_max):
        try:
            self.function = self.parse_function(func_text)
            self.x_min = float(x_min)
            self.x_max = float(x_max)
            self.draw_graph()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def parse_function(self, text):
        text = text.strip()
        text = text.replace('^', '**')
        text = text.replace('sqrt', 'np.sqrt')
        text = text.replace('ln', 'np.log')
        text = text.replace('e^x', 'np.exp(x)')
        text = text.replace('sin(x)', 'np.sin(x)')
        text = text.replace('cos(x)', 'np.cos(x)')
        text = text.replace('tan(x)', 'np.tan(x)')
        text = text.replace('|x|', 'np.abs(x)')
        text = text.replace('x(x', 'x*(x')
        text = text.replace(')(x', ')*(x')
        text = text.replace(')(', ')*(')
        return text

    def calculate_function(self, x):
        try:
            safe_dict = {
                'np': np,
                'sin': np.sin,
                'cos': np.cos,
                'tan': np.tan,
                'sqrt': np.sqrt,
                'log': np.log,
                'exp': np.exp,
                'abs': np.abs,
                'x': x
            }
            return eval(self.function, {"__builtins__": {}}, safe_dict)
        except Exception as e:
            print(f"Calc error: {e}")
            return float('nan')

    def draw_graph(self):
        self.canvas.clear()

        if self.width == 0 or self.height == 0:
            return

        width, height = self.size

        with self.canvas:
            Color(1, 1, 1, 1)
            Rectangle(pos=self.pos, size=self.size)

            Color(0.7, 0.7, 0.7, 1)
            x_axis_y = self.y + height/2
            Line(points=[self.x, x_axis_y, self.x + width, x_axis_y], width=1)
            y_axis_x = self.x + width/2
            Line(points=[y_axis_x, self.y, y_axis_x, self.y + height], width=1)

        points = []
        valid_y_values = []

        num_points = min(200, int(width))

        for i in range(num_points):
            x_pixel = self.x + (i * width / num_points)
            x_value = self.x_min + (i / num_points) * (self.x_max - self.x_min)

            try:
                y_value = self.calculate_function(x_value)
                if not np.isnan(y_value) and not np.isinf(y_value):
                    valid_y_values.append(y_value)

                    if len(valid_y_values) > 1:
                        y_min = min(valid_y_values)
                        y_max = max(valid_y_values)
                        if y_max - y_min > 1e-10:
                            y_normalized = (y_value - y_min) / (y_max - y_min)
                        else:
                            y_normalized = 0.5
                    else:
                        y_normalized = 0.5

                    y_pixel = self.y + height - (y_normalized * height)
                    points.append(x_pixel)
                    points.append(y_pixel)
            except:
                continue

        if len(points) > 2:
            with self.canvas:
                Color(0.2, 0.4, 0.8, 1)
                Line(points=points, width=1.5)

class GraphingApp(App):
    def build(self):
        self.title = "Графики функций"

        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5))

        input_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.08))
        input_layout.add_widget(Label(text='y =', size_hint=(0.15, 1), font_size=dp(16)))
        self.function_input = TextInput(
            text='x**2',
            multiline=False,
            size_hint=(0.85, 1),
            font_size=dp(16),
            background_color=get_color_from_hex('#FFFFFF')
        )
        input_layout.add_widget(self.function_input)
        main_layout.add_widget(input_layout)

        hint_label = Label(
            text='(sqrt(x), x**2, sin(x), x*(x-5)+7)',
            size_hint=(1, 0.05),
            font_size=dp(12),
            color=get_color_from_hex('#666666')
        )
        main_layout.add_widget(hint_label)

        range_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.08))
        range_layout.add_widget(Label(text='x от:', size_hint=(0.2, 1), font_size=dp(14)))
        self.x_min_input = TextInput(text='-5', multiline=False, size_hint=(0.2, 1), font_size=dp(14))
        range_layout.add_widget(self.x_min_input)
        range_layout.add_widget(Label(text='до:', size_hint=(0.1, 1), font_size=dp(14)))
        self.x_max_input = TextInput(text='5', multiline=False, size_hint=(0.2, 1), font_size=dp(14))
        range_layout.add_widget(self.x_max_input)

        self.plot_button = Button(
            text='Построить',
            size_hint=(0.3, 1),
            background_color=get_color_from_hex('#4CAF50'),
            color=get_color_from_hex('#FFFFFF'),
            font_size=dp(14)
        )
        self.plot_button.bind(on_press=self.plot_function)
        range_layout.add_widget(self.plot_button)

        main_layout.add_widget(range_layout)

        buttons_label = Label(text='Примеры функций:', size_hint=(1, 0.05), font_size=dp(14))
        main_layout.add_widget(buttons_label)

        scroll = ScrollView(size_hint=(1, 0.3))
        buttons_layout = GridLayout(cols=3, size_hint_y=None, spacing=dp(5))
        buttons_layout.bind(minimum_height=buttons_layout.setter('height'))

        examples = ['x**2', 'np.sin(x)', 'np.cos(x)', 'np.exp(x)', 'np.log(np.abs(x))',
                   'x**3-3*x', 'np.sqrt(x)', 'np.tan(x)', 'x**2+2*x+1', '2*x**2-3*x+1',
                   'x*(x-5)+7', '(x-1)*(x+2)', '1/(x+1e-10)', 'np.abs(x)']

        display_names = ['x^2', 'sin(x)', 'cos(x)', 'e^x', 'ln|x|', 'x^3-3x',
                        'sqrt(x)', 'tan(x)', 'x^2+2x+1', '2x^2-3x+1', 'x(x-5)+7',
                        '(x-1)(x+2)', '1/x', '|x|']

        for i, example in enumerate(examples):
            btn = Button(
                text=display_names[i],
                size_hint_y=None,
                height=dp(40),
                font_size=dp(12),
                background_color=get_color_from_hex('#2196F3'),
                color=get_color_from_hex('#FFFFFF')
            )
            btn.bind(on_press=lambda instance, ex=example: self.set_example(ex, display_names[examples.index(ex)]))
            buttons_layout.add_widget(btn)

        scroll.add_widget(buttons_layout)
        main_layout.add_widget(scroll)

        self.graph = GraphWidget(size_hint=(1, 0.4))
        main_layout.add_widget(self.graph)

        self.status_label = Label(text='Введите функцию', size_hint=(1, 0.05), font_size=dp(12))
        main_layout.add_widget(self.status_label)

        return main_layout

    def set_example(self, example, display_name):
        self.function_input.text = display_name
        self.plot_function()

    def plot_function(self, *args):
        try:
            func_text = self.function_input.text
            x_min = self.x_min_input.text
            x_max = self.x_max_input.text

            success = self.graph.set_function(func_text, x_min, x_max)
            if success:
                self.status_label.text = 'График построен!'
                self.status_label.color = get_color_from_hex('#388E3C')
            else:
                self.status_label.text = 'Ошибка в функции'
                self.status_label.color = get_color_from_hex('#D32F2F')

        except Exception as e:
            self.status_label.text = f'Ошибка: {str(e)}'
            self.status_label.color = get_color_from_hex('#D32F2F')

if __name__ == '__main__':
    GraphingApp().run()