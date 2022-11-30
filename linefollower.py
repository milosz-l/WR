#!/usr/bin/env python3
import ev3dev.ev3 as ev3


# define output names
OUTPUT_A = 'outA'
OUTPUD_D = 'oudD'

# define wheel motors
motor_r = ev3.LargeMotor(OUTPUT_A)
motor_l = ev3.LargeMotor(OUTPUD_D)

# define go_forward function
def go_forward(speed=100, time=0.2):
    '''
    runs both motors at the same time, what makes the car go forward
    speed is a percentage between 0 and 100
    time is in seconds
    '''
    # TODO: change below (driving with two motors)
    # motor_r.on_for_rotations(ev3.SpeedPercent(speed), 5)
    # motor_l.on_for_rotations(ev3.SpeedPercent(speed), 5)
    tank_drive = ev3.MoveTank(OUTPUT_A, OUTPUD_D)

    # drive in a turn for 5 rotations of the outer motor
    # the first two parameters can be unit classes or percentages.
    tank_drive.on_for_rotations(ev3.SpeedPercent(50), ev3.SpeedPercent(75), 10)

    # drive in a different turn for 3 seconds
    tank_drive.on_for_seconds(ev3.SpeedPercent(60), ev3.SpeedPercent(30), 3)


if __name__ == '__main__':
    # TODO: code below
    m = ev3.LargeMotor('outA')
    m.run_timed(time_sp=3000, speed_sp=500)
    while True:
        ev3.Leds.set_color(ev3.Leds.LEFT, (ev3.Leds.GREEN, ev3.Leds.RED)[ts.value()])