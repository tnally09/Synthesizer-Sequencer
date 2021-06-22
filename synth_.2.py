import sys
import numpy as np
import pygame
import pygame.mixer
from pygame.mixer import get_init, stop
from array import array
from functools import partial
from PyQt6.QtWidgets import QApplication, QSlider, QWidget, QPushButton, QGridLayout, QRadioButton, QButtonGroup
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import time
from scipy import signal

# global variables
samp_rate = 44100
pygame.mixer.init(samp_rate, -16, 2, 512)
sequence = []
Loop = False
wave_type = 0
duration = 22050

# method for playing a sine wave
def play_sine(freq):
    arr = np.array([4096 * np.sin(2.0 * np.pi * freq * (x / samp_rate)) for x in range(0, duration)]).astype(np.int16)
    arr2 = np.c_[arr,arr]
    note = pygame.sndarray.make_sound(arr2)
    note.play(1)
    

# method for playing a square wave
def play_square(freq):
    period = int(round(get_init()[0] / freq))
    samples = array("h", [0] * period)
    amplitude = 2 ** (abs(get_init()[1]) - 1) - 1
    #arr = np.array([signal.square(2 * np.pi * freq (x / samp_rate)) for x in range(0, samp_rate)]).astype(np.int16)
    for time in range(period):
        if time < period / 2:
            samples[time] = amplitude
            arr = samples
            arr2 = np.c_[arr,arr]
        else:
            samples[time] = -amplitude
            arr = samples
            arr2 = np.c_[arr,arr]
    arr2 = np.c_[arr,arr]
    note = pygame.sndarray.make_sound(arr2)
    note.play(1)


class Worker(QThread):
    def run(self):
            pygame.mixer.stop
            while Loop == True:
                for i in sequence:
                    if wave_type == 1:
                        play_sine(i)
                        pygame.mixer.stop
                        time.sleep((.25))
                    if wave_type == 2:
                        play_square(i)
                        pygame.mixer.stop                
                        time.sleep((.25))




class key(QPushButton):
    def __init__(self, key_num, freq):
        super().__init__()
        self.key_num = key_num
        self.freq = freq

class synth(QWidget):    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Synthesizer')
        self.resize(800, 150) # width, height
        layout = QGridLayout()
        self.setLayout(layout)
        layout.setSpacing(5)

        # wave type selection definitions
        wave_select = QButtonGroup(self)
        self.sine_button = QRadioButton('Sine', self)
        self.sine_button.move(40,0)
        self.square_button = QRadioButton('Square', self)
        self.square_button.move(120,0)
        wave_select.addButton(self.sine_button)
        wave_select.addButton(self.square_button)
        self.sine_button.clicked.connect(self.onToggle_sine)
        self.square_button.clicked.connect(self.onToggle_square)

        
        

        # tempo/play speed slider
        tempo_slider = QSlider(Qt.Orientation.Horizontal)
        tempo_slider.setValue(120)
        tempo_slider.setMinimum(60)
        tempo_slider.setMaximum(180)
        tempo_slider.move(10,1)
        #.tickInterval(5)
        #tempo_slider.valueChanged[int].connect(tempo_slider.changeValue)
        layout.addWidget(tempo_slider)
        tempo = (tempo_slider.value())/60

        # stop button
        stop = QPushButton('Stop')
        stop.setStyleSheet("background-color: red;")
        layout.addWidget(stop, 1, 25, 1, 6)
        stop.clicked.connect(partial(self.onClick_stop))

        # sequencer button
        sequence_button = QPushButton('Play Sequence')
        sequence_button.setStyleSheet("background-color: green;")
        layout.addWidget(sequence_button, 1, 50, 1, 6)
        sequence_button.clicked.connect(partial(self.onClick_sequence))

       

        # keyboard note range
        lo = 9
        hi = 80

        # keyboard definition
        # i represents musical keyboard key number
        for i in range(lo, hi):
            # key number is used to determine frequency of note
            f = (2 ** ((i - 49) / 12) * 440)
            self.keys = {
                    i: key(i, f)
                }
            
            button = QPushButton()
            
            # differentiate black and white keys
            black_keys = {2, 5, 7, 10, 12, 14, 17, 19, 22, 24, 26, 29, 31, 34, 36, 38, 41, 43, 46, 48, 50, 53, 55, 58, 60, 62, 65, 67, 70, 72, 74, 77, 79, 82, 84, 86}
            if i in black_keys:
                button.setStyleSheet("background-color: black;")
                button.setFixedSize(20,75)
                layout.addWidget(button, 4, i)
            else:
                button.setStyleSheet("background-color: white;")
                button.setFixedSize(20,150)
                layout.addWidget(button, 4, i, 2, 1)

            # behavior for individual piano key presses
            button.clicked.connect(partial(self.onClick_keys, self.keys[i].freq))

    # click behavior for individual piano key presses
    def onClick_keys(self, freq):
        if pygame.mixer.get_busy() == True:
            pygame.mixer.stop()
        if self.sine_button.isChecked() == True:
            play_sine(freq)
        if self.square_button.isChecked() == True:
            play_square(freq)
        # adds pressed key to sequence
        sequence.append(freq)

    # click behavior for stop button
    def onClick_stop(self):
        global Loop
        Loop = False
        pygame.mixer.stop()
        global sequence
        sequence = []
        return sequence
        

    # click behavior for sequence button
    def onClick_sequence(self):
        if pygame.mixer.get_busy() == True:
            pygame.mixer.stop()
        self.worker = Worker()
        global Loop
        Loop = True
        self.worker.start()

    def onToggle_sine(self):
        global wave_type
        wave_type = 1
        return wave_type
    
    def onToggle_square(self):
        global wave_type
        wave_type = 2
        return wave_type
            

# application event loop
app = QApplication(sys.argv)
window = synth()
window.show()
app.exec()
sys.exit(app.exec())