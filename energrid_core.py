#############################################
#               ENERGRID_CORE               #
#############################################

# 1 january 2020
# code by Alexandre TURREL https://github.com/alexandreturrel
# for Polytech Sorbonne Engineering project lead by Francois PECHEUX



## Energrid architecture to map all elements needed to the solution

import json
import logging
from datetime import datetime
import time

#############################################
#               ENERGRID_MQTT               #
#############################################

import paho.mqtt.client as PahoMqtt
import threading

class Client:

    debug = False

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


#=======================
#            led res tot
# 0A <-----> 870     870
# 1.150A <->     910 810
# 1.435A <-> 929     803
# 2.06A <--> 888 923 772
#=======================


    def on_message(self, client, userdata, message):
        logging.info('message received on %s', message.topic)
        parsed_topic = message.topic.split("/")
        current_house_id = str(parsed_topic[3])
        current_peripheral_category = str(parsed_topic[4])
        parsed_message = json.loads(message.payload)
        current_peripheral_id = None
        if len(parsed_topic) == 6:
            current_peripheral_id = parsed_topic[5]
        check = False
        if current_peripheral_category == "Consumer":
            #retrieving data from sensors
            if str(parsed_topic[-1]) == "Consumer":
                for key in parsed_message:
                    if str(key) != "0":
                        tmp_topic = "Neighborhood/0/House/" + current_house_id +"/"+ current_peripheral_category +"/"+str(key)
                    elif str(key) == "0":
                        tmp_topic = str(message.topic)
                    else:
                        break
                    for consumer in House.consumers:
                        if tmp_topic == consumer.name:
                            range1 = [0,1700]
                            range2 = [-15,15]
                            delta1 = range1[1]-range1[0]
                            delta2 = range2[1]-range2[0]
                            result = (delta2 * (parsed_message[key] - range1[0]) / delta1) + range2[0]
                            consumer.pull.update(time.time(), result)
                            if parsed_message[key] > 870:
                                consumer.pull.set_status(True)
                            else:
                                consumer.pull.set_status(False)
                check = True

        elif current_peripheral_category == "Supplier":
            #retrieving data from sensors
            if str(parsed_topic[-1]) == "Supplier":
                for each_id in parsed_message:
                    tmp_topic = "Neighborhood/0/House/" + current_house_id +"/"+ current_peripheral_category +"/"+str(each_id)
                    for supplier in House.suppliers:
                        if tmp_topic in supplier.name:
                            def src_v():
                                return supplier.src_voltage
                            def src_c():
                                return supplier.src_current
                            def push_v():
                                return supplier.push_voltage
                            def push_c():
                                return supplier.push_current
                            def battery_v():
                                return supplier.battery_voltage
                            def battery_c():
                                return supplier.battery_current
                            def battery_r():
                                return supplier.battery_remaining
                            options = {
                                "pvvoltage": src_v,
                                "pvcurrent": src_c,
                                "lvoltage": push_v,
                                "lcurrent": push_c,
                                "bvoltage": battery_v,
                                "bcurrent": battery_c,
                                "bremaining": battery_r,
                            }
                            for each_sensor in parsed_message[u'{}'.format(each_id)]:
                                if str(each_sensor) in options:
                                    options[u'{}'.format(each_sensor)]().update(time.time(), parsed_message[u'{}'.format(each_id)][u'{}'.format(each_sensor)])
                            check = True
                
        if check == False:
            print("Wrong peripheral")

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

    def set_status(self, new_status):
        self.state = new_status

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
        if identifier == '':
            self.name = house_name + "/Supplier"
        else:
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
        result["src_voltage"] = self.src_voltage.last
        result["src_current"] = self.src_current.last
        result["battery_voltage"] = self.battery_voltage.last
        result["battery_current"] = self.battery_current.last
        result["battery_remaining"] = self.battery_remaining.last
        result["push_voltage"] = self.push_voltage.last
        result["push_current"] = self.push_current.last
        return str(result)

#############################################
#                  CONSUMER                 #
#############################################
## Electricity Consumer part of a House
class Consumer:
    def __init__(self, identifier, house_name):
        logging.info('new Consumer created')
        self.id = identifier
        if identifier == '':
            self.name = house_name + "/Consumer"
        else:
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
        result["pull"] = self.pull.last
        return str(result)


#############################################
#                    HOUSE                  #
#############################################
class House:

    client = Client('GhostHouse')
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

        self.consumption = Consumer('',self.name)
        House.consumers.append(self.consumption)
        House.client.add_topic(self.consumption.name)
        self.supply = Supplier('',self.name)
        House.suppliers.append(self.supply)
        House.client.add_topic(self.supply.name)

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
        House.consumers.append(self.consumers[-1])
        self.client.add_topic(self.consumers[-1].name)

    def rm_consumer(self,old_consumer_name):
        for i in range(len(self.consumers)):
            if self.consumers[i].name == old_consumer_name:
                logging.info('Consumer %s removed from %s', old_consumer_name, self.name)
                self.client.rm_topic(old_consumer_name)
                self.consumers.pop(i)
                break
        for j in range(len(House.consumers)):
            if House.consumers[j].name == old_consumer_name:
                House.consumers.pop(j)
                break

    def add_supplier(self):
        logging.info('new Supplier add to the %s', self.name)
        House.last_supplier_id += 1
        self.last_supplier_id += 1
        self.suppliers.append(Supplier(self.last_supplier_id,self.name))
        House.suppliers.append(self.suppliers[-1])
        self.client.add_topic(self.suppliers[-1].name)

    def rm_supplier(self,old_supplier_name):
        for i in range(len(self.suppliers)):
            if self.suppliers[i].name == old_supplier_name:
                logging.info('Supplier %s removed from %s', old_supplier_name, self.name)
                self.client.rm_topic(old_supplier_name)
                self.suppliers.pop(i)
                break
        for j in range(len(House.suppliers)):
            if House.suppliers[j].name == old_supplier_name:
                House.suppliers.pop(j)
                break

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
        self.houses.append((House(self.last_house_id,self.name,0,0)))
        Neighborhood.houses.append(self.houses[-1])

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return "Neighborhood: " + self.name + "\n" + str(self.__dict__)

#############################################
#                    MAIN                   #
#############################################
if __name__ == "__main__":
    print("Energrid Core Imported")
