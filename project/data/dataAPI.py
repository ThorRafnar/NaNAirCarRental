from project.data.employee_data import EmployeeData

class DataAPI():
    def __init__(self):
        print("Hello data layer! :~)")
        self.employee_data = EmployeeData()

    def get_employees(self):
        return self.employee_data.get_employees()