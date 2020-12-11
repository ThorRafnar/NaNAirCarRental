from data_layer.data_api import DataAPI
from logic_layer.employee_logic import EmployeeLogic
from logic_layer.customer_logic import CustomerLogic
from logic_layer.vehicle_logic import VehicleLogic
from logic_layer.destination_logic import DestinationLogic
from logic_layer.contract_logic import ContractLogic
from logic_layer.vehicle_type_logic import VehicleTypeLogic
from logic_layer.logic_error_check import LogicErrorCheck
from logic_layer.chuck_logic import ChuckLogic
from logic_layer.profit_logic import ProfitLogic
from logic_layer.utilization_logic import UtilizationLogic

class LogicAPI():

    def __init__(self):
        self.data_api = DataAPI()
        self.employee_logic = EmployeeLogic(self.data_api)
        self.customer_logic = CustomerLogic(self.data_api)
        self.vehicle_logic = VehicleLogic(self.data_api,self.customer_logic)
        self.destination_logic = DestinationLogic(self.data_api)
        self.vehicle_type_logic = VehicleTypeLogic(self.data_api, self.vehicle_logic)
        self.contract_logic = ContractLogic(self.data_api,self.vehicle_logic,self.vehicle_type_logic, self.destination_logic,self.customer_logic)
        self.logic_error_check = LogicErrorCheck(self.data_api)
        self.chuck_logic = ChuckLogic(self.data_api)
        self.profit_logic = ProfitLogic(self.data_api, self.destination_logic, self.vehicle_type_logic)
        self.utilization_logic = UtilizationLogic(self.data_api)

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
        ''' Sends an instance of a changed employee to data layer, and replaces it '''
        return self.employee_logic.change_employee_info(emp)

    # Vehicle logic
    def all_vehicles_to_list(self):
        ''' Sends a list of vehicles as instances of Vehicle class to UI '''
        return self.vehicle_logic.all_vehicles_to_list()

    def register_new_vehicle(self, new_vehicle):
        ''' Sends a instance of Vehicle class for new vehicle to data layer '''
        self.vehicle_logic.register_new_vehicle(new_vehicle)

    def find_vehicle(self, veh_id):
        ''' Gets vehicle id from UI, looks for vehicle in database and returns an instance of Vehicle class if found, else returns None back to UI '''
        return self.vehicle_logic.find_vehicle(veh_id)

    def change_vehicle_condition(self, vehicle_id, status):
        ''' Sends vehicle id and condition status to data layer '''
        return self.vehicle_logic.change_vehicle_condition(vehicle_id, status)

    def availble_vehicles_by_location(self, location):
        '''returns all availble vehicles by location as instanses '''
        return self.vehicle_logic.availble_vehicles_by_location(location)
    
    def get_filtered_vehicle(self,start_date,end_date,location,vehicle_type):
        ''' Filters vehicles to find if vehicle is available for rent '''
        return self.vehicle_logic.get_filtered_vehicle(start_date,end_date,location,vehicle_type)
    
    def match_licenses(self, customer_ssn, vehicle_id):
        ''' checks if customer licenses is valid for givin vehicle '''
        return self.vehicle_logic.match_licenses(customer_ssn,vehicle_id)
    
    def licenses_options_list(self):
        ''' returns a list with all licence types '''
        return self.vehicle_logic.licenses_options_list()

    def get_vehicle_by_location(self, location):
        '''returns a list with instances of all vehicles in set location'''
        return self.vehicle_logic.get_vehicle_by_location(location)

    # Destination logic
    def get_destinations(self):
        ''' Sends a list of destinations as instances of Destination class to UI '''
        return self.destination_logic.get_destinations()
    
    def find_destination(self, iata):
        ''' Gets iata code from UI and checks if destination exists in database, returns an instance of Destination class for give destination if found, else returns None ''' 
        return self.destination_logic.find_destination(iata)

    def create_destination(self, destination):
        ''' Gets an instance of Destination class from UI and sends it to data layer '''
        return self.destination_logic.create_destination(destination)
    
    def destinations_option_list(self):
        ''' Returns destinations attributes for use in UI start screen '''
        return self.destination_logic.destinations_option_list()

    def city_to_iata(self, city):
        ''' retunrs iata code for given city '''
        return self.destination_logic.city_to_iata(city)

    # Customer Logic
    def get_customer(self):
        ''' Returns a list of all customer as instances of Customer class '''
        return self.customer_logic.get_customers()
    
    def find_customer(self, ssn):
        ''' returns a certain customer  '''
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

    def get_pending_contracts(self, ssn, location):
        ''' Returns pending contracts by customer ssn and location '''
        return self.contract_logic.get_pending_contracts(ssn, location)
    
    def find_contract(self, contract_id):
        ''' Gets contract ID from UI and finds correct contract from given ID and returns the contract to UI if found, else returns None '''
        return self.contract_logic.find_contract(contract_id)
    
    def change_contract_status(self, contract_id, status):
        ''' Gets id of contract and changes to that contract status and send to data layer for changes to be made '''
        return self.contract_logic.change_contract_status(contract_id, status)
    
    def get_unpaid_contracts(self, ssn, start_date, end_date):
        ''' returns unpaid contracts for certain customer for given time '''
        return self.contract_logic.get_unpaid_contracts( ssn, start_date, end_date)

    def change_contract(self, cust):
        ''' returns a contract instanse down to db and overwrites the old one '''
        self.contract_logic.change_contract(cust)
    
    def get_paid_and_unpaid_contracts(self, start_date, end_date):
        ''' returns all paid and unpaid contracts for given time '''
        return self.contract_logic.get_paid_and_unpaid_contracts(start_date, end_date)

    def get_active_contract(self, vehicle_id, location_iata):
        ''' Returns active contract for a given vehicle id in a location, returning none if none exists '''
        return self.contract_logic.get_active_contract(vehicle_id, location_iata)
    
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
        ''' Searches for a vehicle type and returns it rate '''
        return self.vehicle_type_logic.get_types_rate(selected_type)

    def filter_by_region(self, reg, start_date, end_date):
        ''' Gets for UI region to filter by and returns a list of vehicle types available in that given region '''
        return self.vehicle_type_logic.filter_by_region(reg, start_date, end_date)

    #Profits Logic
    def calculate_profits(self,start_date, end_date):
        ''' returns a total profits for given time as int. this function also calls calculate_profits_by_location
        and  calculate_profits_by_location and returns it as well in a list'''
        return self.profit_logic.calculate_profits(start_date, end_date)

    # Utilization logic
    def get_utilization_for_location(self, location):
        ''' returns a list of all utilization instances for given location'''
        return self.utilization_logic.get_utilization_for_location(location)

    # ERROR logic
    def check_attribute(self, attr_val, attr_key):
        return self.logic_error_check.decide_what_error(attr_val, attr_key)

    def check_work_area(self,a_str):
        return self.logic_error_check.check_work_area(a_str)

    def check_date(self, date_str):
        return self.logic_error_check.check_date(date_str)

    def check_ssn(self, ssn):
        return self.logic_error_check.ssn_formatter(ssn)

    def check_phone(self, phone):
        return self.logic_error_check.check_phone(phone)

    def check_hours(self, hours):
        return self.logic_error_check.check_hours(hours)
    
    def check_if_only_number(self, number_str):
        ''' checs  if a_string is a number'''
        return self.logic_error_check.check_if_number(number_str)

    # Random Chuck Norris jokes logic
    def get_random_joke(self):
        ''' Returns one random Chuck Norris joke from chuck_jokes.txt '''
        return self.chuck_logic.get_random_joke()

    