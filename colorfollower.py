#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_D, MoveSteering, SpeedPercent, MediumMotor
from ev3dev2.sensor import INPUT_1, INPUT_4, INPUT_3
from ev3dev2.sensor.lego import ColorSensor, InfraredSensor

from time import sleep

# define output names
OUTPUT_A = 'outA'
OUTPUT_B = 'outB'
OUTPUT_D = 'outD'

# define color sensors
COLOR_SENSOR_R = ColorSensor(address=INPUT_1)
COLOR_SENSOR_L = ColorSensor(address=INPUT_4)

# define InfraredSensor
INFRARED_SENSOR = InfraredSensor(address=INPUT_3)
PROXIMITY_THRESHOLD = 1.3

# define MoveSteering object
STEERING_DRIVE = MoveSteering(OUTPUT_D, OUTPUT_A)

# define arm motot
ARM_MOTOR = MediumMotor(OUTPUT_B)

# define speed
GO_FORWARD_SPEED = 4
TURN_SPEED = GO_FORWARD_SPEED

# define light intensity threshold
LIGHT_THRESHOLD = 15
STEERING_SCALAR = 1
SPEED_THRESHOLD = 25

# define colors rgb lists
RED_L = [130, 14, 17]
RED_R = [210, 17, 35]
BLUE_L = [17, 59, 90]
BLUE_R = [25, 57, 180]
GREEN_L = [12, 75, 32]
GREEN_R = [22, 70, 63]
BLACK_L = [16, 22, 19]
BLACK_R = [22, 22, 38]
WHITE_L = [100, 145, 110]
WHITE_R = [180, 175, 255]
MAX_EUCLIDEAN_DISTANCE = 510

# define pick up and delivery color
PACKAGE_COLOR = "Blue"
DELIVERY_COLOR = "Green"

# define the size of list with colors
NUM_OF_COLORS_IN_LIST = 10
# define how many colors in a row are needed to make a turn
NUM_OF_COLORS_TO_TURN = 5
# define how many colors in a row are needed to stop the car
NUM_OF_COLORS_TO_STOP = 8

# define frequency
FREQUENCY = 0.01


def euclidean_distance(vx, vy):
    '''
    calculate euclidean distance between vectors
    '''
    return sum((y-x)**2 for x, y in zip(vx, vy)) ** 0.5


class ColorFollower():

    def __del__(self):
        STEERING_DRIVE.off()

    def get_colors(self):
        '''
        returns one of three colors that is closest in euclidean distance
        returns Black, Blue, Green, White or Red
        '''
        COLOR_THRESHOLD = 60
        rgb_l = COLOR_SENSOR_L.rgb
        distances_l = {}
        distances_l['Black'] = euclidean_distance(rgb_l, BLACK_L)
        distances_l['Blue'] = euclidean_distance(rgb_l, BLUE_L)
        distances_l['Green'] = euclidean_distance(rgb_l, GREEN_L)
        distances_l['White'] = euclidean_distance(rgb_l, WHITE_L)
        distances_l['Red'] = euclidean_distance(rgb_l, RED_L)
        lowest_l = min(distances_l, key=distances_l.get)

        rgb_r = COLOR_SENSOR_R.rgb
        distances_r = {}
        distances_r['Black'] = euclidean_distance(rgb_r, BLACK_R)
        distances_r['Blue'] = euclidean_distance(rgb_r, BLUE_R)
        distances_r['Green'] = euclidean_distance(rgb_r, GREEN_R)
        distances_r['White'] = euclidean_distance(rgb_r, WHITE_R)
        distances_r['Red'] = euclidean_distance(rgb_r, RED_R)
        lowest_r = min(distances_r, key=distances_r.get)

        if distances_l[lowest_l] > COLOR_THRESHOLD or distances_r[lowest_r] > COLOR_THRESHOLD:
            return "Black", "Black"

        return lowest_l, lowest_r

    def rgb_to_intensity(self, color_sensor, sensor_is_left, color):
        '''
        color can be either Black, Blue, Green or Red
        '''
        rgb = color_sensor.rgb
        if color == "Black":
            if sensor_is_left:
                rgb_to_compare = BLACK_L
            else:
                rgb_to_compare = BLACK_R
        elif color == "Blue":
            if sensor_is_left:
                rgb_to_compare = BLUE_L
            else:
                rgb_to_compare = BLUE_R
        elif color == "Green":
            if sensor_is_left:
                rgb_to_compare = GREEN_L
            else:
                rgb_to_compare = GREEN_R
        else:
            raise ValueError("invalid color passed")
        intensity_rgb = euclidean_distance(rgb, rgb_to_compare) / MAX_EUCLIDEAN_DISTANCE * 100
        return intensity_rgb

    def adjust_color_steering(self, color):
        '''
        calculates and returns steering based on rgb intensity and color given to follow
        '''
        calculated_intensity_l = self.rgb_to_intensity(COLOR_SENSOR_L, sensor_is_left=True, color=color)
        calculated_intensity_r = self.rgb_to_intensity(COLOR_SENSOR_R, sensor_is_left=False, color=color)
        light_difference = (calculated_intensity_l - calculated_intensity_r)

        if light_difference > LIGHT_THRESHOLD:
            return 100
        if light_difference < -LIGHT_THRESHOLD:
            return -100
        if abs(light_difference) < 2:
            return 0
        return light_difference*STEERING_SCALAR

    def adjust_color_speed(self, steering):
        '''
        adjust speed based on turn angle
        '''
        if abs(steering) > SPEED_THRESHOLD:
            return SpeedPercent(TURN_SPEED)
        else:
            return SpeedPercent(GO_FORWARD_SPEED)

    def get_steering_and_speed_for_color_linefollowing(self, color):
        '''
        returns calculated steering and speed for given color
        '''
        color_steering = self.adjust_color_steering(color)
        # print('following ', color)
        color_speed = self.adjust_color_speed(color_steering)
        return color_steering, color_speed

    def last_elements_are_specific_color(self, colors_list, n, specific_color):
        '''
        check whether last n elements in a list are given color
        '''
        if len(colors_list) < n:
            return False
        return all([color == specific_color for color in colors_list[-n:]])

    def append_colors_lists(self, l_colors, r_colors):
        '''
        append list of colors with new colors and remove older colors
        '''
        l_color, r_color = self.get_colors()
        l_colors.append(l_color)
        if len(l_colors) > NUM_OF_COLORS_IN_LIST:
            l_colors.pop(0)
        r_colors.append(r_color)
        if len(r_colors) > NUM_OF_COLORS_IN_LIST:
            r_colors.pop(0)
        return l_colors, r_colors

    def check_whether_to_turn(self, l_colors, r_colors, color=PACKAGE_COLOR):
        '''
        checks whether a turn should be made and returns 'left', 'right' or None
        '''
        turn = None
        if self.last_elements_are_specific_color(colors_list=l_colors, specific_color=color, n=NUM_OF_COLORS_TO_TURN):
            if not self.last_elements_are_specific_color(colors_list=r_colors, specific_color=color, n=NUM_OF_COLORS_TO_TURN):
                turn = 'left'
        elif self.last_elements_are_specific_color(colors_list=r_colors, specific_color=color, n=NUM_OF_COLORS_TO_TURN):
            turn = 'right'
        return turn

    def at_square(self, l_colors, r_colors, color):
        '''
        return whether robot is at square of given color
        '''
        return self.last_elements_are_specific_color(colors_list=l_colors, specific_color=color, n=NUM_OF_COLORS_TO_STOP) and self.last_elements_are_specific_color(colors_list=r_colors, specific_color=color, n=NUM_OF_COLORS_TO_STOP)

    def deliver_package(self):
        '''
        function that runs whole delivery from start until the end
        '''
        l_colors = []
        r_colors = []
        while True:

            # append colors lists
            l_colors, r_colors = self.append_colors_lists(l_colors, r_colors)

            # check whether a turn should be made
            turn = self.check_whether_to_turn(l_colors, r_colors)
            if turn == 'left' or turn == 'right':
                # turn for 90 degrees and move forward for a second
                if turn == 'left':
                    turn_steering = -100
                else:
                    turn_steering = 100
                steering, speed = turn_steering, 7
                STEERING_DRIVE.on(steering, speed)
                print('TURNING BLUE')
                sleep(1.9)
                steering, speed = 0, 7
                STEERING_DRIVE.on(steering, speed)
                sleep(1)

                # follow PACKAGE_COLOR line until both are the same color (then we are on color square)
                l_colors = []
                r_colors = []
                while not self.at_square(l_colors, r_colors, PACKAGE_COLOR):
                    # append colors lists
                    l_colors, r_colors = self.append_colors_lists(l_colors, r_colors)
                    steering, speed = self.get_steering_and_speed_for_color_linefollowing(PACKAGE_COLOR)
                    STEERING_DRIVE.on(steering, speed)
                print('AT PACKAGE COLOR SQUARE')

                # use InfraredSensor
                proximity = INFRARED_SENSOR.proximity / 10    # 0 means 0cm, 100 means 7cm
                while not proximity < PROXIMITY_THRESHOLD:  # if proximity is below around 3cm
                    proximity = INFRARED_SENSOR.proximity / 10    # 0 means 0cm, 100 means 7cm
                    print('proximity = ', proximity)

                # stop at color
                steering, speed = 0, 0
                STEERING_DRIVE.on(steering, speed)

                # pick up the package
                ARM_MOTOR.on_for_degrees(speed=3, degrees=-50, brake=True, block=True)
                sleep(1)

                # move around 180 degrees
                steering, speed = 100, 7
                STEERING_DRIVE.on(steering, speed)
                sleep(4.2)  # TODO: adjust time sleep

                # follow DELIVERY_COLOR (green) until both sensors are the same color (then we are on color square)
                print('FOLLOWING DELIVERY_COLOR')

                turned_to_green = False
                while not turned_to_green:
                    l_colors = []
                    r_colors = []
                    while not turned_to_green:

                        # append colors lists
                        l_colors, r_colors = self.append_colors_lists(l_colors, r_colors)

                        # check whether a turn should be made
                        turn = self.check_whether_to_turn(l_colors, r_colors, color=DELIVERY_COLOR)
                        if turn == 'left' or turn == 'right':
                            # turn for 90 degrees and move forward for a second
                            if turn == 'left':
                                turn_steering = -100
                            else:
                                turn_steering = 100
                            steering, speed = turn_steering, 7
                            STEERING_DRIVE.on(steering, speed)
                            print('TURNING GREEN')
                            sleep(1.9)
                            steering, speed = 0, 7
                            STEERING_DRIVE.on(steering, speed)
                            sleep(1)
                            turned_to_green = True
                        else:   # if not making any turn just follow DELIVERY_COLOR line
                            steering, speed = self.get_steering_and_speed_for_color_linefollowing(DELIVERY_COLOR)
                            STEERING_DRIVE.on(steering, speed)

                # stopping at square
                l_colors = []
                r_colors = []
                while not self.at_square(l_colors, r_colors, DELIVERY_COLOR):
                    # append colors lists
                    l_colors, r_colors = self.append_colors_lists(l_colors, r_colors)
                    steering, speed = self.get_steering_and_speed_for_color_linefollowing(DELIVERY_COLOR)
                    STEERING_DRIVE.on(steering, speed)

                print('AT DELIVERY COLOR SQUARE')
                # stop at color
                steering, speed = 0, 0
                STEERING_DRIVE.on(steering, speed)

                # put down the package
                ARM_MOTOR.on_for_degrees(speed=3, degrees=50, brake=True, block=True)
                print('FINISHED, sleep for 10')
                sleep(10)

            else:   # if not making any turn just follow black line
                steering, speed = self.get_steering_and_speed_for_color_linefollowing("Black")
                STEERING_DRIVE.on(steering, speed)

    def print_sensors_rgb_for_configuration(self):
        while True:
            rgb_l = COLOR_SENSOR_L.rgb
            rgb_r = COLOR_SENSOR_R.rgb
            sleep(0.1)


if __name__ == '__main__':
    taczkowoz = ColorFollower()
    taczkowoz.deliver_package()
