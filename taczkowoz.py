#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_D, MoveSteering, SpeedPercent, MediumMotor
from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import ColorSensor
#from time import sleep

# define output names
OUTPUT_A = 'outA'
OUTPUT_B = 'outB'
OUTPUT_D = 'outD'

# define color sensors
color_sensor_r = ColorSensor(address=INPUT_1)
color_sensor_l = ColorSensor(address=INPUT_4)

# define MoveSteering object
steering_drive = MoveSteering(OUTPUT_D, OUTPUT_A)

# define arm motot
arm_motor = MediumMotor(OUTPUT_B)

# define speed
go_forward_speed = 10  # 5
turn_speed = 5  # 4

# define light intensity threshold
light_threshold = 20
STEERING_SCALAR = 1
SPEED_THRESHOLD = 25


def taczkowoz():

    def get_steering_and_speed_for_linefollowing():
        def adjust_steering():
            light_difference = color_sensor_l.reflected_light_intensity - color_sensor_r.reflected_light_intensity
            if light_difference > light_threshold:
                return 100
            if light_difference < -light_threshold:
                return -100
            if light_difference < 15:
                return 0
            return light_difference*STEERING_SCALAR

        def adjust_speed(steering):
            if abs(steering) > SPEED_THRESHOLD:
                return SpeedPercent(turn_speed)
            else:
                return SpeedPercent(go_forward_speed)

        steering = adjust_steering()
        speed = adjust_speed(steering)
        return steering, speed

    def get_colors():
        '''
        returns tuple of two strings: (left_color, right_color)
        '''
        color_r = color_sensor_r.color
        text_r = ColorSensor.COLORS[color_r]
        color_l = color_sensor_l.color
        text_l = ColorSensor.COLORS[color_l]
        print(text_r, text_l)
        return text_l, text_r

    def get_steering_and_speed_for_color_linefollowing():
        def adjust_color_steering():
            light_difference = color_sensor_l.reflected_light_intensity - color_sensor_r.reflected_light_intensity
            if light_difference > light_threshold:
                return 100
            if light_difference < -light_threshold:
                return -100
            if light_difference < 15:
                return 0
            return light_difference*STEERING_SCALAR

        def adjust_color_speed(steering):
            if abs(steering) > SPEED_THRESHOLD:
                return SpeedPercent(turn_speed)
            else:
                return SpeedPercent(go_forward_speed)

        color_steering = adjust_color_steering()
        color_speed = adjust_color_speed(color_steering)
        return color_steering, color_speed

    while True:
        # sleep(0.1)
        # color_sensor_l.calibrate_white()
        # color_sensor_r.calibrate_white()

        PACKAGE_COLOR = "green"  # or blue przetestowac

        l_color, r_color = get_colors()
        if l_color == PACKAGE_COLOR or r_color == PACKAGE_COLOR:
            # TODO: turn to PACKAGE_COLOR and follow black line until both are the same color (then we are on color square)
            # while l_color != PACKAGE_COLOR and r_color != PACKAGE_COLOR:
            steering, speed = 0, 0

        else:
            steering, speed = get_steering_and_speed_for_linefollowing()
        steering_drive.on(steering, speed)


if __name__ == '__main__':
    try:
        taczkowoz()
    except KeyboardInterrupt:
        steering_drive.off()
