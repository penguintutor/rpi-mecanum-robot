# rpi-mecanum-robot
Raspberry Pi powered mecanum robot

## Requirements
Software to control a 4-wheel mecanum robot. Based on a Raspberry Pi (such as Raspberry Pi Pico W) with two pairs of TB6612FNG motor drivers. Uses keypad controls, also compatible with AntiMicroX or QJoyPad for gamepad control.

## Install and run
Download the file mecanum.py. It is recommended that this is installed in /opt/mecanum
Create directory and copy the files using
    sudo mkdir /opt/mecanum
    sudo chown $USER:
    cp mecanum.py /opt/mecanum/
    cp robot.sh /opt/mecanum/
    
Run using
    /opt/robot/mecanum.py

Use the keypad to set the direction.

## Using AntiMicroX / QJoyPad

Configuration files are included for AnitMicroX and QJoyPad allowing the robot to be controlled with a gamepad controller. 

QJoyPad has not been updated for a long time, so AntiMicroX is recommended.
Install using 
    sudo apt install antimicro
    
The following files are included:
* mecanum.gamecontroller.amgp - AntiMicroX
* mecanum-gamepad.lyt - QJoyPad

There appears to be a conflict, possibly with VNC. If the gamepad is not detected correctly then trying removing and reinserting the USB dongle once or twice and then choosing "Update Joysticks" from the menu.

## Starting automatically
The programs can be started by adding the following entry to /etc/xdg/lxsession/LXDE-pi/autostart (edit using sudo)
    lxterminal -e /opt/mecanum/robot.sh


## Pygame Zero version
There is also a version designed for Pygame Zero. This includes a distance sensor and stops forward motion if a crash is imminent. This is currently under development. To run use
    pgzrun mecanum-pgz.py


## More information 

For more information see [Raspberry Pi Mecanum Robot on Penguintutor](http://www.penguintutor.com/projects/robot)
