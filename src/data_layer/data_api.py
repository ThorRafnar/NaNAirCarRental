from data_layer.employee_data import EmployeeData


class DataAPI():
    
    def __init__(self):
        self.employee_data = EmployeeData()
        print("Data :^)")

    def get_employees(self):
        return self.employee_data.get_employees()