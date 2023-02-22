import os
import csv
import time
import random
import string
import keyboard
import math

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


global csv_path

os.chdir(os.path.dirname(os.path.abspath(__file__)))

csv_path = "./count.csv"

print("[Q] quit, [R] reset, [S] save, [L] load")


def csv_exists():
    try:
        with open(csv_path, "r") as f:
            return True
    except FileNotFoundError:
        return False


def csv_read(row, column):
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        try:
            return float(list(reader)[row][column])
        except IndexError:
            return 0
        except FileNotFoundError:
            return create_csv()


def create_csv():
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([0, 0, time.time()])
        return 0


t_start = time.time() if not csv_exists() else csv_read(0, 2)

print(csv_exists(), t_start)

if not csv_exists():
    create_csv()


class Counter(Widget):
    def __init__(self, **kwargs):
        super(Counter, self).__init__(**kwargs)
        self.count = 0 if not csv_exists() else int(csv_read(-1, 0))
        self.timestamp_abs = math.floor((time.time()-t_start)*1000)
        self.key_down = False
        self.initUI()

    def initUI(self):
        # create label to display count
        self.count_label = Label(text=str(self.count), font_size=24, halign="center")

        # create buttons to add and subtract
        self.add_button = Button(text="+")
        self.sub_button = Button(text="-")

        # set stylesheet for widgets
        self.count_label.background_color = (0, 0, 0, 1)
        self.count_label.color = (1, 1, 1, 1)

        self.add_button.background_color = (0.23, 0.23, 0.23, 1)
        self.add_button.color = (1, 1, 1, 1)
        self.add_button.font_size = 18
        self.add_button.border_radius = 15
        self.add_button.padding = (10, 20)

        self.sub_button.background_color = (0.23, 0.23, 0.23, 1)
        self.sub_button.color = (1, 1, 1, 1)
        self.sub_button.font_size = 18
        self.sub_button.border_radius = 15
        self.sub_button.padding = (10, 20)

        # create horizontal layout for buttons
        hbox = BoxLayout()
        hbox.add_widget(self.sub_button)
        hbox.add_widget(self.add_button)

        # create vertical layout and add widgets
        vbox = BoxLayout(orientation="vertical")
        vbox.add_widget(self.count_label)
        vbox.add_widget(hbox)

        # set layout
        self.add_widget(vbox)

        # connect buttons to functions
        self.add_button.bind(on_press=self.add)
        self.sub_button.bind(on_press=self.subtract)

        # bind resize event
        Window.bind(on_resize=self.onResize)
        

        
    def onResize(self, instance, size):
        self.Window_size = size
        self.Window_x = self.Window_size[0]
        self.Window_y = self.Window_size[1]
        self.font_size = int(self.Window_y / 3)
        self.button_size = int(self.Window_y / 10)

        # change font size when window is resized
        self.count_label.font_size = self.font_size

        self.add_button.font_size = self.button_size
        self.add_button.padding = [10, 20]
        self.sub_button.font_size = self.button_size
        self.sub_button.padding = [10, 20]
    
    def add(self, instance):
        self.count += 1
        self.count_label.text = str(self.count)
        self.timestamp_abs = math.floor((time.time()-t_start)*1000)
     
    def subtract(self, instance):
        self.count -= 1
        self.count_label.text = str(self.count)
        self.timestamp_abs = math.floor((time.time()-t_start)*1000)
    
    
    
class CounterApp(App):
    def build(self):
        # create the counter widget
        return Counter()

if __name__ == "__main__":
    CounterApp().run()

    print("Bye!")