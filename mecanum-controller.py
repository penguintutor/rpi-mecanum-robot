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
    '1' : "turn_left",
    '2' : "backward",
    '3' : "turn_right",
    '4' : "left",
    '5' : "stop",
    '6' : "right",
    '7' : "diagonal_left",
    '8' : "forward",
    '9' : "diagonal_right",
    'q' : "diagonal_left",
    'e' : "diagonal_right",
    'z' : "diagonal_left_rev",
    'c' : "diagonal_right_rev"

}

current_direction = "stop"
# speed is as a percentage (ie. 100 = top speed)
# start speed is 50% which is fairly slow on a flat surface
speed = 50
pwm_out.value = speed/100

print ("Robot control - use number keys to control direction")
print ("Speed " + str(speed) +"% - use +/- to change speed")

while True:
    # Convert speed from percentage to float (0 to 1)
    if (current_direction == "forward") :
        motors[0].forward()
        motors[1].forward()
        motors[2].forward()
        motors[3].forward()
    # rev
    elif (current_direction == "backward") :
        motors[0].backward()
        motors[1].backward()
        motors[2].backward()
        motors[3].backward()
    elif (current_direction == "left") :
        motors[0].backward()
        motors[1].forward()
        motors[2].forward()
        motors[3].backward()
    elif (current_direction == "right") :
        motors[0].forward()
        motors[1].backward()
        motors[2].backward()
        motors[3].forward()
    elif (current_direction == "turn_left") :
        motors[0].backward()
        motors[1].forward()
        motors[2].backward()
        motors[3].forward()
    elif (current_direction == "turn_right") :
        motors[0].forward()
        motors[1].backward()
        motors[2].forward()
        motors[3].backward()
    elif (current_direction == "diagonal_left") :
        motors[0].stop()
        motors[1].forward()
        motors[2].forward()
        motors[3].stop()
    elif (current_direction == "diagonal_right") :
        motors[0].forward()
        motors[1].stop()
        motors[2].stop()
        motors[3].forward()
    elif (current_direction == "diagonal_right_rev") :
        motors[0].stop()
        motors[1].backward()
        motors[2].backward()
        motors[3].stop()
    elif (current_direction == "diagonal_left_rev") :
        motors[0].backward()
        motors[1].stop()
        motors[2].stop()
        motors[3].backward()
    # stop
    else :
        motors[0].stop()
        motors[1].stop()
        motors[2].stop()
        motors[3].stop()

    # Get next key pressed
    ch = getch()

    # p = quit
    if (ch == 'p') :
        break
    elif (ch == '+' or ch == '=') :
        speed += 10
        if speed > 100 :
            speed = 100
        pwm_out.value = speed/100
        print ("Speed : "+str(speed))
    elif (ch == '-' ) :
        speed -= 10
        if speed < 0 :
            speed = 0
        pwm_out.value = speed/100
        print ("Speed : "+str(speed))
    elif (ch in direction.keys()) :
        current_direction = direction[ch]
        print ("Direction "+current_direction)
