# Radar callable by function
# by Consiliarius

# Import require modules
import board
import pulseio
import time


# create class
class GroveUltrasonicTransceiver(object):
    def __init__(self):
        self.listen =pulseio.PulseIn(board.GP1,maxlen=1)
    
    def _get_distance(self):
        # set variables to zero 
        self.ping =0
        self.distance=0
        
        # Clear the stored ping
        self.listen.pause()
        self.listen.clear()
        
        # Transmit a fresh one for 10microseconds to send ONE PING ONLY and pause to let it return
        self.listen.resume(10)
        time.sleep(0.5)
       
        # Stop listening, write the pulse length
        self.listen.pause()
        self.listen.pause()
        self.ping =self.listen[0]
        
        # Calculate distance (distance to object is half of length of pulse times cm travelled by sound in microseconds
        # Then round to two decimals for readability
        distance =round((self.ping  * 0.034027 / 2),2)
        
        return distance
        
    def get_distance(self):
        while True:
            dist = self._get_distance()
            if dist:
                return dist

GUT = GroveUltrasonicTransceiver()


# Run radar indefinitely

while True:
    if GUT.get_distance() < 400:
        print('Surface is {} cm away'.format(GUT.get_distance()))
    else:
        print('Surface is over 4m away')
    time.sleep(0.5)