import bluetooth_server
import distance_sensor
import gps_sensor
import imu_sensors
from shapely.geometry import Polygon
from random_line_pathing import RandomLinePathAlgorithm
from random_spiral_pathing import RandomSpiralPathAlgorithm
import time

STOP_ACCEL_THRESHOLD = 5
pathing_handler = None

def main():
    global pathing_handler

    mowing_region = generate_mowing_region(bluetooth_server.collect_latlng_history())

    initialize_sensors()

    pathing_handler = RandomLinePathAlgorithm(mowing_region)
    # pathing_handler = RandomSpiralPathAlgorithm(mowing_region)

    run_loop()

def generate_mowing_region(location_history):
    location_history.append(location_history[0]) # Polygon requires first and last point to be same to enclose area
    return Polygon(location_history)

def initialize_sensors():
    distance_sensor.initialize()
    gps_sensor.initialize()
    imu_sensors.initialize()

def run_loop():
    global pathing_handler
    while True:
        current_front_distance = gps_data = acceleration = gyro = magnet = None
        # Read sensor data
        while gps_data == None or gps_data == False: # wait for valid reading from gps. Can take some time
            gps_data = gps_sensor.read_gps()
        current_front_distance = distance_sensor.get_distance()
        acceleration, gyro, magnet = imu_sensors.read_sensors()

        print("\n################Sensor Data##################")
        if current_front_distance != None:
            print("Current Distance from nearest object in front of mower: %dmm" % (current_front_distance))
        if gps_data != False and gps_data != None:
            print("Current GPS Coordinates (Lat, Lng): (%f,%f)" % (float(gps_data['lat']), float(gps_data['lon'])))
        if acceleration != None:
            print("AccelX = ", acceleration['x'])
            print("AccelY = ", acceleration['y'])
            print("AccelZ = ", acceleration['z'])
        if gyro != None:
            print("GyroX = ", gyro['x'])
            print("GyroY = ", gyro['y'])
            print("GyroZ = ", gyro['z'])
        if magnet != None:
            print("MagX = ", magnet['x'])
            print("MagY = ", magnet['y'])
            print("MagZ = ", magnet['z'])
        print("#############################################\n")

        pathing_handler.run(gps_data, acceleration, gyro, magnet, current_front_distance)

        #time.sleep(0.1)

if __name__ == '__main__':
    main()
