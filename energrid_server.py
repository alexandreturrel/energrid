#############################################
#               ENERGRID_SERVER             #
#############################################

import energrid_core as Core
import energrid_db as DataBase
import energrid_mqtt as Mqtt

from random import randrange
import threading

def start_server():
    test = True

    mqttClient = Mqtt.Client('client')

    mqttClient.add_topic('publishing')

    mqttClient.publish('client/publishing','message')

    if test:
        test_clients = []
        
        clients = []

        n = Core.Neighborhood(5)
        
        for house in n.houses:
            #adding suppliers and consumers
            tmp = randrange(5)
            tmp2 = randrange(3)
            for j in range(tmp):
                house.add_consumer()
            for h in range(tmp2):
                house.add_supplier()

#        #multiple connections
#        for i in range(len(test_clients)):
#            client = Mqtt.Client(test_clients[i])
#            client.add_topic('#')
#            clients.append(client)

        print('')
        print('##################')
        print('##################')
        print('')
        print('Connections done !')
        print('')
        print('##################')
        print('##################')
        print('')

        for house in n.houses:
            for consumer in house.consumers:
                print(consumer.mqtt)
                consumer.mqtt.client.publish(consumer.name + '/test',str(consumer))
            for supplier in house.suppliers:
                supplier.mqtt.client.publish(supplier.name + '/test', str(supplier))

        for house in n.houses:
            for consumer in house.consumers:
                consumer.mqtt.disconnect()
            for supplier in house.suppliers:
                supplier.mqtt.disconnect()

    mqttClient.disconnect()

if __name__ == "__main__":
    print('Energrid Server Imported')
    start_server()
