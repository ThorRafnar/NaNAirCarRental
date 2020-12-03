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

    def get_employees(self):
        return self.employee_data.get_employees()

    def register_employee(self, emp):
        return self.employee_data.register_employee(emp)
        #test

    def change_employee_info(self, att_list):
        return self.employee_data.change_employee_info(att_list)

    def get_customers(self):
        return self.customer_data.get_customers()

    def add_customer(self, cust):
        return self.customer_data.add_customer(cust)
    
    def change_customer_info(self, att_list):
        return self.customer_data.change_customer_info(att_list)

    def get_destinations(self):
        return self.destination_data.get_destinations()
    
    def create_destination(self, dest):
        return self.destination_data.create_destination(dest)

    def get_all_vehicles(self):
        return self.vehicle_data.all_vehicles_to_list()
    
    def make_new_vehicle(self,info_list):
        return self.vehicle_data.new_vehicle(info_list)
    
    def change_vehicle_condition(self, new_cond, ID):
        return self.vehicle_data.change_vehicle_condition(new_cond,ID)
    
    def get_all_vehicle_types(self):
        return self.vehicle_type_data.get_all_vehicle_types()
    
    def change_vehicle_rate(self, new_rate, vehicle_type):
        return self.vehicle_type_data.change_vehicle_rate(new_rate, vehicle_type)
    
    def new_vehicle_type(self, info):
        return self.vehicle_type_data.new_vehicle_type(info)
