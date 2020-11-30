from project.logic.logicAPI import LogicAPI
from project.ui.employeeUI import EmployeeUI

class UI_Main():
    def __init__(self):
        self.logicAPI = LogicAPI()
        self.employee_UI = EmployeeUI

    def start(self):
        print("Hi there UI")

    def get_employees(self):
        employees = self.logicAPI.get_employees()
        for employee in employees:
            print(employee.name)
        
<<<<<<< HEAD
    def get_administrators(self):
        administrators = self.logicAPI.get_administrators()
        for admin in administrators:
            print(admin.name)
    
    def new_employee(self):
        self.employee_UI.create_new_employee(self)
=======
    def get_filtered_employees(self, attribute_list):
        employees = self.logicAPI.get_filtered_employees(attribute_list)
        for emp in employees:
            print(emp.name)
>>>>>>> efe91c53425670bc46a9fba2179c86439ef175bc

    