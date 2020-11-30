from data_layer.data_api import DataAPI
from logic_layer.employee_logic import EmployeeLogic

class LogicAPI():

    def __init__(self):
        self.data_api = DataAPI()
        self.employee_logic = EmployeeLogic(self.data_api)
        print("Logic, b1tch!")

    def get_employees(self):
        return self.employee_logic.get_employees()