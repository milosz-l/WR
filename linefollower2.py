#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, MoveSteering, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import ColorSensor

# define output names
OUTPUT_A = 'outA'
OUTPUT_D = 'outD'

# define color sensors
color_sensor_r = ColorSensor(address=INPUT_1)
color_sensor_l = ColorSensor(address=INPUT_4)

# define MoveSteering object
steering_drive = MoveSteering(OUTPUT_D, OUTPUT_A)

# define speed
go_forward_speed = 30
turn_speed = 10

# define light intensity threshold
light_threshold = 50


def follow_line():

    def adjust_steering():
        print(color_sensor_l.reflected_light_intensity, color_sensor_r.reflected_light_intensity)
        light_difference = color_sensor_l.reflected_light_intensity - color_sensor_r.reflected_light_intensity
        if light_difference > light_threshold:
            return 100
        if light_difference < -light_threshold:
            return -100
        return light_difference

    def adjust_speed(steering):
        if abs(steering) > 25:
            return SpeedPercent(turn_speed)
        else:
            return SpeedPercent(go_forward_speed)

    while True:
        steering = adjust_steering()
        speed = adjust_speed(steering)
        steering_drive.on(steering, speed)


if __name__ == '__main__':
    try:
        follow_line()
    except KeyboardInterrupt:
        steering_drive.off()
