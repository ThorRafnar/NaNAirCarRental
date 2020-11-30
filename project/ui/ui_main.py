from project.logic.logicAPI import LogicAPI

class UI_Main():
    def __init__(self):
        self.logicAPI = LogicAPI()
        

    def start(self):
        print("Hi there UI")

    def get_employees(self):
        employees = self.logicAPI.get_employees()
        for employee in employees:
            print(employee.name)
        
    def get_filtered_employees(self, attribute_list):
        employees = self.logicAPI.get_filtered_employees(attribute_list)
        for emp in employees:
            print(emp.name)

    