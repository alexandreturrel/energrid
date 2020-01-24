# Energrid - Serverside Management Documentation

## Description
A Smart grid management solution with a Virtual Reality interface. 
The code and documentation here is to troubleshoot and debug on a serverside level with a simple CLI.

## Supervision Server
The solution needs a supervision server to coordinate all peripherals and the VR interface.

### Platform support

Any Unix based system. See the installation instructions below to get more details.
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

 > ~~tools that will be used in following updates~~

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

You can go to the Example section below to see how to use the CLI

### Files

#### energrid_core.py - 1.0
Contains all classes used to run the solution

##### Classes & Methods

###### Client - custom MQTT Client

	__init__(self,name): create a new MQTT Client with its name
	add_topic(self, new_topic): subscribe to a new_topic
	rm_topic(self, old_topic): unsubscribe to an old_topic
	publish(self, topic, payload): publish payload on topic
	disconnect(self): disconnect from the MQTT broker
	on_connect(self, client, userdata, flags, rc): standard callback
	on_message(self, client, userdata, message): callback used to write into the Neighborhood architecture. WARNING! the message may have to be a JSON string format
	on_disconnect(self, client, userdata, rc): standard callback
	__repr__(self): debug method for printing data
	__str__(self): debug method for printing data

###### Data - core class used to store the data retrieved from the sensors

	__init__(self): create a new empty Data object
	mean_update(self,db): method used when update() is called to update the average value
	update(self, timestamp, value): update the last database entry with its timestamp
	set_status(self, new_status): update the status of an object (mainly to see the information from the VR interface)
	__repr__(self): debug method for printing data

###### Supplier - core class simulating a real energy supplier

	__init__(self, identifier, house_name): create a new empty Supplier object and affect it to house_name
	set_type(self, new_type): update the type of the Supplier (mainly to statistic use)
	__repr__(self): debug method for printing data


###### Consumer - core class simulating a real energy consumer

	__init__(self, identifier, house_name): create a new empty Consumer object and affect it to house_name
	set_type(self, new_type): update the type of the Consumer (mainly to statistic use)
	__repr__(self): debug method for printing data

###### House - core class simulating a house

	__init__(self, identifier, neighborhood_name, suppliers_qntity, consumers_qntity): create a new House with an ID, affects it to a neighborhood_name and generate suppliers and consumers
	add_consumer(self): method called if a new consumer is affected to the house
	rm_consumer(self,old_consumer_name): method called if an old consumer has to be removed from the house
	add_supplier(self): method called if a new supplier is affected to the house
	rm_supplier(self,old_supplier_name): method called if an old supplier has to be removed from the house
	consume(self): return how many Amps the house is consuming at the last sensor reading timestamp
	~~ supply(self): return how many Amps the house is supplying at the last sensor reading timestamp ~~ not fully functionnal
	__repr__(self): debug method for printing data

###### Neighborhood - core class simulating a full neighborhood

	__init__(self, quantity_houses): creates a new Neighborhood with quantity_houses
	global_consume(self): return how many Amps all houses are comsuming at the last sensor reading timestamp
	add_house(self): method called if a new house is affected to the neighborhood
	__repr__(self): debug method for printing data
	__str__(self): debug method for printing data

#### start_server.py - 1.0
links all services together and supervise the grid

##### Class & Methods

	debug(boolean value): toggle DEBUG mode ON or OFF
	help(): shows how to use the commands
	newHouse(): creates a new House
	newHouse(int VALUE): creates VALUE new Houses
	showHouses(): display all Houses available
	newConsumer(int HouseID, string Type): creates a new Consumer for HouseID
	newConsumer(int HouseID, int X, string Type): creates X new Consumers for HouseID
	showConsumers(int HouseID): shows all Consumers of HouseID
	showConsumers(int HouseID,int CsmID): shows ConsumerID of HouseID
	setConsumer(int HouseID, int CsmID, [0,1]): set on or off a Consumer
	newSupplier(int HouseID, string Type): creates a new Supplier for HouseID
	newSupplier(int HouseID, int X, string Type): creates X new Suppliers for HouseID
	showSuppliers(int HouseID): shows all Suppliers of HouseID
	showSuppliers(int HouseID,int SplID): shows SupplierID of HouseID
	setSupplier(int HouseID, int SplID, [0,1]): set on or off a Supplier
	startDemo(): Demonstration purpose generative script (in french)

#### energrid - 1.0
starts an interactive python interpreter with all dependencies and start the server

### Examples

	./energrid # starts the CLI

	>>> newHouse(2) # creates 3 houses

	>>> newConsumer(1,2,'LED') # creates 2 LEDs Consumer for House n°1
	>>> newConsumer(2,'Lamp') # creates 1 Lamp Consumer for House n°2

	>>> newSupplier(1,2,'Solar Panel') # creates 2 Solar Panels for House n°1
	>>> newSupplier(2,'Wind Turbine') # creates 1 Wind Turbine Supplier for House n°2

	>>> showHouses() # shows the status of all the houses with their consumers and suppliers

	>>> showHouse(1) # shows all consumers and suppliers with the consumption and supply levels for House N°1

	>>> setConsumer(2,1,1) # turns ON the Lamp in House N°2
	>>> setConsumer(2,1,0) # turns OFF the Lamp in House N°2

Or

	./energrid # starts the CLI

	>>> startDemo() # starts a demonstration purpose environment and scripts a neighborhood generation with 2 Houses with 3 consumers each and 1 supplier
	>>> showHouses() # shows the status of all the houses with their consumers and suppliers

## Creators: 
 
DABBOUS TALA | DE VERGNES BENOIT | TURREL ALEXANDRE
-------------|-------------------|------------------
VR Software Manager | Hardware & Electronics Manager | Server & Data Manager
