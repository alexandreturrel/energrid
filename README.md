# Energrid

## Creators: 
DABBOUS TALA	DE VERGNES BENOIT	TURREL ALEXANDRE

## Description
A Smart grid management solution with a Virtual Reality interface.

## Supervision Server
The solution needs a supervision server to coordinate all peripherals and the VR interface

This server runs on a Debian machine with:
 - python 2.7
 - mosquitto-server
 - mariadb-server
 - nginx
 - php
 - php-fpm
 - git

### How does it work?

#### energrid-core.py
contains all classes used to run the solution

#### energrid-mqtt.py
connects the instances created with energrid-core.py to the correct mqtt topics

#### energrid-db.py
connects the instances created with energrid-core.py to the correct database entries

#### energrid-server.py
links all services together and supervise the grid
