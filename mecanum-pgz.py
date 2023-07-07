from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Device, PWMOutputDevice, Motor, DistanceSensor

WIDTH=800
HEIGHT=600

Device.pin_factory = PiGPIOFactory()

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

dist_sensor = DistanceSensor(echo=6, trigger=5)

arrows = [
    Actor("arrow.png", center=(500,300)),
    Actor("arrow.png", center=(400,200)),
    Actor("arrow.png", center=(300,300)),
    Actor("arrow.png", center=(400,400))
    ]
    
arrows[1].angle = 90
arrows[2].angle = 180
arrows[3].angle = 270

# distance is a value between 0 and 1
# higher is further away
min_distance = 0.09

# list to convert key into motor on/off values to correspond with direction
# direction based on number keypad
# 8 = fwd, 4 = left, 5 = stop, 6 = right, 2 = rev
# the key for the list is the key
# For number keys two values, one for main keyboard, the other for 
# numeric keypad
direction = {
    # number keys
    keys.K_1 : (-1, 1, -1, 1),   # Turn left
    keys.KP1 : (-1, 1, -1, 1),   # Turn left
    keys.K_2 : (-1, -1, -1, -1), # Backwards
    keys.KP2 : (-1, -1, -1, -1), # Backwards
    keys.K_3 : (1, -1, 1, -1),   # Turn right
    keys.KP3 : (1, -1, 1, -1),   # Turn right
    keys.K_4 : (-1, 1, 1, -1),   # Left
    keys.KP4 : (-1, 1, 1, -1),   # Left
    keys.K_5 : (0, 0, 0, 0),     # Stop
    keys.KP5 : (0, 0, 0, 0),     # Stop
    keys.K_6 : (1, -1, -1, 1),   # Right
    keys.KP6 : (1, -1, -1, 1),   # Right
    keys.K_7 : (0, 1, 1, 0),     # Diagonal left
    keys.KP7 : (0, 1, 1, 0),     # Diagonal left
    keys.K_8 : (1, 1, 1, 1),     # Forwards
    keys.KP8 : (1, 1, 1, 1),     # Forwards
    keys.K_9 : (1, 0, 0, 1),     # Diagonal right
    keys.KP9 : (1, 0, 0, 1),     # Diagonal right
    # Additional mapping for WASD and diagonal
    keys.Q : (0, 1, 1, 0),     # Diagonal left
    keys.W : (1, 1, 1, 1),     # Forwards
    keys.E : (1, 0, 0, 1),     # Diagonal right
    keys.A : (-1, 1, -1, 1),   # Turn left
    keys.D : (1, -1, 1, -1),   # Turn right
    keys.Z : (-1, 0, 0, -1),   # Diagonal left backwards
    keys.X : (0, 0, 0, 0),     # Stop
    keys.C : (0, -1, -1, 0)    # Diagonal right backwards
}

# Track direction
current_direction = (0, 0, 0, 0)

# speed is as a percentage (ie. 100 = top speed)
# start speed is 50% which is fairly slow on a flat surface
speed = 50
pwm_out.value = speed/100


def draw():
    screen.fill((192,192,192))
    for arrow in arrows:
        arrow.draw()

def update():
    global current_direction
    # Check distance from front
    #print ("Distance : "+str(dist_sensor.distance))
    # if about to crash
    try:
        if (dist_sensor.distance <= min_distance):
            # Is robot going forward (or diagonal)
            if ((current_direction[0] == 1 and current_direction[1] != -1) or
                (current_direction[1] == 1 and current_direction[0] != -1)):
                print ("Warning - crash imminent")
                current_direction = (0, 0, 0, 0)
                motors_stop()
    except:
        print ("No distance sensor detected")


def on_key_down(key):
    global speed, current_direction
    # Get next key pressed      
    if (key == key.PLUS or key == key.EQUALS or key == key.KP_PLUS) :  # speed
        speed += 10
        if speed > 100 :
            speed = 100
        pwm_out.value = speed/100
        print ("Speed : "+str(speed))
    elif (key == key.MINUS or key == key.KP_MINUS) :     # change direction
        speed -= 10
        if speed < 0 :
            speed = 0
        pwm_out.value = speed/100
        print ("Speed : "+str(speed))
    elif (key in direction.keys()) :
        current_direction = direction[key]
        for i in range (0, 4):
            if direction[key][i] == -1:
                motors[i].backward()
            elif direction[key][i] == 1:
                motors[i].forward()
            else:
                motors[i].stop()

def motors_stop():
    for i in range (0, 4):
        motors[i].stop()
