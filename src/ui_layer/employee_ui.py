class EmployeeUI():

    def __init__(self, logic_api):
        self.logic_api = logic_api

    def get_employees(self):
        emps = self.logic_api.get_employees()
        for emp in emps:
            print(emp.name)