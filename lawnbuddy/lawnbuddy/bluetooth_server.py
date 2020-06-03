import bluetooth
import struct

bluetooth_broadcast_name = "PiLawnMower"
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

def collect_latlng_history():
    server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_socket.bind(("", bluetooth.PORT_ANY))
    server_socket.listen(1)

    port = server_socket.getsockname()[1]

    bluetooth.advertise_service(server_socket, bluetooth_broadcast_name, service_id=uuid,
                                service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                                profiles=[bluetooth.SERIAL_PORT_PROFILE],
                                )

    print("Waiting for connection on RFCOMM channel ", port)

    client_socket, address = server_socket.accept()
    print("Accepted connection from ", address)
    print(client_socket)

    # Get number of locations
    res = client_socket.recv(1024)
    num_locations = struct.unpack('>i', res)[0]
    i = 0

    locations = []
    print("NUM LOCATIONS : %d" % (num_locations))
    while i < num_locations:
        res = client_socket.recv(1024)
        latitude = struct.unpack('>d', res)[0]

        res = client_socket.recv(1024)
        longitude = struct.unpack('>d', res)[0]

        locations.append((latitude, longitude))
        #print(str(latitude)+","+str(longitude))
        print("Received: (%f,%f)" % (latitude, longitude))

        i += 1

    client_socket.close()
    server_socket.close()

    return locations