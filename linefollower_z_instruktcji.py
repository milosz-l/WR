#!/usr/bin/env python3
import ev3dev.ev3 as ev3
ts = ev3.TouchSensor()
m = ev3.LargeMotor('outA')
m.run_timed(time_sp=3000, speed_sp=500)
while True:
    ev3.Leds.set_color(ev3.Leds.LEFT, (ev3.Leds.GREEN, ev3.Leds.RED)[ts.value()])