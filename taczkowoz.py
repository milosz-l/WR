#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_D, MoveSteering, SpeedPercent, MediumMotor
from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import ColorSensor
from time import sleep

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
go_forward_speed = 5
turn_speed = 5

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
        print(text_l, text_r)
        return text_l, text_r

    def get_steering_and_speed_for_color_linefollowing(color, color_sensor):
        def rgb_to_intensity(color=color):
            '''
            color can be either black, blue or red
            '''
            rgb = color_sensor.rgb
            if color == "black":
                intensity_rgb = 100 - ((rgb[0] + rgb[1] + rgb[2]) / (256*3))
            elif color == "blue":
                intensity_rgb = 100 - (rgb[2] / 256)
            elif color == "red":
                intensity_rgb = 100 - (rgb[0] / 256)
            return intensity_rgb

        def adjust_color_steering(color=color):
            calculated_intensity_l = rgb_to_intensity(color, color_sensor_l)
            calculated_intensity_r = rgb_to_intensity(color, color_sensor_r)
            light_difference = calculated_intensity_l - calculated_intensity_r
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

    def last_elements_are_specific_color(colors_list, n=5, specific_color="Blue"):
        return all([color == specific_color for color in colors_list[-n:]])

    PACKAGE_COLOR = "Red"  # or blue przetestowac
    NUM_OF_COLORS_IN_LIST = 10
    l_colors = []
    r_colors = []
    while True:
        # sleep(0.1)
        # color_sensor_l.calibrate_white()
        # color_sensor_r.calibrate_white()

        # append colors lists
        l_color, r_color = get_colors()
        l_colors.append(l_color)
        if len(l_colors) > NUM_OF_COLORS_IN_LIST:
            l_colors.pop(0)
        r_colors.append(r_color)
        if len(r_colors) > NUM_OF_COLORS_IN_LIST:
            r_colors.pop(0)

        ##
        turn = None
        if last_elements_are_specific_color(colors_list=l_colors, specific_color=PACKAGE_COLOR):
            if not last_elements_are_specific_color(colors_list=r_colors, specific_color=PACKAGE_COLOR):
                turn = 'left'
        elif last_elements_are_specific_color(colors_list=r_colors, specific_color=PACKAGE_COLOR):
            turn = 'right'

        if turn == 'left' or turn == 'right':
            # TODO: turn right or left 90 degrees and go forward for one square
            if turn == 'left':
                steering = -100
            elif turn == 'right':
                steering = 100
            turning_sleep_time = 0.55*turn_speed
            steering_drive.on(steering, turn_speed)
            print("sleeping at turn for ", turning_sleep_time)
            sleep(turning_sleep_time)

            go_forward_sleep_time = 0.1*go_forward_speed
            steering_drive.on(0, go_forward_speed)
            print("sleeping at go forward for ", go_forward_sleep_time)
            sleep(go_forward_sleep_time)

            # TODO: turn to PACKAGE_COLOR and follow black line until both are the same color (then we are on color square)
            while not (last_elements_are_specific_color(colors_list=l_colors, specific_color=PACKAGE_COLOR) and last_elements_are_specific_color(colors_list=r_colors, specific_color=PACKAGE_COLOR)):
                steering, speed = get_steering_and_speed_for_color_linefollowing()
                steering_drive.on(steering, speed)

            # TODO: change to delivery color

            # DONE: stop at color
            # steering, speed = 0, 0
            # steering_drive.on(steering, speed)
        else:
            steering, speed = get_steering_and_speed_for_linefollowing()
            steering_drive.on(steering, speed)


if __name__ == '__main__':
    try:
        taczkowoz()
    except KeyboardInterrupt:
        steering_drive.off()
