from data_layer.data_api import DataAPI
from logic_layer.employee_logic import EmployeeLogic
from logic_layer.vehicle_logic import VehicleLogic

class LogicAPI():

    def __init__(self):
        self.data_api = DataAPI()
        self.employee_logic = EmployeeLogic(self.data_api)
        self.vehicle_logic = VehicleLogic(self.data_api)
        print("Logic, b1tch!")

    def get_employees(self):
        return self.employee_logic.get_employees()

    def find_employee(self, emp):
        return self.employee_logic.find_employee(emp)
    
    def register_employee(self, emp):
        return self.employee_logic.register_employee(emp)

    def change_employee_info(self, attribute_list):
        return self.employee_logic.change_employee_info(attribute_list)

    def register_new_vehicle(self, new_vehicle):
        return self.vehicle_logic.register_new_vehicle(new_vehicle)

    
