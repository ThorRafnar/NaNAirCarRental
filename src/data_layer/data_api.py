from data_layer.employee_data import EmployeeData
from data_layer.destination_data import DestinationData
from data_layer.customer_data import CustomerData
from data_layer.vehicle_data import VehicleData
from data_layer.vehicle_type_data import VehicleTypeData


class DataAPI():
    
    def __init__(self):
        self.employee_data = EmployeeData()
        self.destination_data = DestinationData()
        self.customer_data = CustomerData()
        self.vehicle_data = VehicleData()
        self.vehicle_type_data = VehicleTypeData()
        print("Data :^)")


# Employee functions
    def get_employees(self):
        ''' Retuns list of all employees as instance of Employee class form data layer '''
        return self.employee_data.get_employees()

    def register_employee(self, emp):
        ''' Returns a instance of Employee to write in database '''
        return self.employee_data.register_employee(emp)
        #test

    def change_employee_info(self, att_list):
        ''' returns a list with attributes for what to change about an employee in database '''
        return self.employee_data.change_employee_info(att_list)

# Customers
    def get_customers(self):
        ''' Calls get_customers in customer_layer that returns a list of customers as instances from Customers '''
        return self.customer_data.get_customers()

    def add_customer(self, cust):
        ''' returns an instance of Customer to database '''
        return self.customer_data.add_customer(cust)
    
    def change_customer_info(self, att_list):
        ''' returns a list with attributes of what to change about an employee down to data_layer  '''
        return self.customer_data.change_customer_info(att_list)

# Destination functions
    def get_destinations(self):
        ''' returns a list of all destinations as instances of Destinations class '''
        return self.destination_data.get_destinations()
    
    def create_destination(self, dest):
        ''' Returns a instance of Destinasion class down to data layer'''
        return self.destination_data.create_destination(dest)

# Vehicle functions
    def get_all_vehicles(self):
        ''' returns a list of all vehicles as instance of Vehicle class '''
        return self.vehicle_data.all_vehicles_to_list()
    
    def make_new_vehicle(self,vehicle_ins):
        ''' Returns a vehicle instance of Vehicle to datalayer '''
        self.vehicle_data.new_vehicle(vehicle_ins)
    
    def change_vehicle_condition(self, new_cond, ID):
        ''' Returns id of a vehicle and what condision it should have in database '''
        return self.vehicle_data.change_vehicle_condition(new_cond,ID)
    
# Vehicle type functions
    def get_all_vehicle_types(self):
        ''' returns a list of instances from VehicleType '''
        return self.vehicle_type_data.get_all_vehicle_types()
    
    def change_vehicle_rate(self, new_rate, vehicle_type):
        ''' returns new_rate and vehicle_type down to database '''
        return self.vehicle_type_data.change_vehicle_rate(new_rate, vehicle_type)
    
    def new_vehicle_type(self, info):
        ''' Returns an instance of Vehicle down to databse '''
        return self.vehicle_type_data.new_vehicle_type(info)
