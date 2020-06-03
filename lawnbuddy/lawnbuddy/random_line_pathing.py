import random
from math import sqrt

STOP_ACCEL_THRESHOLD = 1 # adjustable, to be changed when mower is constructed and tested

# RandomLinePathAlgorithm
# Behavior: Will move forward in a straight line. If one of the following 3 criteria:
#               1) mower hits an obstacle - currently defined as acceleration meeting a threshold
#               2) mower is not within mowing region
#               3) mower is within ~3 (adjustable) inches of obstacle in front
#           Then the mower will stop, turn a random angle in the opposite general direction,
#           and continue on. This will repeat as the mower is powered.
# Pros: This is a simple algorithm, useful if perfection is not so important. Can get a good
#       result when run often.
# Cons: Is not the most efficient way of covering the entire area.
class RandomLinePathAlgorithm():

    mowing_region = None

    def __init__(self, mowing_region):
        self.mowing_region = mowing_region

    def run(self, gps_data, acceleration, gyro_data, magnet_data, front_distance):
        if (
            sqrt(acceleration['x']**2 + acceleration['y']**2 + acceleration['z']**2) > STOP_ACCEL_THRESHOLD 
            or not self.mowing_region.contains((float(gps_data['lat']), float(gps_data['lon'])))
            or front_distance < 75 # will hit something 75mm ~ 3 inches away
        ):
            # motors.stop()
            # turn random between 112 and 248 degrees, guarantees it points opposite general direction
            direction = random.randint(112, 248)
            # motors.turn(direction)
            # motors.start() # resume
