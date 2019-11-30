#############################################
#               ENERGRID_MQTT               #
#############################################

import paho.mqtt.client as PahoMqtt
import time
import threading
import json

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
        if old_topic in self.topics:
            self.topics.pop(old_topic)
            self.client.unsubscribe(old_topic)

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
        result = {message.topic: str(message.payload.decode("utf-8"))}
        self.historic.append(result)
        #infos = json.loads(message.payload) # you can use json.loads to convert string to json

        #for op in Client.OPTIONS:
        #    if infos.get(op) is not None:
        #        print "Success"

        return result

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

if __name__ == '__main__':
    print('Energrid MQTT Imported')
