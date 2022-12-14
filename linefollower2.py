#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, MoveSteering, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import ColorSensor
from time import sleep

# define output names
OUTPUT_A = 'outA'
OUTPUT_D = 'outD'

# define color sensors
color_sensor_r = ColorSensor(address=INPUT_1)
color_sensor_l = ColorSensor(address=INPUT_4)

# define MoveSteering object
steering_drive = MoveSteering(OUTPUT_D, OUTPUT_A)

# define speed
go_forward_speed = 40, used 40, 50
turn_speed = 38, used 29, 30

# define light intensity threshold
light_threshold = 60
STEERING_SCALAR = 1
SPEED_THRESHOLD = 25   # 25


def follow_line():

    def adjust_steering():
        print(color_sensor_l.reflected_light_intensity, color_sensor_r.reflected_light_intensity)
        # TODO: remember which side was black last time, then turn in that direction (90 degree corner solution)
        # TODO: find crossing solution, NOTE: works
        light_difference = color_sensor_l.reflected_light_intensity - color_sensor_r.reflected_light_intensity
        if light_difference > light_threshold:
            # print('turning')
            return 75
        if light_difference < -light_threshold:
            # print('turning')
            return -75
        # print(color_sensor_l.reflected_light_intensity, color_sensor_r.reflected_light_intensity)
        # print('not turnings')
        return light_difference*STEERING_SCALAR

    def adjust_speed(steering):
        if abs(steering) > SPEED_THRESHOLD:
            return SpeedPercent(turn_speed)
        else:
            return SpeedPercent(go_forward_speed)

    while True:
        # color_sensor_l.calibrate_white()
        # color_sensor_r.calibrate_white()
        sleep(0.1)
        steering = adjust_steering()
        speed = adjust_speed(steering)
        steering_drive.on(steering, speed)


if __name__ == '__main__':
    try:
        follow_line()
    except KeyboardInterrupt:
        steering_drive.off()
