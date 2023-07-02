#!/usr/bin/python3
import sys, tty, termios
from gpiozero import PWMOutputDevice, Motor

pwm_pin = 18
m_f_l = (2,3)
m_f_r = (22,23)
m_r_l = (14,15)
m_r_r = (24,25)

motors = [ 
    Motor(m_f_l[0], m_f_l[1], pwm=False),
    Motor(m_f_r[0], m_f_r[1], pwm=False),
    Motor(m_r_l[0], m_r_l[1], pwm=False),
    Motor(m_r_r[0], m_r_r[1], pwm=False)
    ]


pwm_out = PWMOutputDevice (pwm_pin)


# get a character from the command line
def getch() :
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


# list to convert key into motor on/off values to correspond with direction
# direction based on number keypad
# 8 = fwd, 4 = left, 5 = stop, 6 = right, 2 = rev
# the key for the list is the character 
direction = {
    # number keys
    '1' : (-1, 1, -1, 1),   # Turn left
    '2' : (-1, -1, -1, -1), # Backwards
    '3' : (1, -1, 1, -1),   # Turn right
    '4' : (-1, 1, 1, -1),   # Left
    '5' : (0, 0, 0, 0),     # Stop
    '6' : (1, -1, -1, 1),   # Right
    '7' : (0, 1, 1, 0),     # Diagonal left
    '8' : (1, 1, 1, 1),     # Forwards
    '9' : (1, 0, 0, 1),     # Diagonal right
    # Additional mapping for WASD and diagonal
    'q' : (0, 1, 1, 0),     # Diagonal left
    'w' : (1, 1, 1, 1),     # Forwards
    'e' : (1, 0, 0, 1),     # Diagonal right
    'a' : (-1, 1, -1, 1),   # Turn left
    'd' : (1, -1, 1, -1),   # Turn right
    'z' : (-1, 0, 0, -1),   # Diagonal left backwards
    'x' : (0, 0, 0, 0),     # Stop
    'c' : (0, -1, -1, 0)    # Diagonal right backwards
}

current_direction = "stop"
# speed is as a percentage (ie. 100 = top speed)
# start speed is 50% which is fairly slow on a flat surface
speed = 50
pwm_out.value = speed/100

print ("Robot control - use number keys to control direction")
print ("Speed " + str(speed) +"% - use +/- to change speed") 

while True:
    # Get next key pressed      
    ch = getch()

    if (ch == 'q') :        # Quit
        break
    elif (ch == '+') :      # Change speed
        speed += 10
        if speed > 100 :
            speed = 100
        pwm_out.value = speed/100
        print ("Speed : "+str(speed))
    elif (ch == '-' ) :     # Change direction
        speed -= 10
        if speed < 0 :
            speed = 0
        pwm_out.value = speed/100
        print ("Speed : "+str(speed))
    elif (ch in direction.keys()) :
        for i in range (0, 4):
            if direction[ch][i] == -1:
                motors[i].backward()
            elif direction[ch][i] == 1:
                motors[i].forward()
            else:
                motors[i].stop()
        print ("Direction "+ch)

