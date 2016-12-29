# What is this thing?

A Python tool for monitoring status of home router, modem, and ISP connectivity. Logs and reports up time for each with email and auto-Twitter shaming built-in.

It's currently running on my Raspberry Pi and flashes the lights according to whose fault it is that our internet isn't working at the moment.

# If you want to put it on a Raspberry Pi...

You'll probably want:

 * A Raspberry Pi (~$35) https://www.amazon.com/Raspberry-Pi-RASP-PI-3-Model-Motherboard/dp/B01CD5VC92/ref=sr_1_2?s=pc&ie=UTF8&qid=1482521044&sr=1-2&keywords=raspberry+pi
 * A Raspberry Pi case (~$10) https://www.amazon.com/Official-Raspberry-Pi-Case-Black/dp/B01F1PSFY6/ref=sr_1_6?s=pc&ie=UTF8&qid=1482521085&sr=1-6&keywords=raspberry+pi
 * A way to plug-in your Pi with a *MicroUSB* cable and wall plug. (~$10). You might already have one of these from an old smartphone, but be warned that Apple lightning and the newer but similar-looking USB Type C WON'T WORK. 
 * A small MicroSD card (~$5) https://www.amazon.com/SanDisk-microSDHCTM-8GB-Memory-Card/dp/B0012Y2LLE/ref=sr_1_6?s=pc&ie=UTF8&qid=1482521123&sr=1-6&keywords=micro+sd+card+8gb
 * A way to read/write/format the MicroSD card from your computer (~$10) https://www.amazon.com/Lexar-Professional-microSDHC-UHS-II-LSDMI32GCBNL1000R/dp/B00U77V8AM/ref=sr_1_9?s=pc&ie=UTF8&qid=1482521192&sr=1-9&keywords=micro+sd+card+usb

Then you'll need to load the OS onto the MicroSD card (I recommend Raspbian using NOOBS), setup the wifi, and then install this software.

You may also find it useful to configure an SSH login for your Pi:

    sudo raspi-config
    # Interfacing options -> ssh -> Enable
    # Also, set a password for the pi user
    # Make sure you set the local time zone to get correct reporting
    reboot

# Installing

    # Dependencies
    sudo pip-3.2 install python-twitter
    sudo pip-3.2 install python-dateutil
    
    # Configure your Raspberry Pi's on-board LED to be accessible from user-space
    ./led-setup.sh
    
    # Grab the code from github
    git clone https://github.com/jhclark/tattletale.git

# Configuring

Copy tattletale.conf.template to tattletale.conf and fill in your information.

At minimum, you'll need to set:
 * Router IP
 * Modem IP

    cp tattletale.conf.template tattletale.conf
    nano tattletale.conf

For bonus points, you can set up:
 * Gmail integration to get sent reports. If you're using two-factor authentication (you should be), then you'll need to generate an application specific password.
 * Twitter integration to auto-shame your ISP when it's their fault.

# Running

    cd tattletale
    python3 tattletale.py

# Manually viewing the database

You'll need sqlite on the command line:

    sudo apt-get install sqlite

Then you can do this to get a CSV file:

    sqlite3 -header -csv tattletale.db "select * from events;"
