from __future__ import division
import time
from adxl345 import ADXL345
from _ast import Or
adxl345 = ADXL345()
import Adafruit_PCA9685
from sys import argv
from ast import literal_eval as make_tuple
import pyaudio
import wave
from threading import Thread
from multiprocessing import Process
global starttime2
starttime2 = time.time()

def read_audio():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 22050
    CHUNK = 1024
    RECORD_SECONDS = 30
    WAVE_OUTPUT_FILENAME = "train2.wav"
    audio = pyaudio.PyAudio()
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        input_device_index = 1,
                        frames_per_buffer=CHUNK)
    print "recording..."
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print "finished recording"

    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate() 
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

def check_position():
    global starttime2
    nowtime=round(time.time()-starttime2,2)
    axes = adxl345.getAxes(True)
    position = [axes['x'],axes['y'],axes['z'],nowtime]
    return position

def run():
    old_servo_x = 0
    program_disc = open("train2.txt",'w')
    program_disc.truncate
    while True:
        servo = check_position()
        #servo_x = int(servo[0]*250)+350
        #servo_y = int(servo[1]*250)+350
        #servo_z = int(servo[2]*250)+350
        #print('accelerometer reading')
        #if old_servo_x+5 < servo_x or old_servo_x-5 > servo_x:
        #print("bigger")
        program_disc.write(str(servo) + ";")
        #old_servo_x = servo_x
        time.sleep(0.1)

def destroy():
    global BackGroundMusicArray
    BackGroundMusicArray = []
    GPIO.cleanup()                     # Release resource

if __name__ == "__main__":
    try:
        ThreadA = Process(target= run)
        ThreadB = Process(target= read_audio)
        #run()
        #read_audio()
        ThreadB.start()
        ThreadA.start()
        #ThreadA.join()
        #ThreadB.join()
    except KeyboardInterrupt:
        destroy()