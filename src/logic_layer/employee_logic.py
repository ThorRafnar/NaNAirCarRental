class EmployeeLogic():

    def __init__(self, data_api):
        print("I am employee logic :)")
        self.data_api = data_api

    def get_employees(self):
        ''' Returns a list of employees as instances of Employee class from data layer '''
        return self.data_api.get_employees()

    def get_filtered(self, attribute_list):
        ''' Finds employees form given attributes and returns a list of those employees as instances of Employee class '''
        emps = self.get_employees()
        ret_list = []
        for emp in emps:
            target = len(attribute_list)
            counter = 0
            for attribute in attribute_list:
                col = attribute[0]
                att = attribute[1]
                if getattr(emp, col).lower() == att.lower():
                    counter += 1
            if target == counter:
                ret_list.append(emp)

        return ret_list

    def find_employee(self, new_ssn):
        ''' Takes an instance of Employee class for employee from UI and checks if he exist in database, returns an instance of that Employee back if found, else returns None '''
        emp_list = self.get_employees()
        emp_inst = None
        for emp in emp_list:
            if emp.ssn == new_ssn:
                emp_inst = emp
                break
        #print(emp_inst)
        return emp_inst  

    def register_employee(self, emp):
        ''' Sends an instance of Employee class for new employee to data layer to write to database '''
        self.data_api.register_employee(emp)

    def change_employee_info(self, attribute_list):
        ''' Sends a list of attributes to data layer to change given attribute for given employee '''
        self.data_api.change_employee_info(attribute_list)

    