from data_layer.data_api import DataAPI
from logic_layer.employee_logic import EmployeeLogic
from logic_layer.vehicle_logic import VehicleLogic

class LogicAPI():

    def __init__(self):
        self.data_api = DataAPI()
        self.employee_logic = EmployeeLogic(self.data_api)
        self.vehicle_logic = VehicleLogic(self.data_api)

    def get_employees(self):
        ''' Returns a list of all employees as instances of Employee class '''
        return self.employee_logic.get_employees()

    def find_employee(self, new_ssn):
        ''' Looks for one employee in employee.csv from ssn, returns a Employee instance if found, else returns None '''
        return self.employee_logic.find_employee(new_ssn)
    
    def register_employee(self, emp):
        ''' Sends a instance of Employee class for new employee to data layer '''
        return self.employee_logic.register_employee(emp)

    def change_employee_info(self, attribute_list):
        ''' Sends a list containing ssn, attribute it wants to change and the changes for that attribute to data layer, ex. ['220687-2959', 'address', 'Bessastaðir'] '''
        return self.employee_logic.change_employee_info(attribute_list)

    def register_new_vehicle(self, new_vehicle):
        ''' Sends a instance of Vehicle class for new vehicle to data layer '''
        return self.vehicle_logic.register_new_vehicle(new_vehicle)

    
