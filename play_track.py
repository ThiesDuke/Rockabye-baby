import time
import Adafruit_PCA9685
from ast import literal_eval as make_tuple
import pygame
from time import strftime
import os
import math

pwm = Adafruit_PCA9685.PCA9685()

servo = 1000  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096
old_servo = 100
pwm.set_pwm_freq(60)
pygame.mixer.pre_init(16000, -16, 1, 1024)
pygame.mixer.init()
pygame.init()


def run():
    pygame.mixer.music.load('train2.wav')
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play()
    print('Moving servo on channel 0, press Ctrl-C to quit...')
    old_servo_x = 0
    program_disc = open("train2.txt",'r')
    track_string = program_disc.read()
    track= track_string.split(";")
    #program_disc.truncate
    starttime= time.time()
    Sum_x = 0
    Sum_y = 0
    Sum_z = 0
    for num1 in range(0,len(track)-1):
        Sum_x= Sum_x + int(make_tuple(track[num1])[0]*250)+350 
        Sum_y= Sum_y + int(make_tuple(track[num1])[1]*250)+350
        Sum_z= Sum_z + int(make_tuple(track[num1])[2]*250)+350
    
    Delta_x=350-Sum_x/(len(track)-1)
    Delta_y=350-Sum_y/(len(track)-1)
    Delta_z=600-Sum_z/(len(track)-1)
    print(Delta_x)
    print(Delta_y)
    print(Delta_z)
    #program_disc = open("control.txt",'w')
    #program_disc.truncate
    
    for num in range(0,len(track)-1):
        # Move servo on channel O between extremes.
        servo_x = int(make_tuple(track[num])[0]*250)+350+Delta_x
        servo_y = int(make_tuple(track[num])[1]*250)+350+Delta_y
        servo_z = int(make_tuple(track[num])[2]*250)+350+Delta_z
        print("#########################")
        print("servo_x: "+ str(servo_x))
        print("servo_y: "+ str(servo_y))
        print("servo_z: "+ str(servo_z))
        #print(make_tuple(track[num])[3])
        if num%10==0:
            pygame.mixer.music.get_pos()
            num= int(round(make_tuple(track[num])[3],0))
            #print("synced")
        time.sleep(0.1)
        offsetservo_x = 700-servo_x
        offsetservo_y = 700-servo_y
        servo_1= math.sqrt(math.pow(math.sqrt(math.pow(servo_x,2)+math.pow(offsetservo_y,2)),2)+math.pow(servo_z,2))
        servo_2= math.sqrt(math.pow(math.sqrt(math.pow(offsetservo_x,2)+math.pow(offsetservo_y,2)),2)+math.pow(servo_z,2))
        servo_3= math.sqrt(math.pow(math.sqrt(math.pow(servo_x,2)+math.pow(servo_y,2)),2)+math.pow(servo_z,2))
        servo_4= math.sqrt(math.pow(math.sqrt(math.pow(offsetservo_x,2)+math.pow(servo_y,2)),2)+math.pow(servo_z,2))
        #Original- Servos not integrated into Box and not adjusted for installation position
        #servo_1_pwm=((828-servo_1)/1)*5+100
        #servo_2_pwm=((828-servo_2)/1)*5+100
        #servo_3_pwm=((828-servo_3)/1)*5+100
        #servo_4_pwm=((828-servo_4)/1)*5+100
        #Installation of servos with: 
        #1: facing inwards, head towards top, laying on right side; 
        #2: head towards top, laying on left side; 
        #3: head towards bottom, laying on right side; 
        #4: head towards bottom, laying on left side
        servo_1_pwm=((828-servo_1)/1)*5+100
        servo_2_pwm=((servo_2-728)/1)*5+100
        servo_3_pwm=((servo_3-728)/1)*5+100
        servo_4_pwm=((828-servo_4)/1)*5+100
        print(servo_1_pwm)
        print(servo_2_pwm)
        print(servo_3_pwm)
        print(servo_4_pwm)
        #program_disc.write(str(servo_1_pwm) + ",")
        #if old_servo_x+5 < servo_x or old_servo_x-5 > servo_x:
        #pwm.set_pwm(1, 0, int(clamp(servo_1_pwm)))
        #pwm.set_pwm(2, 0, int(clamp(servo_2_pwm)))
        #pwm.set_pwm(3, 0, int(clamp(servo_3_pwm)))
        #pwm.set_pwm(4, 0, int(clamp(servo_4_pwm)))
            #print("bigger")
            #program_disc.write(str(servo) + ";")
            #old_servo_x = servo_x

def destroy():
    global BackGroundMusicArray
    BackGroundMusicArray = []
    GPIO.cleanup()                     # Release resource

def clamp(x):
    return max(100, min(x, 600))

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        destroy()