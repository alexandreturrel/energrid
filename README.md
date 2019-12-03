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
 - python 2.7
     - paho-mqtt (pip install paho-mqtt)
     - ~~mysql-connector (pip install mysql-connector)~~
 - pip
 - mosquitto-server
 - git
 - ~~influxdb for realtime database capabilities : [link](https://www.framboise314.fr/utiliser-le-protocole-mqtt-pour-communiquer-des-donnees-entre-2-raspberry-pi/ "Tutorial to install Influxdb, Telegraf and Chronograf")~~
 - ~~telegraf~~
 - ~~chronograf~~

### How does it work?

#### energrid_core.py - a0.9
contains all classes used to run the solution

#### energrid_mqtt.py - a0.8
connects the instances created with energrid-core.py to the correct mqtt topics

#### energrid_db.py - 
~~connects the instances created with energrid-core.py to the correct database entries~~

#### energrid_server.py - a0.2
links all services together and supervise the grid
