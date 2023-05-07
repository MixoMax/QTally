def req():
    import os
    try:
        import PySide6, keyboard, pyperclip
        return True
    except:
        os.system("pip install PySide6 keyboard pyperclip") if os.name == "nt" else os.system("pip3 install PySide6 keyboard pyperclip")
        return False
req()
import os
import csv
import time
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout, QFileDialog, QFileIconProvider
import random
import string
import keyboard
import math
import pyperclip

global csv_path

user_name = os.getlogin()

os.chdir(f"C:/Users/{user_name}/Documents")

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
        writer.writerow([0, 0, time.time(), 0])
        return 0

t_start = time.time() if not csv_exists() else csv_read(0, 2)

print(csv_exists(), t_start)

if not csv_exists():
    create_csv()



class Counter(QWidget):
    def __init__(self):
        super().__init__()
        self.count = 0 if not csv_exists() else int(csv_read(-1, 1))
        self.timestamp_rel = self.update_timestamp_rel()
        self.initUI()
        self.keyPressEvent = self.handle_key_press
        self.resizeEvent = self.onResize
        self.Window_size = self.size()
        self.Window_x = self.Window_size.width()
        self.Window_y = self.Window_size.height()
        self.font_size = self.Window_y / 10
        self.button_size = int(self.Window_y / 10)
        self.plus_count = 0
        self.last_key = ""

    def initUI(self):
        #set screen size
        self.setMinimumSize(100, 100)
        self.setMaximumSize(400, 400)
        self.setWindowTitle("Counter")

        # create label to display count
        self.count_label = QLabel(str(self.count), self)
        self.count_label.setAlignment(Qt.AlignCenter)

        # create buttons to add and subtract
        self.add_button = QPushButton("+", self)
        self.sub_button = QPushButton("-", self)

        # set stylesheet for widgets
        self.setStyleSheet('''
            background-color: #1e1e1e;
            color: #f0f0f0;
            border: none;
        ''')

        self.count_label.setStyleSheet('''
            font-size: 24px;
        ''')

        self.add_button.setStyleSheet('''
            background-color: #3a3a3a;
            color: #f0f0f0;
            font-size: 18px;
            border-radius: 15px;
            padding: 10px 20px;
        ''')

        self.sub_button.setStyleSheet('''
            background-color: #3a3a3a;
            color: #f0f0f0;
            font-size: 18px;
            border-radius: 15px;
            padding: 10px 20px;
        ''')

        # create horizontal layout for buttons
        hbox = QHBoxLayout()
        hbox.addWidget(self.sub_button, 1)
        hbox.addWidget(self.add_button, 1)

        # create vertical layout and add widgets
        vbox = QVBoxLayout()
        vbox.addWidget(self.count_label, 1)
        vbox.addLayout(hbox)

        # set layout
        self.setLayout(vbox)

        # connect buttons to functions
        self.add_button.clicked.connect(self.add)
        self.sub_button.clicked.connect(self.subtract)


    def onResize(self, event):
        self.Window_size = self.size()
        self.Window_x = self.Window_size.width()
        self.Window_y = self.Window_size.height()
        self.font_size = int(self.Window_y / 3)
        self.button_size = int(self.Window_y / 10)

        # change font size when window is resized
        self.count_label.style().unpolish(self.count_label)
        self.count_label.setStyleSheet(f"font-size: {self.font_size}px;")
        self.count_label.style().polish(self.count_label)
        self.count_label.update()

        self.add_button.style().unpolish(self.add_button)
        self.add_button.setStyleSheet(f'''
            background-color: #3a3a3a;
            color: #f0f0f0;
            font-size: {self.button_size}px;
            border-radius: 15px;
            padding: 10px 20px;
        ''')
        self.add_button.style().polish(self.add_button)
        self.add_button.update()
        
        self.sub_button.style().unpolish(self.sub_button)
        self.sub_button.setStyleSheet(f'''
            background-color: #3a3a3a;
            color: #f0f0f0;
            font-size: {self.button_size}px;
            border-radius: 15px;
            padding: 10px 20px;
        ''')
        self.sub_button.style().polish(self.sub_button)
        self.sub_button.update()


    def add(self):
        self.count += 1
        self.count_label.setText(str(self.count))
        self.plus_count += 1
        self.timestamp_rel = self.update_timestamp_rel()
        self.record_count()
        time.sleep(1/30)

    def subtract(self):
        self.count -= 1
        self.count_label.setText(str(self.count))
        self.timestamp_rel = self.update_timestamp_rel()
        self.record_count()
        time.sleep(1/30)

    def record_count(self):
        # write count and timestamp to CSV file
        with open(csv_path, "a", newline="") as f:
            writer = csv.writer(f)
            self.timestamp_rel = self.update_timestamp_rel()
            writer.writerow([self.timestamp_rel, self.count, time.time(), self.plus_count])
    
    def update_timestamp_rel(self):
        return (time.time()-t_start) / 60
    
    def close_2(self):
        random_key = random.choice(string.ascii_letters).lower()
        print(f"Press {random_key} to close")
        t1 = time.time()
        while time.time()-t1 < 3:
            if keyboard.is_pressed(random_key):
                self.close()
                break
    
    
    def reset_csv(self):
        random_key = random.choice(string.ascii_letters).lower()
        print(f"Press {random_key} to reset")
        t1 = time.time()
        while time.time()-t1 < 3:
            if keyboard.is_pressed(random_key):
                os.remove(csv_path)
                print("Reset")
                self.load_csv()
                break
        else:
            print("Reset cancelled")
        
    
    def load_csv(self):
        global csv_path
        # load CSV file
        
        #open explorer to select file
        csv_path = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")[0]
        
        if csv_exists():
            print(f"CSV loaded: {csv_path}")
            self.count = int(csv_read(-1, 0))
            self.count_label.setText(str(self.count))
            self.count_label.update()
            t_start = csv_read(0,2)
            self.timestamp_rel = self.update_timestamp_rel()
        else:
            self.close()

    def create_new_csv(self):
        global csv_path
        # create CSV file
        
        #open explorer to select file
        csv_path = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")[0]
        
        with open(csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([str(int(self.count)), 0, time.time()])
            print(f"CSV created: {csv_path}")
        
    
    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.count_label.text())
        print("Copied to clipboard")
    
    
    def handle_key_press(self, event):
        key = event.key()

        if key < 256:
            key = chr(key)
        
        self.last_key = key

        match key:
            case "+": self.add()
            case "-": self.subtract()
            case "Q": self.close_2()
            case "R": self.reset_csv()
            case "X": self.reset_csv()
            case "L": self.load_csv()
            case "S": self.create_new_csv()
            case "C": self.copy_to_clipboard()
        
#

if __name__ == '__main__':
    app = QApplication([])
    counter = Counter()
    counter.show()
    app.exec()
