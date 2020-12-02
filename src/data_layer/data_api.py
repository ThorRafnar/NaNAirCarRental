from data_layer.employee_data import EmployeeData


class DataAPI():
    
    def __init__(self):
        self.employee_data = EmployeeData()
        print("Data :^)")

    def get_employees(self):
        return self.employee_data.get_employees()

    def register_employee(self, emp):
        return self.employee_data.register_employee(emp)
        #test

    def change_employee_info(self, att_list):
        return self.employee_data.change_employee_info(att_list)