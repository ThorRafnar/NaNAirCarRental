from data_layer.data_api import DataAPI
from logic_layer.employee_logic import EmployeeLogic
from logic_layer.vehicle_logic import VehicleLogic
from logic_layer.destination_logic import DestinationLogic
from logic_layer.customer_logic import CustomerLogic
from logic_layer.contract_logic import ContractLogic
from logic_layer.vehicle_type_logic import VehicleTypeLogic
from logic_layer.logic_error_check import LogicErrorCheck
from logic_layer.chuck_logic import ChuckLogic
from logic_layer.profit_logic import ProfitLogic

class LogicAPI():

    def __init__(self):
        self.data_api = DataAPI()
        self.employee_logic = EmployeeLogic(self.data_api)
        self.vehicle_logic = VehicleLogic(self.data_api)
        self.destination_logic = DestinationLogic(self.data_api)
        self.customer_logic = CustomerLogic(self.data_api)
        self.vehicle_type_logic = VehicleTypeLogic(self.data_api)
        self.contract_logic = ContractLogic(self.data_api,self.vehicle_logic,self.vehicle_type_logic)
        self.logic_error_check = LogicErrorCheck(self.data_api)
        self.chuck_logic = ChuckLogic(self.data_api)
        self.profit_logic = ProfitLogic(self.data_api)

    # Employee logic
    def get_employees(self):
        ''' Returns a list of all employees as instances of Employee class '''
        return self.employee_logic.get_employees()
    
    def get_filtered_employees(self, attribute_list):
        return self.employee_logic.get_filtered_employees(attribute_list)

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
        self.vehicle_logic.register_new_vehicle(new_vehicle)

    def find_vehicle(self, veh_id):
        return self.vehicle_logic.find_vehicle(veh_id)

    def change_vehicle_condition(self, vehicle_id, status):
        ''' Sends vehicle id and condition status to data layer '''
        return self.vehicle_logic.change_vehicle_condition(vehicle_id, status)

    def list_vehicles_by_status(self, status):
        return self.vehicle_logic.list_vehicles_by_status(status)
    
    def get_filtered_vehicle(self,start_date,end_date,location,vehicle_type):
        return self.vehicle_logic.get_filtered_vehicle(start_date,end_date,location,vehicle_type)

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
    
    def find_customer(self, ssn):
        return self.customer_logic.find_customer(ssn)

    def change_customer_info(self, attribute_list):
        ''' Sends a list containing ssn, attribute it wants to change and the changes for that attribute to data layer, ex. ['220687-2959', 'address', 'Bessastaðir'] '''
        return self.customer_logic.change_customer_info(attribute_list)

    def add_customer(self, cust):
        ''' Sends a instance of Customer class for new customer to data layer '''
        return self.customer_logic.add_customer(cust)
    
    # Contract logic
    def get_all_contracts(self):
        ''' Returns a list containing intstances of Contract classes for all contracts in database '''
        return self.contract_logic.get_all_contracts()

    def create_new_contract(self, cont):
        ''' Takes a instance of Contract for new contract and sends it down to data layer '''
        return self.contract_logic.create_new_contract(cont)

    def view_customer_contracts(self, ssn):
        ''' Gets ssn from UI and finds all contracts linked to that ssn in database and returns them as list of Contract classes '''
        return self.contract_logic.view_customer_contracts(ssn)
    
    def find_contract(self, contract_id):
        ''' Gets contract ID from UI and finds correct contract from given ID and returns the contract to UI if found, else returns None '''
        return self.contract_logic.find_contract(contract_id)
    
    def change_contract_status(self, contract_id, status):
        ''' Gets id of contract and changes to that contract status and send to data layer for changes to be made '''
        return self.contract_logic.change_contract_status(contract_id, status)
    
    def change_contract_dates(self,contract_id,start_date,end_date):
        return self.contract_logic.change_contract_dates(contract_id,start_date,end_date)
    
    def change_contract_vehicle(self,contract_id, veh_id):
        return self.contract.logic.change_contract_vehicle(contract_id, veh_id)
    
    def get_contracts_by_attr(self, attr_list):
        ''' Gets a list containing an attribute to filter by and the value to filter it from '''
        return self.contract_logic.get_contracts_by_attr(attr_list)
    
    # Vehcile Types Logic
    def get_vehicle_types(self):
        ''' Returns a list of all available vehicle types '''
        return self.vehicle_type_logic.get_vehicle_types()
    
    def create_new_type(self, vehicle_type):
        ''' Gets an instance of new vehicle type from UI and sends it down to data layer '''
        return self.vehicle_type_logic.create_new_type(vehicle_type)

    def change_types_rate(self, type_name, new_rate):
        ''' Gets from UI vehicle type and new rate and sends down to data layer '''
        return self.vehicle_type_logic.change_types_rate(type_name, new_rate)
    
    def get_types_rate(self, selected_type):
        return self.vehicle_type_logic.get_types_rate(selected_type)

    def filter_by_region(self, reg):
        ''' Gets for UI region to filter by and returns a list of vehicle types available in that given region '''
        return self.vehicle_type_logic.filter_by_region(reg)

    #Profits Logic
    def get_profits(self):
        return self.profit_logic.get_profits()

    def calculate_profits(self,start_date, end_date):
        return self.profit_logic.calculate_profits(start_date, end_date)

    # ERROR logic
    def check_work_area(self,a_str):
        return self.logic_error_check.check_work_area(a_str)

    def check_date(self, date_str):
        return self.logic_error_check.check_date(date_str)

    # Random Chuck Norris jokes logic
    def get_random_joke(self):
        ''' Returns one random Chuck Norris joke from chuck_jokes.txt '''
        return self.chuck_logic.get_random_joke()

    