#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_D, SpeedPercent, MoveSteering
from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.wheel import EV3Tire
from time import sleep


# define output names
OUTPUT_A = 'outA'
OUTPUT_D = 'outD'

# define wheel motors
motor_r = LargeMotor(OUTPUT_A)
motor_l = LargeMotor(OUTPUT_D)

# define color sensors
color_sensor_r = ColorSensor(address=INPUT_1)
color_sensor_l = ColorSensor(address=INPUT_4)

# define MoveSteering object
steering_drive = MoveSteering(OUTPUT_D, OUTPUT_A)


def go_forward(speed=100, rotations=2):
    '''
    runs both motors at the same time, what makes the car go forward
    speed is a percentage between 0 and 100
    time is in seconds
    '''
    # TODO: change below (driving with two motors)
    # motor_r.on_for_rotations(ev3.SpeedPercent(speed), 5)
    # motor_l.on_for_rotations(ev3.SpeedPercent(speed), 5)
    tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)
    # tank_drive.on_for_rotations(SpeedPercent(speed), SpeedPercent(speed), rotations)
    tank_drive.on(SpeedPercent(speed), SpeedPercent(speed))


def turn(speed=100, speed_divisor=3, rotations=2, direction='right'):
    '''
    turns
    speed_divisor is between -100 and 100 (-100 turns in place)
    '''
    if direction == 'right':
        if speed_divisor == 0:
            speed_r = 0
        else:
            speed_r = speed/speed_divisor
        speed_l = speed
    else:
        if speed_divisor == 0:
            speed_l = 0
        else:
            speed_l = speed/speed_divisor
        speed_r = speed
    tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)
    # tank_drive.on_for_rotations(SpeedPercent(speed_r), SpeedPercent(speed_l), rotations)
    tank_drive


def get_colors():
    '''
    returns tuple of two strings: (right_color, left_color)
    '''
    color_r = color_sensor_r.color
    text_r = ColorSensor.COLORS[color_r]
    color_l = color_sensor_l.color
    text_l = ColorSensor.COLORS[color_l]
    print(text_r, text_l)
    return text_r, text_l


def follow_black(speed=30, go_forward_rotations=0.05, turn_rotations=0.05):
    '''
    black is in the middle of sensors
    '''
    def can_go_forward():
        color_r, color_l = get_colors()
        if color_r == 'black' and color_l != 'black':
            return True
        return False

    def both_not_black():
        color_r, color_l = get_colors()
        if color_r != 'black' and color_l != 'black':
            return True
        return False

    def right_not_black():
        color_r, _ = get_colors()
        if color_r != 'black':
            return True
        return False

    def left_is_black():
        _, color_l = get_colors()
        if color_l == 'black':
            return True
        return False

    def right_is_black():
        color_r, _ = get_colors()
        if color_r == 'black':
            return True
        return False

    # on_black_sensor = color_sensor_r
    # on_left_sensor = color_sensor_l
    while True:
        # if right_not_black() or left_is_black:  # go left condition
        #     turn(speed=speed, speed_divisor=-1, rotations=turn_rotations, direction='left')
        # elif
        # elif can_go_forward():
        #     go_forward(speed=speed, rotations=go_forward_rotations)
        # else:
        #     go_forward(speed=speed, rotations=go_forward_rotations)
        if left_is_black():
            turn(speed=speed, speed_divisor=-1, rotations=turn_rotations, direction='left')
        elif right_is_black():
            turn(speed=speed, speed_divisor=-1, rotations=turn_rotations, direction='right')
        else:
            go_forward(speed=speed, rotations=go_forward_rotations)


if __name__ == '__main__':
    # ---------------------------------------

    # # go_forward test
    # go_forward(speed=10, rotations=1)
    # sleep(10)
    # go_forward(speed=100, rotations=20)

    # # colors test
    # while True:
    #     print(get_colors())
    #     sleep(0.1)

    # # turn test
    # turn(speed=100, speed_divisor=100, rotations=1, direction='right')
    # go_forward(speed=100, rotations=1)
    # turn(speed=100, speed_divisor=100, rotations=1, direction='left')

    diameter_in_mm = 81.6
    tire = EV3Tire(diameter_mm=diameter_in_mm)
    # calculate the number of rotations needed to travel forward 500 mm
    rotations_for_500mm = 500 / tire.circumference_mm

    follow_black()
