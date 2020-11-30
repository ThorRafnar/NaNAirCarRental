"""
from project.data.dataAPI import DataAPI
from project.logic.logicAPI import LogicAPI
from project.models.employee import Employee
class EmployeeUI:
    def __init__(self):
        self.logic_api = LogicAPI
        
    def create_new_employee(self):
        name = input("Enter full name: ")
        address = input("Enter address: ")
        postal_code = input("Enter postal code: ")
        ssn = input("Enter social security number: ")
        home_phone = input("Enter Home Phone number: ")
        mobile_phone = input("Enter mobile phone number: ")
        e_mail = input("Enter E-mail: ")
        work_area = input("Enter Work Area: ")
        emp = Employee(name,address,postal_code,ssn,home_phone,mobile_phone,e_mail,work_area)
        self.logic_api.create_new_employee(emp)
        """