import random
import geopy.distance
from math import sqrt

STOP_ACCEL_THRESHOLD = 1 # adjustable, to be changed when mower is constructed and tested

# RandomSpiralPathAlgorithm
# Behavior: Will move forward in a straight line for a random distance. Then the mower will move in an outward spiral.
#           If one of the following 3 criteria:
#               1) mower hits an obstacle - currently defined as acceleration meeting a threshold
#               2) mower is not within mowing region
#               3) mower is within ~3 (adjustable) inches of obstacle in front
#           Then the mower will stop, turn a random angle in the opposite general direction,
#           and continue on. This will repeat as the mower is powered.
# Pros: This is a relatively simple algorithm, and provides an improvement on the RandomLinePathAlgorithm on large open areas.
# Cons: Is not the most efficient way of covering the entire area and will take longer to cover corners.
class RandomSpiralPathAlgorithm():

    mowing_region = None
    last_stopped_position = None
    distance_to_stop = None
    is_moving_in_spiral = False

    def __init__(self, mowing_region):
        self.mowing_region = mowing_region

    def run(self, gps_data, acceleration, gyro_data, magnet_data, front_distance):
        current_pos = (gps_data['lat'], gps_data['lon'])

        # Start spirals
        if (
            self.last_stopped_position != None 
            and self.distance_to_stop != None
            and geopy.distance.geodesic(self.last_stopped_position, current_pos).feet >= self.distance_to_stop
        ):
            self.is_moving_in_spiral = True
            # motors.changeRightMotorSpeed(.05) # set right motor slow to turn right clockwise

        # Need to stop and turn
        if (
            sqrt(acceleration['x']**2 + acceleration['y']**2 + acceleration['z']**2) > STOP_ACCEL_THRESHOLD 
            or not self.mowing_region.contains((gps_data['lat'], gps_data['lon']))
            or front_distance < 75 # will hit something 75mm ~ 3 inches away
        ):
            # motors.stop()
            # turn random between 112 and 248 degrees, guarantees it points opposite general direction
            direction = random.randint(112, 248)
            self.last_stopped_position = (gps_data['lat'], gps_data['lon'])
            self.distance_to_stop = random.random() * 2 + 3 # random distance between 3 and 5 feet
            self.is_moving_in_spiral = False
            # motors.turn(direction)
            # motors.start() # resume
        
        if self.is_moving_in_spiral:
            # motors.incrementRightMotorSpeed(.01) # small change to perform clockwise outward spiral
            pass