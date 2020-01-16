import energrid_core as e
import os
import sys

def help():
    print('Welcome to the Energrid Server Manager')
    print('Here are useful commands to edit your Neighborhood:')

    print('\tdebug(BOOLEAN)\t\t\t\ttoggle DEBUG mode')
    print('\thelp()\t\t\t\t\tshows this message')
    print('\tnewHouse()\t\t\t\tcreates a new House')
    print('\tnewHouse(int VALUE)\t\t\tcreates VALUE new Houses')
    print('\tnewConsumer(int HouseID, string Type)\t\tcreates a new Consumer for HouseID')
    print('\tnewConsumer(int HouseID, int X, string Type)\tcreates X new Consumers for HouseID')
    print('\tnewSupplier(int HouseID, string Type)\t\tcreates a new Supplier for HouseID')
    print('\tnewSupplier(int HouseID, int X, string Type)\tcreates X new Suppliers for HouseID')
    print('\tshowHouses()\t\t\t\tdisplay all Houses available')
    print('\tshowConsumers(int HouseID)\t\tshows all Consumers of HouseID')
    print('\tshowConsumers(int HouseID,int CsmID)\tshows ConsumerID of HouseID')
    print('\tshowSuppliers(int HouseID)\t\tshows all Suppliers of HouseID')
    print('\tshowSuppliers(int HouseID,int SplID)\tshows SupplierID of HouseID')
    print('\tstart_demo()\t\t\t\tDemonstration purpose generative script (in french)')

n = e.Neighborhood(0)

def debug(booleanValue):
    for house in n.houses:
        e.Client.debug = booleanValue

#==============================================

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

#==============================================

def newConsumer(*args):
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

def showConsumers(*args):
    if len(args) == 1:
        for consumer in n.houses[args[0]-1].consumers:
            print(str(consumer))
        print('House Consumption: {}'.format(n.houses[args[0]-1].consume()))
    elif len(args) == 2:
        print(n.houses[args[0]-1].consumers[args[1]-1])


#==============================================

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


#==============================================

#==============================================

def start_demo():
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
