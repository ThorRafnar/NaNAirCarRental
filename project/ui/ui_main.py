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
        
    def get_administrators(self):
        administrators = self.logicAPI.get_administrators()
        for admin in administrators:
            print(admin.name)

    