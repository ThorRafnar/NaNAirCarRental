from project.data.dataAPI import DataAPI
from project.logic.employee_logic import EmployeeLogic

class LogicAPI():
    def __init__(self):
        print("Hello logic layer!")
        self.data_api = DataAPI()
        self.employee_logic = EmployeeLogic(self.data_api)