# Sonar callable by function
# Activated by button
# by Consiliarius


# Import required modules
import board
import pulseio
import time
import neopixel
import simpleio
"""
STARTUP SECTION: Runs once
"""

# Initialize Neopixel RGB LEDs
def set-rgb-leds:
    pixels = neopixel.NeoPixel(board.GP18, 2)
    pixels.fill(0)

color = 0
state = 0

# Define pin connected to piezo buzzer and pick some tunes
def set-buzzer-n-tones:
    PIEZO_PIN = board.GP22

# Initialize buttons
def set-buttons:
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
        self.listen =pulseio.PulseIn(board.GP1,maxlen=1)
    
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
Sonar = GroveUltrasonicTransceiver()


"""
RUN LOOP: Runs indefinitely
"""

while True:
    
    # Check button 1 (GP20)
    if not btn20.value:  # button 1 pressed 
        
        # Check the transceiver is sending realistic values back (max range ~350-400cm)...
        if GUT.get_distance() < 400:
            
            # ...if it is, signal with a tone & light up LEDS green...
            pixels.fill(11,102,36)
            simpleio.tone(PIEZO_PIN, 600, duration=0.1)
            time.sleep(0.2)
            simpleio.tone(PIEZO_PIN, 600, duration=0.8)
                       
            # and print distance to the console
            print('Surface is {} cm away'.format(Sonar.get_distance()))
            time.sleep(1)
       
        # ...and alert if value can't be trusted
        else:
            pixels.fill(255,0,0)
            simpleio.tone(PIEZO_PIN, 262, duration=0.5)
            
            print('Surface is over 4m away')
            time.sleep(1)
            
            
    elif not btn21.value:

# reset colour and debounce
    pixels.fill(0)
    time.sleep(0.05)