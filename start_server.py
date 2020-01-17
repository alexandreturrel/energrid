#===================#
#   START SERVER    #
#===================#

# 1 january 2020
# code by Alexandre TURREL https://github.com/alexandreturrel
# for Polytech Sorbonne Engineering project lead by Francois PECHEUX


#imports
import energrid_core as e
import os
import sys

#userguide
def help():
    print('')
    print('')
    print('#=========================================#')
    print('|         Energrid Server Manager         |')
    print('#=========================================#')
    print('')
    print('Welcome! Here are useful commands to edit your Neighborhood:')
    print('')
    print('\tdebug(BOOLEAN)\t\t\t\ttoggle DEBUG mode')
    print('\thelp()\t\t\t\t\tshows this message')
    print('#=========================================#')
    print('\tnewHouse()\t\t\t\tcreates a new House')
    print('\tnewHouse(int VALUE)\t\t\tcreates VALUE new Houses')
    print('\tshowHouses()\t\t\t\tdisplay all Houses available')
    print('#=========================================#')
    print('\tnewConsumer(int HouseID, string Type)\t\tcreates a new Consumer for HouseID')
    print('\tnewConsumer(int HouseID, int X, string Type)\tcreates X new Consumers for HouseID')
    print('\tshowConsumers(int HouseID)\t\tshows all Consumers of HouseID')
    print('\tshowConsumers(int HouseID,int CsmID)\tshows ConsumerID of HouseID')
    print('\tsetConsumer(int HouseID, int CsmID, [0,1])\tset on or off a Consumer')
    print('#=========================================#')
    print('\tnewSupplier(int HouseID, string Type)\t\tcreates a new Supplier for HouseID')
    print('\tnewSupplier(int HouseID, int X, string Type)\tcreates X new Suppliers for HouseID')
    print('\tshowSuppliers(int HouseID)\t\tshows all Suppliers of HouseID')
    print('\tshowSuppliers(int HouseID,int SplID)\tshows SupplierID of HouseID')
    print('\tsetSupplier(int HouseID, int SplID, [0,1])\tset on or off a Supplier')
    print('#=========================================#')
    print('\tstart_demo()\t\t\t\tDemonstration purpose generative script (in french)')
    print('#=========================================#')
    print('')
    print('')

#start the server creating an empty neighborhood
n = e.Neighborhood(0)

help()

#==============================================
#   DEBUG
#==============================================

def debug(booleanValue):
    for house in n.houses:
        e.Client.debug = booleanValue

#==============================================
#   HOUSES
#==============================================

def newHouse(*args):
    if len(args) == 0:
        n.add_house()
    elif len(args) == 1:
        for i in range(args[0]):
            n.add_house()
    else:
        print('Error! Expecting:')
        print('newHouse() or newHouse([numberOfHousesToCreate])')

def showHouses():
    for house in n.houses:
        print('{}: {} Consumers | {} Suppliers'.format(house.name, len(house.consumers), len(house.suppliers)))


#==============================================
#   CONSUMERS
#==============================================

def newConsumer(*args):     #newConsumer(int HouseID, string CsmType) or newConsumer(int HouseID, int nbCsmToCreate, string CsmType)
    if len(args) == 2:
        n.houses[args[0]-1].add_consumer()
        n.houses[args[0]-1].consumers[-1].set_type(args[1])
    elif len(args) == 3:
        for i in range(args[1]):
            n.houses[args[0]-1].add_consumer()
            n.houses[args[0]-1].consumers[-1].set_type(args[2])
    else:
        print('Error! Expecting:')
        print('newConsumer(int HouseID, string CsmType) or newConsumer(int HouseID, int nbCsmToCreate, string CsmType)')

def showConsumers(*args):       #showConsumers(int HouseID, int CsmID) or showConsumers(int HouseID, int CsmID)
    if len(args) == 1:
        for consumer in n.houses[args[0]-1].consumers:
            print(str(consumer))
        print('House Consumption: {}'.format(n.houses[args[0]-1].consume()))
    elif len(args) == 2:
        print(n.houses[args[0]-1].consumers[args[1]-1])
    else:
        print('Error: Expecting:')
        print('showConsumers(int HouseID, int CsmID) or showConsumers(int HouseID, int CsmID)')

def setConsumer(*args):     #setConsumer(int HouseID, int CsmID, [0,1])
    if len(args) == 3:
        #result = "Neighborhood/0/House/"+ str(args[0]) + "/Consumer/" + str(args[1]) + "/set"
        n.houses[args[0]-1].client.publish(n.houses[args[0]-1].consumers[args[1]-1].name + '/set', args[2])
        #command = 'mosquitto_pub -h 127.0.0.1 -m ' + str(args[2]) + ' -t ' + result
        #os.system(command)
    else:
        print('Error: Expecting:')
        print('setConsumer(int HouseID, int CsmID, [0,1])')

#==============================================
#   SUPPLIERS
#==============================================

def newSupplier(*args):
    if len(args) == 2:
        n.houses[args[0]-1].add_supplier()
        n.houses[args[0]-1].suppliers[-1].set_type(args[1])
    elif len(args) == 3:
        for i in range(args[1]):
            n.houses[args[0]-1].add_supplier()
            n.houses[args[0]-1].suppliers[-1].set_type(args[2])
    else:
        print('Error! Expecting:')
        print('newSupplier(HouseID, string SplType) or newSupplier(HouseID, [nbOfSplToCreate], string SplType)')

def showSuppliers(*args):
    if len(args) == 1:
        for supplier in n.houses[args[0]-1].suppliers:
            print(supplier)
    elif len(args) == 2:
        print(n.houses[args[0]-1].suppliers[args[1]-1])

def setSupplier(*args):
    if len(args) == 3:
        result = "Neighborhood/0/House/"+ str(args[0]) + "/Supplier/" + str(args[1]) + "/booleanLoad"
        command = 'mosquitto_pub -h 127.0.0.1 -m ' + str(args[2]) + ' -t ' + result
        os.system(command)
    else:
        print('Error: Expecting:')
        print('setConsumer(int HouseID, int CsmID, [0,1])')

#==============================================
#   DEMO
#==============================================

def startDemo():
    newHouse(2)
    print('Creation des deux maisons pour la demonstration')
    for i in [1,2]:
        newConsumer(i,'Radiateur')
        print('Creation d\'un radiateur dans la Maison {}'.format(i))
        newConsumer(i,'Frigo')
        print('Creation d\'un frigo dans la Maison {}'.format(i))
        newConsumer(i,'Lampe')
        print('Creation d\'une lampe dans la Maison {}'.format(i))
        newSupplier(i,'Solar Panel')
        print('Creation d\'un panneau solaire dans la Maison {}'.format(i))
    newConsumer(2,'Relais')

