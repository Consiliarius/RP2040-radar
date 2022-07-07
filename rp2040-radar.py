# Radar callable by function
# by Consiliarius

"""
STARTUP SECTION: Runs once
"""

# Import require modules
import board
import pulseio
import time

# Create the class to control the sensor
class GroveUltrasonicTransceiver(object):
    # At initialisation, bind a pin (GP1) to receive digital pulses, and store one pulse at a time as variable
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
GUT = GroveUltrasonicTransceiver()


"""
RUN LOOP: Runs indefinitely
"""

while True:
    # Check the transceiver is sending realistic values back (max range ~350-400cm)...
    if GUT.get_distance() < 400:
        print('Surface is {} cm away'.format(GUT.get_distance()))
    # ...and alert if value can't be trusted
    else:
        print('Surface is over 4m away')
    # Wait a moment, then go again
    time.sleep(2.5)