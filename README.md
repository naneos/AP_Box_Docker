# AP_Box_Docker
With the Docker Solution Grafana + InfluxDB + log2ram (longer lifetime of the SD-Card) everything as in the AP_Box_database solution shoult be possible.

## Setting up the Raspberry Pi 4
I recommend using the Raspberry [Pi Imager](https://www.raspberrypi.org/downloads/ "Pi Imager Download Page"). Write the standard Rasperri Pi Os (~1GB) on an SD-Card.
If headless connection is needed optionally add a empty file called ssh to the root directory of the boot partition.

More information about SSH connection can be found on the Rasperry Pi foundation's site.
I've switched over to a static IP because dynamic IP caused problems when accessing in different networks (@home and @work).

When connected I recommend updating the system. This can take some time!
```Bash
sudo apt update
sudo apt full-upgrade
```

## Installing Docker
For my first Docker atttempt I used this [video](https://www.youtube.com/watch?time_continue=29&v=a6mjt8tWUws&feature=emb_logo). The exact installation process for our naneos box will be described in this section.

First install IOTstack from github and start ./menu.sh.
```Bash
git clone https://github.com/gcgarner/IOTstack.git
cd IOTstack
./menu.h
```

Now you can install Docker and the following conatiners: portainer, nodered, influx, grafana, python.
Then I recommend to deactivate Swap + activate log2ram in the miscellaneous section of ./menu.sh.

-