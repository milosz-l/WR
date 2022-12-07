from ev3dev2.sensor.lego import TouchSensor, ColorSensor
from ev3dev2.sensor import INPUT_1, INPUT_3, INPUT_4
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveSteering, SpeedPercent
```
#!/usr/bin/env python3


class LineFollower:
    def __init__(self, straight_speed, curve_speed, input_ports, output_ports):
        self.straight_speed = straight_speed
        self.curve_speed = curve_speed
        self.input_ports = input_ports
        self.output_ports = output_ports
        self.light_intensity_threshold = 50

        self.color_sensor_left = ColorSensor(self.input_ports.get("color_sensor_left"))
        self.color_sensor_right = ColorSensor(self.input_ports.get("color_sensor_right"))
        self.touch_sensor = TouchSensor(self.input_ports.get("touch_sensor"))
        self.steering = MoveSteering(self.output_ports.get('left_motor'), self.output_ports.get('right_motor'))

    def drive(self):
        print('Waiting for button click...')
        self.touch_sensor.wait_for_bump()

        while True:
            steering_result = self.calc_steering_angle()
            self.steering.on(steering_result, self.calc_speed(steering_result))

            # if self.on_off_button.is_pressed:
            #         self.wait_for_button_unpress(DEFAULT_BUTTON_WAIT_INTERVAL)
            #         self.movement.off()
            #         break

    def calc_speed(self, steering):
        if abs(steering) > 25:
            self.speed = SpeedPercent(self.curve_speed)
        else:
            self.speed = SpeedPercent(self.straight_speed)
        return self.speed

    def calc_steering_angle(self):
        light_intensity_difference = self.color_sensor_left.reflected_light_intensity - self.color_sensor_right.reflected_light_intensity

        if light_intensity_difference > self.light_intensity_threshold:
            return 100
        if light_intensity_difference < -self.light_intensity_threshold:
            return -100
        return light_intensity_difference


```
