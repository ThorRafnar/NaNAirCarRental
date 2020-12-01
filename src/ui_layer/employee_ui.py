from model_layer.employee import Employee


class EmployeeUI():

    def __init__(self, logic_api):
        self.logic_api = logic_api


    def get_employees(self):
        emps = self.logic_api.get_employees()
        for emp in emps:
            print(emp.name)

    def check_name(self, name):
        """
        Takes user input for a name, checks that all characters are either alphabetical or spaces,
        if input has invalid characters, returns none
        """
        for char in name:
            if char.isalpha() == False and char != " ":
                name = None
                continue       
        return name

    def get_name(self):
        a_str = input("Enter name: ")
        name = self.check_name(a_str)

    def create_employee(self):
        name = self.get_name()
        address = input("Enter Address: ")
        postal_code = input("Enter postal code: ")
        ssn = input("Enter social security number: ")
        home_phone = input("Enter home phone: ")
        mobile_phone = input("Enter mobile phone: ")
        email = input("Enter email: ")
        work_area = input("Enter work area: ")
        new_employee = Employee(name, address, postal_code, ssn, home_phone, mobile_phone, email, work_area)
        print(new_employee)