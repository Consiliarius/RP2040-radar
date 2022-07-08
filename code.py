# Sonar callable by function
# Activated by button
# by Consiliarius


# Import required modules
import board
import time
import pulseio
import simpleio
import digitalio
import neopixel

"""
STARTUP SECTION: Runs once
"""

# Initialize Neopixel RGB LEDs
pixels = neopixel.NeoPixel(board.GP18, 2)
pixels.brightness=0.33
pixels.fill(0)

color = 0
state = 0

# Define pin connected to piezo buzzer and pick some tunes
PIEZO_PIN = board.GP22

# Initialize buttons
btn20 = digitalio.DigitalInOut(board.GP20)
btn21 = digitalio.DigitalInOut(board.GP21)
btn20.direction = digitalio.Direction.INPUT
btn21.direction = digitalio.Direction.INPUT
btn20.pull = digitalio.Pull.UP
btn21.pull = digitalio.Pull.UP



# Create the class to control the sensor
class GroveUltrasonicTransceiver(object):
    # At initialisation, bind a pin (GP28) to receive digital pulses, and store one pulse at a time as variable
    def __init__(self):
        self.listen =pulseio.PulseIn(board.GP28,maxlen=1)
    
    # Send, receive and interpret pulses to/from the sensor
    def _get_distance(self):
        # Ensure the pin value is 0
        self.listen.pause()
        self.listen.clear()
        # Define & set other required variables to zero.
        self.ping =0
        self.distance=0
        
        # Transmit a single pulse of 10microseconds to the sensor/tranceiver:
        # This will trigger one ping (and one ping only, Vassily!) to be sent,
        # and give time for returning pulse to be read and saved
        self.listen.resume(10)
        time.sleep(0.1)
       
        # Stop listening for pulses, set the pulse length (microseconds) as ping, 
        self.listen.pause()
        self.ping =self.listen[0]
        
        # Calculate distance and round to two decimals for readability;
        # the distance to an object is one half of:
        # speed of sound (in cm/microseconds) * length of pulse (in microseconds)
        distance =round((self.ping  * 0.034027 / 2),2)
        return distance
    
    # Output the distance as an attribute    
    def get_distance(self):
        while True:
            dist = self._get_distance()
            if dist:
                return dist

# Call the transceiver class
sonar = GroveUltrasonicTransceiver()


"""
RUN LOOP: Runs indefinitely
"""

while True:
    
    # Check button 1 (GP20)
    if not btn20.value:  # button 1 pressed 
        
        # Check the transceiver is sending realistic values back (max range ~350-400cm)...
        if sonar.get_distance() < 400:
            
            # ...if it is, signal with a tone & light up LEDs green...
            print('Surface is {} cm away'.format(sonar.get_distance()))
            pixels.fill([11,102,36])
            simpleio.tone(PIEZO_PIN, 4978, duration=0.05)
            time.sleep(0.05)
            simpleio.tone(PIEZO_PIN, 4978, duration=0.2)
            time.sleep(0.25)
            
        # ...and alert if value can't be trusted in console, tone and LEDs
        else:
            print('Surface is over 4m away')
            pixels.fill([255,0,0])
            simpleio.tone(PIEZO_PIN, 4978, duration=0.05)
            time.sleep(0.05)
            simpleio.tone(PIEZO_PIN, 58, duration=0.4)
            time.sleep(0.5)
            
            
# reset colour and debounce
    pixels.fill(0)
    time.sleep(0.05)