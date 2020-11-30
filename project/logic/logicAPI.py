from project.data.dataAPI import DataAPI
from project.logic.employee_logic import EmployeeLogic

class LogicAPI():
    def __init__(self):
        print("Hello logic layer!")
        self.data_api = DataAPI()
        self.employee_logic = EmployeeLogic(self.data_api)

    def get_employees(self):
        return self.employee_logic.get_employees()

<<<<<<< HEAD
    def get_administrators(self):
        return self.employee_logic.get_administrators()

    def create_new_employee(self, emp):
        self.employee_logic.create_new(emp)
=======
    def get_filtered_employees(self, attribute_list):
        return self.employee_logic.get_filtered(attribute_list)
>>>>>>> efe91c53425670bc46a9fba2179c86439ef175bc
