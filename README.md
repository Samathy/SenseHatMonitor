# SenseHatMonitor
Code for the STEM Digital project at Rolls-Royce PLC. Monitors all sensors on a RaspPi SenseHAT

This project aims to regually gather data from the sensors on a SenseHAT and deposit that data into a CSV file for layer analysis.

# Requirements

(All below are Rasbian packages)

 * ephiphany-browser
 * matchbox
 * python3
 * sense-hat
 * python3-pip
 * usbmount
 * of-spi2-core
 * git

Pip
 * Python3 websockets

Other
 * chartjs (wget https://github.com/chartjs/Chart.js/releases/download/v2.6.0/Chart.js)


#Installation instructions

 1: Clone this repo into the home of the 'pi' user. To use another user, replace
    any instances of 'pi' in the source files with your given user.
 2: Download all the Debian package requirements and the Pip requirements.
 3: wget chartjs into the folder in which this repo has been downloaded
 4: Run 
    sudo ./install
 5: move to /usr/local/bin and run

    sudo ln -s /home/pi/sensehatmonitor/SenseHatMonitor.py .

 6: open the usbmount settings file with:

    sudo vi /etc/usbmount

 7: Edit the file system options line and add:

    -fstype=vfat,umask=000

 8: Copy the .xinit file into 'pi's root home with:

    cp ../.xinitrc ~/
