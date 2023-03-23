import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.setupconfig import USE_SDL2

import os
import csv
import time
import math

global csv_path

#https://www.youtube.com/watch?v=6gNpSuE01qE

kivy.require("1.9.0")

os.chdir(os.path.dirname(os.path.abspath(__file__)))

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
    def __init__(self, **kwargs):
        super(MyRoot, self).__init__(**kwargs)
    
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



class counterapp(App):
    def __init__(self, **kwargs):
        super(counterapp, self).__init__(**kwargs)
        self.count = 0 if not csv_exists() else int(csv_read(0, 0))
        self.timestamp_abs = math.floor((time.time()-t_start)*1000)
        self.delete_presses = []
    
    def add(self):
        self.count += 1
        self.timestamp_abs = math.floor((time.time()-t_start)*1000)
        self.record_count()
        time.sleep(1/100)


    def subtract(self):
        self.count -= 1
        self.timestamp_abs = math.floor((time.time()-t_start)*1000)
        self.record_count()
        time.sleep(1/100)


    def delete(self):
        self.delete_presses.append(time.time())
        
        print(self.delete_presses)
        
        valid_presses = [press for press in self.delete_presses if press > time.time()-2]
        
        if len(valid_presses) > 5:
            os.remove(csv_path)
            print("deleted")
            self.load_csv()


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
        
        platform = kivy.utils.platform
        print(platform)
        
        if platform == "android":
            from android.storage import primary_external_storage_path
            from jnius import autoclass
            from jnius import cast
            
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            
            Intent = autoclass("android.content.Intent")
            String = autoclass("java.lang.String")
            Uri = autoclass("android.net.Uri")
            File = autoclass("java.io.File")
            
            ShareIntent = Intent(Intent.ACTION_SEND)
            ShareIntent.setType("text/plain")
            
            path = os.path.join(primary_external_storage_path(), "./count.csv")
        
            csv_file = File(path)
            Uri = Uri.fromFile(csv_file)
            parcelable = cast("android.os.Parcelable", Uri)
            ShareIntent.putExtra(Intent.EXTRA_STREAM, parcelable)
            
            CurrentActivity = cast("android.app.Activity", PythonActivity.mActivity)
            CurrentActivity.startActivity(ShareIntent)


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