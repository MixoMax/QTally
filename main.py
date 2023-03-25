import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.setupconfig import USE_SDL2
from kivy.core.audio import SoundLoader
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import ObjectProperty

import os
import csv
import time
import math

global csv_path

#https://www.youtube.com/watch?v=6gNpSuE01qE

kivy.require("1.9.0")

platform = kivy.utils.platform

file_path = os.path.dirname(os.path.realpath(__file__))

os.chdir(file_path)

csv_path = "./count.csv"

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

if not csv_exists():
    create_csv()



class MyRoot(BoxLayout):
    counter_label = ObjectProperty()

    def __init__(self, **kwargs):
        super(MyRoot, self).__init__(**kwargs)
        self.update_label()
    
    def update_label(self):
        self.counter_label.text = str(counter.count)
    
    def increment(self):
        counter.add()
        self.update_label()
    
    def decrement(self):
        counter.subtract()
        self.update_label()
    
    def delete(self):
        counter.delete()
        self.update_label()
    
    def share(self):
        counter.share()



class counterapp(MDApp):
    def __init__(self, **kwargs):
        super(counterapp, self).__init__(**kwargs)
        self.count = 0 if not csv_exists() else int(csv_read(-1,0))
        self.timestamp_abs = math.floor((time.time()-t_start)*1000)
        self.delete_presses = []
        if platform == "win":
            self.up_sound = SoundLoader.load("./data/audio/up.mp3")
            self.down_sound = SoundLoader.load("./data/audio/down.mp3")
    
    def add(self):
        self.count += 1
        self.timestamp_abs = math.floor((time.time()-t_start)*1000)
        self.record_count()
        if platform == "win":
            self.up_sound.play()
        time.sleep(1/100)


    def subtract(self):
        self.count -= 1
        self.timestamp_abs = math.floor((time.time()-t_start)*1000)
        self.record_count()
        if platform == "win":
            self.up_sound.play()
        time.sleep(1/100)


    def delete(self):
        self.delete_presses.append(time.time())
        
        valid_presses = [press for press in self.delete_presses if press > time.time()-2]
        
        if len(valid_presses) > 5:
            os.remove(csv_path)
            print("deleted")
            self.load_csv()
        else:
            print("press", 6 - len(valid_presses), "more times to delete")


    def load_csv(self):
        global csv_path
        
        with open(csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([str("0"), 0, time.time()])
        
        print(f"CSV loaded: {csv_path}")
        self.count = int(csv_read(-1, 0))
        t_start = csv_read(0,2)
        self.timestamp_abs = math.floor((time.time()-t_start)*1000)


    def share(self):
        """share current csv file via android intent"""
        
        return 0


    def record_count(self):
        """write count and timestamp to CSV file"""
        with open(csv_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([self.count, self.timestamp_abs, time.time()])


    def build(self):
        return MyRoot()



if __name__ == "__main__":
    counter = counterapp()
    counter.run()