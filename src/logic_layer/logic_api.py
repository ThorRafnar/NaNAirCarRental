from data_layer.data_api import DataAPI
from logic_layer.employee_logic import EmployeeLogic
from logic_layer.vehicle_logic import VehicleLogic
from logic_layer.destination_logic import DestinationLogic
from logic_layer.customer_logic import CustomerLogic

class LogicAPI():

    def __init__(self):
        self.data_api = DataAPI()
        self.employee_logic = EmployeeLogic(self.data_api)
        self.vehicle_logic = VehicleLogic(self.data_api)
        self.destination_logic = DestinationLogic(self.data_api)
        self.customer_logic = CustomerLogic(self.data_api)

    # Employee logic
    def get_employees(self):
        ''' Returns a list of all employees as instances of Employee class '''
        return self.employee_logic.get_employees()

    def find_employee(self, new_ssn):
        ''' Looks for one employee in employee.csv from ssn, returns a Employee instance if found, else returns None '''
        return self.employee_logic.find_employee(new_ssn)
    
    def register_employee(self, emp):
        ''' Sends a instance of Employee class for new employee to data layer '''
        return self.employee_logic.register_employee(emp)

    def change_employee_info(self, emp):
        ''' Sends a list containing ssn, attribute it wants to change and the changes for that attribute to data layer '''
        return self.employee_logic.change_employee_info(emp)

    # Vehicle logic
    def all_vehicles_to_list(self):
        ''' Sends a list of vehicles as instances of Vehicle class to UI '''
        return self.vehicle_logic.all_vehicles_to_list()

    def register_new_vehicle(self, new_vehicle):
        ''' Sends a instance of Vehicle class for new vehicle to data layer '''
        return self.vehicle_logic.register_new_vehicle(new_vehicle)

    def change_vehicle_condition(self, vehicle_id, status):
        ''' Sends vehicle id and condition status to data layer '''
        return self.vehicle_logic.change_vehicle_condition(vehicle_id, status)

    def list_vehicles_by_status(self, status):
        return self.vehicle_logic.list_vehicles_by_status(status)

    # Destination logic
    def get_destinations(self):
        return self.destination_logic.get_destinations()
    
    def find_destination(self, iata):
        return self.destination_logic.find_destination(iata)

    def create_destination(self, destination):
        ''' Gets an instance of Destination class from UI and sends it to data layer '''
        return self.destination_logic.create_destination(destination)
    
    def destinations_option_list(self):
        return self.destination_logic.destinations_option_list()

    # Customer Logic
    def get_customer(self):
        ''' Returns a list of all customer as instances of Customer class '''
        return self.customer_logic.get_customers()

    def change_customer_info(self, attribute_list):
        ''' Sends a list containing ssn, attribute it wants to change and the changes for that attribute to data layer, ex. ['220687-2959', 'address', 'Bessastaðir'] '''
        return self.customer_logic.change_customer_info(attribute_list)

    def add_customer(self, cust):
        ''' Sends a instance of Customer class for new customer to data layer '''
        return self.customer_logic.add_customer(cust)