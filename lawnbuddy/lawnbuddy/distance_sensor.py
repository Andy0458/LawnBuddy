import VL53L1X

sensor = None
sensing = False

def initialize():
    global sensor, sensing

    sensor = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
    sensor.open()
    sensing = False

def get_distance():
    global sensing
    
    # sensor hasn't been told to start transmitting
    if sensing == False:
        sensor.start_ranging(1)
        sensing = True
    return sensor.get_distance()

def stop_sensing():
    global sensing

    # Tell sensor to stop transmitting
    if sensing == True:
        sensing = False
        sensor.stop_sensing()