#############################################
#               ENERGRID_SERVER             #
#############################################

import energrid_core as Core
#import energrid_db as DataBase
#import energrid_mqtt as Mqtt

from random import randrange
#import threading

OPTIONS = ['new', 'update', 'remove', 'status', 'database']

def start_server():
    test = True

    mqttClient = Mqtt.Client('sdfqigqlkvgqiugv')

    mqttClient.add_topic('publishing')

    mqttClient.publish('client/publishing','message')

    if test:
        test_clients = []
        
        clients = []

        n = Core.Neighborhood(1)
        
        for house in n.houses:
            #adding suppliers and consumers
            nb_houses = randrange(3)
            nb_suppliers = randrange(2)
            for j in range(nb_houses):
                house.add_consumer()
            for h in range(nb_suppliers):
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
                print("consumer: " + consumer.name)
                print(consumer)
                house.client.publish(str(consumer.name), str(consumer))
            for supplier in house.suppliers:
                print("supplier: " + supplier.name)
                print(supplier)
                house.client.publish(supplier.name, str(supplier))

        for house in n.houses:
            house.client.disconnect()

    mqttClient.disconnect()

if __name__ == "__main__":
    print('Energrid Server Imported')
    start_server()
