import time
import smbus

BUS = None # I2C Bus
address = 0x42 # address of device on bus

# Placeholder
#GPSDAT = {
#    'strType': None,
#    'fixTime': None,
#    'lat': None,
#    'latDir': None,
#    'lon': None,
#    'lonDir': None,
#    'fixQual': None,
#    'numSat': None,
#    'horDil': None,
#    'alt': None,
#    'altUnit': None,
#    'galt': None,
#    'galtUnit': None,
#    'DPGS_updt': None,
#    'DPGS_ID': None
#}

def initialize():
    global BUS
    BUS = smbus.SMBus(1)

def parse_response(gps_line):
    gps_chars = ''.join(chr(c) for c in gps_line)
    if "*" not in gps_chars:
        return False
    gps_data = {}
    # Checksum after string, separated with '*'
    gps_str, chk_sum = gps_chars.split('*')    
    gps_components = gps_str.split(',')
    gps_start = gps_components[0]
    #print(gps_str)
    if (gps_start == "$GNGGA"):
        # Check checksum
        chkVal = 0
        for ch in gps_str[1:]: # Remove the $
            chkVal ^= ord(ch)
        if (chkVal == int(chk_sum, 16)):
            # String sent over I2C will be formatted 'strType,fixTime,lat,latDir,...,DPGS_ID\n'
            for i, k in enumerate(['strType', 'fixTime', 'lat', 'latDir', 'lon', 'lonDir', 'fixQual', 
                    'numSat', 'horDil', 'alt', 'altUnit', 'galt', 'galtUnit', 'DPGS_updt', 'DPGS_ID']):
                gps_data[k] = gps_components[i]
            #print(gps_data)
            try:
                float(gps_data['lat'])
                float(gps_data['lon'])
                return gps_data
            except Exception:
                return None
    return None

def read_gps():
    b = None
    response = []
    try:
        # Read to new line or bad character
        while True:
            b = BUS.read_byte(address)
            # not ready
            if b == 255:
                return False
            # new line
            elif b == 10:
                break
            else:
                response.append(b)
        return parse_response(response)
    except IOError:
        # Something went wrong, reconnect to device
        time.sleep(0.5)
        initialize()
    except Exception, e:
        print e
