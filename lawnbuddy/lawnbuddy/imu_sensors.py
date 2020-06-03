import FaBo9Axis_MPU9250
import time
import sys

imu_device = None

def initialize():
    global imu_device

    imu_device = FaBo9Axis_MPU9250.MPU9250()

    # Configure device to output +- 250 degrees per sec and accelerometer to +-4g
    imu_device.configMPU9250(FaBo9Axis_MPU9250.GFS_250, FaBo9Axis_MPU9250.AFS_4G)

def read_sensors():
    global imu_device

    acceleration = gyro = magnet = None

    try:
        acceleration = imu_device.readAccel()
    # print("AccelX = ", acceleration['x'])
    # print("AccelY = ", acceleration['y'])
    # print("AccelZ = ", acceleration['z'])
    except Exception:
        pass

    try:
        gyro = imu_device.readGyro()
    # print("GyroX = ", gyro['x'])
    # print("GyroY = ", gyro['y'])
    # print("GyroZ = ", gyro['z'])
    except Exception: 
        pass
   
    try:
        magnet = imu_device.readMagnet()
    # print("MagX = ", magnet['x'])
    # print("MagY = ", magnet['y'])
    # print("MagZ = ", magnet['z'])
    except Exception:
        pass

    return acceleration, gyro, magnet
