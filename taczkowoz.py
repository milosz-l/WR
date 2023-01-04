#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_D, MoveSteering, SpeedPercent, MediumMotor, SpeedDPS
from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import ColorSensor
from time import sleep
import math


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
go_forward_speed = 7
turn_speed = 7

# define light intensity threshold
light_threshold = 18
STEERING_SCALAR = 1
SPEED_THRESHOLD = 25

# define colors rgb lists
RED_L = [130, 14, 17]
RED_R = [210, 17, 35]
BLUE_L = [16, 55, 90]
BLUE_R = [27, 58, 180]
GREEN_L = [12, 75, 32]
GREEN_R = [22, 70, 63]
WHITE_L = [100, 145, 110]
WHITE_R = [180, 175, 255]
BLACK_L = [10, 15, 15]
BLACK_R = [15, 15, 30]
MAX_EUCLIDEAN_DISTANCE = 510


def euclidean_distance(vx, vy):
    return sum((y-x)**2 for x, y in zip(vx, vy)) ** 0.5


def taczkowoz():

    # def get_steering_and_speed_for_linefollowing():
    #     def adjust_steering():
    #         light_difference = color_sensor_l.reflected_light_intensity - color_sensor_r.reflected_light_intensity
    #         if light_difference > light_threshold:
    #             return 100
    #         if light_difference < -light_threshold:
    #             return -100
    #         if light_difference < 15:
    #             return 0
    #         return light_difference*STEERING_SCALAR

    #     def adjust_speed(steering):
    #         if abs(steering) > SPEED_THRESHOLD:
    #             return SpeedPercent(turn_speed)
    #         else:
    #             return SpeedPercent(go_forward_speed)

    #     steering = adjust_steering()
    #     speed = adjust_speed(steering)
    #     return steering, speed

    def get_colors():
        '''
        returns tuple of two strings: (left_color, right_color)
        '''
        color_r = color_sensor_r.color
        text_r = ColorSensor.COLORS[color_r]
        color_l = color_sensor_l.color
        text_l = ColorSensor.COLORS[color_l]
        return text_l, text_r

    def get_steering_and_speed_for_color_linefollowing(color):
        def rgb_to_intensity(color_sensor, sensor_is_left, color=color):
            '''
            color can be either black, blue or red
            '''
            rgb = color_sensor.rgb
            if color == "Black":
                if sensor_is_left:
                    rgb_to_compare = BLACK_L
                else:
                    rgb_to_compare = BLACK_R
                # intensity_rgb = ((rgb[0] + rgb[1] + rgb[2]) / (256*3)) * 100    # returns white intensity
            elif color == "Blue":
                if sensor_is_left:
                    rgb_to_compare = BLUE_L
                else:
                    rgb_to_compare = BLUE_R
                # intensity_rgb = 100 - (rgb[2] / 256) * 100
            elif color == "Green":
                if sensor_is_left:
                    rgb_to_compare = GREEN_L
                else:
                    rgb_to_compare = GREEN_R
            elif color == "Red":
                if sensor_is_left:
                    rgb_to_compare = RED_L
                else:
                    rgb_to_compare = RED_R
                # intensity_rgb = 100 - (rgb[0] / 256) * 100
            else:
                raise ValueError("invalid color passed")
            intensity_rgb = euclidean_distance(rgb, rgb_to_compare) / 510 * 100
            return intensity_rgb

        def adjust_color_steering():
            calculated_intensity_l = rgb_to_intensity(color_sensor_l, True)
            calculated_intensity_r = rgb_to_intensity(color_sensor_r, False)
            # print("looking for", color, calculated_intensity_l, calculated_intensity_r)
            print("looking for", color)

            # adjust intensity to be percentage
            # light_sum = calculated_intensity_l + calculated_intensity_r

            # light_difference = calculated_intensity_l - calculated_intensity_r
            # light_difference = (calculated_intensity_l - calculated_intensity_r) / light_sum * 100
            light_difference = (calculated_intensity_l - calculated_intensity_r)

            print(light_difference)
            if light_difference > light_threshold:
                return 100
            if light_difference < -light_threshold:
                return -100
            if abs(light_difference) < 6:
                return 0
            # if light_sum < 15:
            #     return 0
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

    PACKAGE_COLOR = "Blue"
    DELIVERY_COLOR = "Green"
    NUM_OF_COLORS_IN_LIST = 10
    l_colors = []
    r_colors = []
    while True:
        # append colors lists
        l_color, r_color = get_colors()
        l_colors.append(l_color)
        if len(l_colors) > NUM_OF_COLORS_IN_LIST:
            l_colors.pop(0)
        r_colors.append(r_color)
        if len(r_colors) > NUM_OF_COLORS_IN_LIST:
            r_colors.pop(0)

        # set steering and speed
        turn = None
        if last_elements_are_specific_color(colors_list=l_colors, specific_color=PACKAGE_COLOR, n=3):
            if not last_elements_are_specific_color(colors_list=r_colors, specific_color=PACKAGE_COLOR, n=3):
                turn = 'left'
        elif last_elements_are_specific_color(colors_list=r_colors, specific_color=PACKAGE_COLOR, n=3):
            turn = 'right'

        if turn == 'left' or turn == 'right':

            # turn to PACKAGE_COLOR and follow black line until both are the same color (then we are on color square)
            l_colors = []
            r_colors = []
            while not (last_elements_are_specific_color(colors_list=l_colors, specific_color=PACKAGE_COLOR, n=8) and last_elements_are_specific_color(colors_list=r_colors, specific_color=PACKAGE_COLOR, n=8)):
                # append colors lists
                l_color, r_color = get_colors()
                l_colors.append(l_color)
                if len(l_colors) > NUM_OF_COLORS_IN_LIST:
                    l_colors.pop(0)
                r_colors.append(r_color)
                if len(r_colors) > NUM_OF_COLORS_IN_LIST:
                    r_colors.pop(0)
                steering, speed = get_steering_and_speed_for_color_linefollowing(PACKAGE_COLOR)
                steering_drive.on(steering, speed)

            # stop at color
            steering, speed = 0, 0
            steering_drive.on(steering, speed)

            # pick up the package
            arm_motor.on_for_degrees(speed=20, degrees=-50, brake=True, block=True)
            sleep(1)

            # move around 180 degrees
            steering, speed = 100, 5
            steering_drive.on(steering, speed)
            sleep(2)  # TODO: adjust time sleep

            # put down then package # TODO: move this below green following
            arm_motor.on_for_degrees(speed=20, degrees=50, brake=True, block=True)
            sleep(1)

            # follow DELIVERY_COLOR (green) until both sensors are the same color (then we are on color square)
            l_colors = []
            r_colors = []
            while not (last_elements_are_specific_color(colors_list=l_colors, specific_color=DELIVERY_COLOR, n=8) and last_elements_are_specific_color(colors_list=r_colors, specific_color=DELIVERY_COLOR, n=8)):
                # append colors lists
                l_color, r_color = get_colors()
                l_colors.append(l_color)
                if len(l_colors) > NUM_OF_COLORS_IN_LIST:
                    l_colors.pop(0)
                r_colors.append(r_color)
                if len(r_colors) > NUM_OF_COLORS_IN_LIST:
                    r_colors.pop(0)
                steering, speed = get_steering_and_speed_for_color_linefollowing(DELIVERY_COLOR)
                steering_drive.on(steering, speed)

        else:
            # steering, speed = get_steering_and_speed_for_linefollowing()
            steering, speed = get_steering_and_speed_for_color_linefollowing("Black")
            steering_drive.on(steering, speed)


if __name__ == '__main__':
    try:
        taczkowoz()
    except KeyboardInterrupt:
        steering_drive.off()
