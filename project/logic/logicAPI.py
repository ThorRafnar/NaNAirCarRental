from project.data.dataAPI import DataAPI
from project.logic.employee_logic import EmployeeLogic

class LogicAPI():
    def __init__(self):
        print("Hello logic layer!")
        self.data_api = DataAPI()
        self.employee_logic = EmployeeLogic(self.data_api)

    def get_employees(self):
        return self.employee_logic.get_employees()

    def get_administrators(self):
        return self.employee_logic.get_administrators()

    def create_new_employee(self, emp):
        self.employee_logic.create_new(emp)
