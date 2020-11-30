from logic_layer.logic_api import LogicAPI
from ui_layer.employee_ui import EmployeeUI

class UIAPI():
    def __init__(self):
        self.logic_api = LogicAPI()
        self.employee_ui = EmployeeUI(self.logic_api)
        print("UI!")

    def get_employees(self):
        self.employee_ui.get_employees()