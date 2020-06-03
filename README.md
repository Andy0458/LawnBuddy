# LawnBuddy
The Lawn Buddy mower bot eliminates one of the biggest burdens of maintaining a grass lawn. There is no need for a user to push around a large machine, because the bot utilizes autonomous technology to navigate the lawn. Troublesome pull-start mechanisms, traditional gas engine maintenance, and physical demands of lawnmowing are no longer a hassle.

This git repository contains the source code for the project, include the Android application and the python package built for the Raspberry Pi 4.

## Installing
First, clone the repository: 

```
git clone https://github.com/Andy0458/LawnBuddy.git
```

Building the Android application involves opening the project in Android Studio, and building.

To install the dependencies for the python package, simply run:

```
cd LawnBuddy/lawnbuddy
sudo pip install -r requirements.txt
```


## Running
To run the python code on a Raspberry Pi, simply do the following:

```
cd lawnbuddy
sudo python lawnbuddy.py
```

This will launch the program. First, it will require that a mowing region be sent via the Android Application.

To do this, first power the RaspberryPi on, pair to 'PiLawnMower' on your Android device, and step through the app. Once a region has been captured, press the export button in the top right of the app. This will connect to the Pi and transmit the gathered data. Then the program will begin running.
