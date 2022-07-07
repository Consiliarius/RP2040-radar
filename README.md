# RP2040-radar

This is a simple circuitpython script that uses a Seeed Grove Ultrasonic Ranger (https://www.seeedstudio.com/Grove-Ultrasonic-Distance-Sensor.html).

Pin GP1 is used for both the trigger pulse and the return pulse, the width of which is the time (in microseconds) it took for the sensor to transmit and receive the echo of an ultrasonic (40Khz+) burst.

Every 2.5 seconds the distance to the object in front of the sensor is calculated (max range of around 4m - the script will alert you if the sonar's out of range of an object) and then printed to console in human-friendly format:

"The object is x cm away"
or
"The object is over 4m away"

