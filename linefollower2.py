#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, MoveSteering, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import ColorSensor
#from time import sleep

# define output names
OUTPUT_A = 'outA'
OUTPUT_D = 'outD'

# define color sensors
color_sensor_r = ColorSensor(address=INPUT_1)
color_sensor_l = ColorSensor(address=INPUT_4)

# define MoveSteering object
steering_drive = MoveSteering(OUTPUT_D, OUTPUT_A)

# define speed
go_forward_speed = 50
turn_speed = 25

# define light intensity threshold
light_threshold = 50
STEERING_SCALAR = 1
SPEED_THRESHOLD = 25


def follow_line():

    def adjust_steering():
        # print(color_sensor_l.reflected_light_intensity, color_sensor_r.reflected_light_in$
        # TODO: remember which side was black last time, then turn in that direction (90 d$
        # TODO: find crossing solution, NOTE: works
        light_difference = color_sensor_l.reflected_light_intensity - color_sensor_r.refle$
        if light_difference > light_threshold:
            # print('turning')
            return 100
        if light_difference < -light_threshold:
            # print('turning')
            return -100
        # print(color_sensor_l.reflected_light_intensity, color_sensor_r.reflected_light_in$
        #print('not turnings')
        if light_difference < 15:
            return -5
        return light_difference*STEERING_SCALAR

    def adjust_speed(steering):
        if abs(steering) > SPEED_THRESHOLD:
            return SpeedPercent(turn_speed)
        else:
            return SpeedPercent(go_forward_speed)

    while True:
        # sleep(0.1)
        # color_sensor_l.calibrate_white()
        # color_sensor_r.calibrate_white()
        steering = adjust_steering()
        speed = adjust_speed(steering)
        steering_drive.on(steering, speed)


if __name__ == '__main__':
    try:
        follow_line()
    except KeyboardInterrupt:
        steering_drive.off()
