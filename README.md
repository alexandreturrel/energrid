# Energrid

## Creators: 
 
DABBOUS TALA | DE VERGNES BENOIT | TURREL ALEXANDRE
-------------|-------------------|------------------
VR Software Manager | Hardware & Electronics Manager | Server & Data Manager

## Description
A Smart grid management solution with a Virtual Reality interface.

## Supervision Server
The solution needs a supervision server to coordinate all peripherals and the VR interface

This server runs on a Debian machine with:
 - python3
     - paho-mqtt
     - ~~influxdb~~
     - ~~mysql-connector (pip install mysql-connector)~~
 - pip
 - mosquitto-server
 - mosquitto-clients
 - git
 - ~~influxdb for realtime database capabilities : [link](https://www.framboise314.fr/utiliser-le-protocole-mqtt-pour-communiquer-des-donnees-entre-2-raspberry-pi/ "Tutorial to install Influxdb, Telegraf and Chronograf")~~
 - ~~telegraf~~
 - ~~chronograf~~

### Installation

	sudo apt update
	sudo apt upgrade
	sudo apt install pip3 mosquitto mosquitto-server mosquitto-clients git
	git clone https://github.com/alexandreturrel/energrid.git
	cd energrid/
	sudo pip3 install -r requirements.txt
	chmod +x energrid

### How does it work?

Just
	./energrid
Or
	python -i start_server.py

#### energrid_core.py - 1.0
contains all classes used to run the solution

#### start_server.py - a0.5
links all services together and supervise the grid

#### energrid - a0.5
starts an interactive python interpreter with all dependencies and start the server

comments:

0A value is 870 on analog values

1.150A	910	LED		810
1.435A	929	resistor	803
2.06A	888(led)	923(resistor)	led+ressistor	0: 772

