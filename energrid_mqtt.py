#############################################
#               ENERGRID_MQTT               #
#############################################

import paho.mqtt.client as mqtt
import time
import threading


class Client:

    debug = True

    def __init__(self,name):
        self.name = name
        self.client = mqtt.Client(name)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.client.connected_flag = False
        if Client.debug:
            print(self.name + '\t' +'connection...')
        self.client.connect('127.0.0.1', port=1883, keepalive=60, bind_address="")
        self.client.loop_start()
        self.topics=[]
        self.historic=[]
        while not self.client.connected_flag:
            time.sleep(.1)
        self.add_topic('')

    def add_topic(self, new_topic):
        if new_topic == '':
            tmp = self.name
        else:
            tmp = self.name + '/' + new_topic
        if Client.debug:
            print(self.name + '\t' + 'new topic added: ' + tmp + ' and subscription done')
        self.topics.append(tmp)
        self.client.subscribe(tmp, qos=2)
        self.client.message_callback_add(tmp, self.client.on_message)

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
        result = message.topic + '\t' + str(message.payload.decode("utf-8"))
        self.historic.append(result)
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
