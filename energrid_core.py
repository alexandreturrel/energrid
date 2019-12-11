#############################################
#               ENERGRID_CORE               #
#############################################

## Energrid architecture to map all elements needed to the solution

import json
import logging
import datetime
import time

logging.basicConfig(filename='energrid' + str(datetime.datetime.now()) + '.log',filemode='a', format='%(asctime) - %(levelname)s - %(message)s', level=logging.DEBUG)


#############################################
#               ENERGRID_MQTT               #
#############################################

import paho.mqtt.client as PahoMqtt
import threading

class Client:

    debug = True

    OPTIONS = ['new', 'update', 'remove', 'status', 'database']

    def __init__(self,name):
        #core
        self.name = name
        self.client = PahoMqtt.Client(name)

        #callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.client.connected_flag = False

        #starting connection
        if Client.debug:
            print(self.name +' connecting...')
        self.client.connect('127.0.0.1', port=1883, keepalive=60, bind_address="")
        self.client.loop_start()
        self.topics=[]
        self.historic=[]
        while not self.client.connected_flag:
            time.sleep(.1)
        self.add_topic('')    #self subscribtion to edit components

    def add_topic(self, new_topic):
        if new_topic == '':
            tmp = self.name
        else:
            tmp = new_topic
        if Client.debug:
            print(self.name + '\t' + 'new topic added: ' + tmp + ' and subscription done')
        self.topics.append(tmp)
        self.client.subscribe(tmp, qos=2)
        self.client.message_callback_add(tmp, self.client.on_message)

    def rm_topic(self, old_topic):
        for i in range(len(self.topics)):
            if self.topics[i] == old_topic:
                if Client.debug:
                    print(self.name + '\t' + 'old topic removed: ' + old_topic + ' and unsubscription done')
                self.topics.pop(i)
                self.client.unsubscribe(old_topic)
                break

    def publish(self, topic, payload):
        if topic in self.topics:
            if Client.debug:
                tmp = topic + ' ' + payload
                print('publishing new message: ' + tmp)
            self.client.publish(topic, payload=payload, qos=2, retain=False)

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            if Client.debug:
                print('connection done.')
            self.client.connected_flag = True

    def on_message(self, client, userdata, message):
        print(message.topic)
        logging.info('message received on %s', message.topic)
        parsed_message = message.topic.split("/")
        current_house_id = parsed_message[3]
        current_peripheral_category = parsed_message[4]
        current_peripheral_id = parsed_message[5]
        check = False
        for consumer in House.consumers:
            print(consumer.name)
            if message.topic == consumer.name:
                consumer.pull.update(message.payload)
                check = True
        for supplier in House.suppliers:
            print(supplier.name)
            if message.topic == supplier.name:
                print(str(message.payload.decode("utf8")))
                check = True
        if check == False:
            print("Wrong peripheral")

#        result = {message.topic: str(message.payload.decode("utf-8"))}
#        self.historic.append(result)
#        infos = json.loads(message.payload)

#        for op in Client.OPTIONS:
#            if infos.get(op) is not None:
#                print "Success"
#        return result


    def on_disconnect(self, client, userdata, rc):
        if Client.debug:
            print(self.name + '\t' + 'disconnecting... reason: ' + str(rc))
            print('disconnected.')
        client.connected_flag = False
        client.disconnected_flag = True

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


#############################################
#              ENERGRID_OBJECTS             #
#############################################


#############################################
#                   DATA                    #
#############################################
# Pseudo database to test operations and serialization
## all data retrieved from the electric grid is homogeneous
## it can be used for all requests
class Data:
    def __init__(self):
        logging.info('new Data created')
        self.last = 0
        self.values = 0
        self.db_timestamp = []
        self.db_values = []
        self.mean = 0
        self.max = 0
        self.min = 0
        self.state = False

    def mean_update(self,db):
        logging.debug('Data mean updated')
        return sum(db)/len(db)

    def update(self, timestamp, value):
        logging.debug('Data updated')
        self.last = value
        if self.values == 0:
            self.max = value
            self.min = value
        self.values += 1
        self.db_timestamp.append(timestamp)
        self.db_values.append(value)
        self.mean = self.mean_update(self.db_values)
        if value > self.max:
            self.max = value
        if value < self.min:
            self.min = value

    def __repr__(self):
        result = {}
        result["last"] = self.last
        result["values"] = self.values
        result["mean"] = self.mean
        result["max"] = self.max
        result["min"] = self.min
        if self.state:
            result["state"] = "TRUE"
        else:
            result["state"] = "FALSE"
        return str(self.__dict__)

#############################################
#                  SUPPLIER                 #
#############################################
## Electricity Supplier part of a House
class Supplier:
    def __init__(self, identifier, house_name):
        logging.info('new Supplier created')
        self.id = identifier
        self.name = house_name + "/Supplier/" + str(self.id)
        self.type = ""
        self.src_voltage = Data()
        self.src_current = Data()
        self.battery_voltage = Data()
        self.battery_current = Data()
        self.battery_remaining = Data()
        self.push_voltage = Data()
        self.push_current = Data()

    def set_type(self, new_type):
        logging.debug('Supplier type updated')
        self.type = str(new_type)

    def __repr__(self):
        result = {}
        result["id"] = self.id
        result["name"] = self.name
        result["type"] = self.type
        result["src_voltage"] = self.src_voltage
        result["src_current"] = self.src_current
        result["battery_voltage"] = self.battery_voltage
        result["battery_current"] = self.battery_current
        result["battery_remaining"] = self.battery_remaining
        result["push_voltage"] = self.push_voltage
        result["push_current"] = self.push_current
        return str(result)

#############################################
#                  CONSUMER                 #
#############################################
## Electricity Consumer part of a House
class Consumer:
    def __init__(self, identifier, house_name):
        logging.info('new Consumer created')
        self.id = identifier
        self.name = house_name + "/Consumer/" + str(self.id)
        self.type = ""
        self.pull = Data()

    def set_type(self, new_type):
        logging.debug('Consumer type updated')
        self.type = str(new_type)

    def __repr__(self):
        result = {}
        result["id"] = self.id
        result["name"] = self.name
        result["type"] = self.type
        result["pull"] = self.pull
        return str(result)


#############################################
#                    HOUSE                  #
#############################################
class House:

    client = Client('GenericHouse')
    last_consumer_id = 0
    last_supplier_id = 0
    suppliers = []
    consumers = []


    def __init__(self, identifier, neighborhood_name, suppliers_qntity, consumers_qntity):
        logging.info('new House created')
        ##core
        self.id = identifier
        self.name = neighborhood_name + "/House/" + str(self.id)
        self.client = Client(self.name)
        self.client.on_message = self.on_message

        self.consumption = Consumer(0,self.name)
        House.consumers.append(self.consumption)
        self.supply = Supplier(0,self.name)
        House.suppliers.append(self.supply)

        #suppliers
        self.last_supplier_id = 0
        self.suppliers = []
        for i in range(suppliers_qntity):
            self.add_supplier()

        #consumers
        self.last_consumer_id = 0
        self.consumers = []
        for i in range(consumers_qntity):
            self.add_consumer()

    def add_consumer(self):
        logging.info('new Consumer add to the %s', self.name)
        self.last_consumer_id += 1
        self.consumers.append(Consumer(self.last_consumer_id,self.name))
        House.last_consumer_id += 1
        House.consumers.append(Consumer(House.last_consumer_id,self.name))
        self.client.add_topic(self.consumers[-1].name)

    def rm_consumer(self,old_consumer_name):
        for i in range(len(self.consumers)):
            if self.consumers[i].name == old_consumer_name:
                logging.info('Consumer %s removed from %s', old_consumer_name, self.name)
                self.client.rm_topic(old_consumer_name)
                self.consumers.pop(i)
                break

    def add_supplier(self):
        logging.info('new Supplier add to the %s', self.name)
        self.last_supplier_id += 1
        self.suppliers.append(Supplier(self.last_supplier_id,self.name))
        House.last_supplier_id += 1
        House.suppliers.append(Supplier(House.last_supplier_id,self.name))
        self.client.add_topic(self.suppliers[-1].name)

    def rm_supplier(self,old_supplier_name):
        for i in range(len(self.suppliers)):
            if self.supppliers[i] == old_supplier_name:
                logging.info('Supplier %s removed from %s', old_supplier_name, self.name)
                self.suppliers.pop(i)
                self.client.rm_topic(old_supplier_name)

    def on_message(self, client, userdata, message):
        print("House")
        logging.info('message received on %s', message.topic)
        parsed_message = message.topic.split("/")
        current_house_id = parsed_message[3]
        current_peripheral_category = parsed_message[4]
        current_peripheral_id = parsed_message[5]
        if message.topic in House.consumers:
            print(str(message.payload.decode("utf8")))
        elif message.topic in House.suppliers:  #Supplier
            print(str(message.payload.decode("utf8")))
        else:
            print("Invalid Peripheral")
        return 0

    def consume(self):
        logging.debug('%s consumption updated', self.name)
        result = 0
        for i in self.consumers:
            result += i.pull.last
        return result

    def supply(self):
        logging.debug('%s supply updated', self.name)
        result = [0.,0.,0.,0.,0.,0.,0.]
        for i in self.suppliers:
            result[0] += i.src_voltage.last
            result[1] += i.src_current.last
            result[2] += i.battery_voltage.last
            result[3] += i.battery_current.last
            result[4] += i.battery_remaining.last
            result[5] += i.push_voltage.last
            result[6] += i.push_current.last
        return result

    def __repr__(self):
        return str(self.__dict__)

#############################################
#                NEIGHBORHOOD               #
#############################################
class Neighborhood:
    nb_id = 0

    client = Client('GenericNeighborhood')
    last_house_id = 0
    houses = []

    def __init__(self, quantity_houses):
        logging.info('new Neighborhood created')
        self.id = Neighborhood.nb_id
        Neighborhood.nb_id += 1
        self.name = "Neighborhood/" + str(self.id)
        self.last_house_id = 0
        self.houses = []
        for i in range(quantity_houses):
            self.add_house()

    def global_consume(self):
        logging.debug('%s global consumption updated', self.name)
        result = 0
        for i in self.houses:
            result += i.consume()
        return result

    def add_house(self):
        logging.info('add new House to %s', self.name)
        self.last_house_id += 1
        self.houses.append((House(self.last_house_id,self.name,1,1)))

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return "Neighborhood: " + self.name + "\n" + str(self.__dict__)

#############################################
#                    MAIN                   #
#############################################
if __name__ == "__main__":
    print("Energrid Core Imported")
