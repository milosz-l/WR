#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_D, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import ColorSensor
from time import sleep


# define output names
# OUTPUT_A = 'outA'
# OUTPUT_D = 'oudD'

# define wheel motors
# motor_r = LargeMotor(OUTPUT_A)
# motor_l = LargeMotor(OUTPUT_D)

# define color sensors
color_sensor_r = ColorSensor(address=INPUT_1)
color_sensor_l = ColorSensor(address=INPUT_4)

# define go_forward function


def go_forward(speed=100, rotations=10):
    '''
    runs both motors at the same time, what makes the car go forward
    speed is a percentage between 0 and 100
    time is in seconds
    '''
    # TODO: change below (driving with two motors)
    # motor_r.on_for_rotations(ev3.SpeedPercent(speed), 5)
    # motor_l.on_for_rotations(ev3.SpeedPercent(speed), 5)
    tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)
    tank_drive.on_for_rotations(SpeedPercent(speed), SpeedPercent(speed), rotations)


def turn(speed=100, rotations=10, direction='right'):
    '''
    turns
    '''
    if direction == 'right':
        speed_r = speed/3
        speed_l = speed
    else:
        speed_r = speed
        speed_l = speed/3
    tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)
    tank_drive.on_for_rotations(SpeedPercent(speed), SpeedPercent(speed), rotations)


def get_colors():
    '''
    returns tuple of two strings: (right_color, left_color)
    '''
    color_r = color_sensor_r.color
    text_r = ColorSensor.COLORS[color_r]
    color_l = color_sensor_l.color
    text_l = ColorSensor.COLORS[color_l]
    return text_r, text_l


if __name__ == '__main__':
    # go_forward(speed=10, rotations=1)
    # sleep(10)
    # go_forward(speed=100, rotations=20)
    while True:
        print(get_colors())
        sleep(0.1)
