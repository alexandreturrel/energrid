#############################################
#               ENERGRID_CORE               #
#############################################


## Energrid architecture to map all elements needed to the solution

import energrid_mqtt as Mqtt

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



## Electricity Supplier part of a House
class Supplier:
    def __init__(self, identifier, house_name):
        self.id = identifier
        self.name = house_name + '/Supplier/' + str(self.id)
        self.type = ''
        self.src_voltage = Data()
        self.src_current = Data()
        self.battery_voltage = Data()
        self.battery_current = Data()
        self.battery_remaining = Data()
        self.push_voltage = Data()
        self.push_current = Data()
    
    def set_type(self, new_type):
        self.type = str(new_type)

    def __repr__(self):
        result = {}
        result['id'] = self.id
        result['name'] = self.name
        result['type'] = self.type
        result['src_voltage'] = self.src_voltage
        result['src_current'] = self.src_current
        result['battery_voltage'] = self.battery_voltage
        result['battery_current'] = self.battery_current
        result['battery_remaining'] = self.battery_remaining
        result['push_voltage'] = self.push_voltage
        result['push_current'] = self.push_current
        return str(result)


## Electricity Consumer part of a House
class Consumer:
    def __init__(self, identifier, house_name):
        self.id = identifier
        self.name = house_name + '/Consumer/' + str(self.id)
        self.type = ''
        self.pull = Data()

    def set_type(self, new_type):
        self.type = str(new_type)

    def __repr__(self):
        result = {}
        result['id'] = self.id
        result['name'] = self.name
        result['type'] = self.type
        result['pull'] = self.pull
        return str(result)


##
class House:
    def __init__(self, identifier, neighborhood_name, suppliers_qntity, consumers_qntity):
        ##core
        self.id = identifier
        self.name = neighborhood_name + '/House/' + str(self.id)
        self.client = Mqtt.Client(self.name)

        #callbacks
        self.on_message = self.client.on_message

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
        self.last_consumer_id += 1
        self.consumers.append(Consumer(self.last_consumer_id,self.name))
        self.client.add_topic(self.consumers[-1].name)

    def rm_consumer(self,old_consumer):
        if old_consumer in self.consumers:
            self.consumers.pop(old_consumer)

    def add_supplier(self):
        self.last_supplier_id += 1
        self.suppliers.append(Supplier(self.last_supplier_id,self.name))
        self.client.add_topic(self.suppliers[-1].name)

    def rm_supplier(self,old_supplier):
        if old_supplier in self.suppliers:
            self.suppliers.pop(old_supplier)

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
        self.name = 'Neighborhood/' + str(self.id)
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
        self.houses.append((House(self.last_house_id,self.name,1,1)))

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return 'Neighborhood: ' + self.name + '\n' + str(self.__dict__)



if __name__ == '__main__':
    print('Energrid Core Imported')
