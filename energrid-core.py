## Energrid architecture to map all elements needed to the solution

import random


## Pseudo database to test operations and serialization
## all data retrieved from the electric grid is homogeneous
## it can be used for all requests
class Data:
    def __init__(self):
        self.last = 0
        self.values = 0
        self.db_timestamp = []
        self.db_values = []
        self.mean = 0
        self.max = 0
        self.min = 0
        self.state = False

    def mean_update(self,db):
        return sum(db)/len(db)

    def update(self, timestamp, value):
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
        return str(self.__dict__)

    def __str__(self):
        result = ''
        result += 'last: ' + str(self.last) + '\t'
        result += 'mean: ' + str(self.mean) + '\t'
        result += 'min: ' + str(self.min) + '\t'
        result += 'max: ' + str(self.max) + '\t'
        result += 'values: ' + str(self.values) + '\t'
       ## result += 'db_timestamp: ' + str(['{:.3f}'.format(x) for x in self.db_timestamp]) + '\n'
       ## result += 'db_values: ' + str(['{:.3f}'.format(x) for x in self.db_values]) + '\n'
        result += 'state: ' + str(self.state) + '\n'
        return result



## Electricity Supplier part of a House
## can be up to 9 per House
class Supplier:
    def __init__(self, identifier):
        self.id = identifier
        self.type = ''
        self.src_voltage = Data()
        self.src_current = Data()
        self.battery_voltage = Data()
        self.battery_current = Data()
        self.battery_remaining = Data()
        self.push_voltage = Data()
        self.push_current = Data()

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):    
        result = ''
        result += 'Supplier ' + str(self.id) + '\n'
        result += 'type: ' + self.type + '\n'
        result += 'src_voltage: ' + '\t\t' + str(self.src_voltage)
        result += 'src_current: ' + '\t\t' + str(self.src_current)
        result += 'battery_voltage: ' + '\t' + str(self.battery_voltage)
        result += 'battery_current: ' + '\t' + str(self.battery_current)
        result += 'battery_remaining: ' + '\t' + str(self.battery_remaining)
        result += 'push_voltage: ' + '\t\t' + str(self.push_voltage)
        result += 'push_current: ' + '\t\t' + str(self.push_current)
        return result


## Electricity Consumer part of a House
## can be up to 99 per House
class Consumer:
    def __init__(self, identifier):
        self.id = identifier
        self.type = ''
        self.pull = Data()

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        result = ''
        result += 'Consumer: ' + str(self.id) + '\n'
        result += 'type: ' + self.type + '\n'
        result += 'pull: ' + '\t\t' + str(self.pull)
        return result


##
class House:
    def __init__(self, identifier, suppliers_qntity, consumers_qntity):
        self.id = identifier
        self.last_supplier_id = 10 * identifier
        self.suppliers = []
        for i in range(suppliers_qntity):
            self.add_supplier()
        self.last_consumer_id = 100 * identifier
        self.consumers = []
        for i in range(consumers_qntity):
            self.add_consumer()

    def add_supplier(self):
        self.last_supplier_id += 1
        self.suppliers.append(Supplier(self.last_supplier_id))

    def add_consumer(self):
        self.last_consumer_id += 1
        self.consumers.append(Consumer(self.last_consumer_id))

    def consume(self):
        result = 0
        for i in self.consumers:
            result += i.pull.last
        return result

    def supply(self):
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


class Neighborhood:
    nb_id = 0
    def __init__(self, quantity_houses):
        self.id = Neighborhood.nb_id
        Neighborhood.nb_id += 1
        self.name = ""
        self.last_house_id = 0
        self.houses = []
        for i in range(quantity_houses):
            self.add_house()

    def global_consume(self):
        result = 0
        for i in self.houses:
            result += i.consume()
        return result

    def add_house(self):
        self.last_house_id += 1
        self.houses.append((House(self.last_house_id,1,1)))

    def update_simulation(self,steps):
        tmp = 1.
        for k in range(steps):
            for i in range(len(self.houses)):
                for m in range(len(self.houses[i].suppliers)):
                    self.houses[i].suppliers[m].src_voltage.update(tmp,25*random.random())
                    self.houses[i].suppliers[m].src_current.update(tmp,25*random.random())
                    self.houses[i].suppliers[m].battery_voltage.update(tmp,25*random.random())
                    self.houses[i].suppliers[m].battery_current.update(tmp,25*random.random())
                    self.houses[i].suppliers[m].battery_remaining.update(tmp,25*random.random())
                    self.houses[i].suppliers[m].push_voltage.update(tmp,25*random.random())
                    self.houses[i].suppliers[m].push_current.update(tmp,25*random.random())
                for j in range(len(self.houses[i].consumers)):
                    self.houses[i].consumers[j].pull.update(tmp,10*random.random())
            tmp += .2


    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return 'Neighborhood: ' + self.name + '\n' + str(self.__dict__)



'''
quartier = Neighborhood(0,3)

tmp = 1.
for k in range(50):
    for i in range(len(quartier.houses)):
        for m in range(len(quartier.houses[i].suppliers)):
            quartier.houses[i].suppliers[m].src_voltage.update(tmp,25*random.random())
            quartier.houses[i].suppliers[m].src_current.update(tmp,25*random.random())
            quartier.houses[i].suppliers[m].battery_voltage.update(tmp,25*random.random())
            quartier.houses[i].suppliers[m].battery_current.update(tmp,25*random.random())
            quartier.houses[i].suppliers[m].battery_remaining.update(tmp,25*random.random())
            quartier.houses[i].suppliers[m].push_voltage.update(tmp,25*random.random())
            quartier.houses[i].suppliers[m].push_current.update(tmp,25*random.random())
        for j in range(len(quartier.houses[i].consumers)):
            quartier.houses[i].consumers[j].pull.update(tmp,10*random.random())
    tmp += .2


print(quartier.houses[0].consume())
print(quartier.houses[0].supply()[6])
print(quartier.houses[1].consume())
print(quartier.houses[1].supply()[6])
print(quartier.houses[2].consume())
print(quartier.houses[2].supply()[6])
'''

if __name__ == '__main__':
    print('Energrid Imported')
