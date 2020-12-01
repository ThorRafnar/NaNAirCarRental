class EmployeeLogic():

    def __init__(self, data_api):
        print("I am employee logic :)")
        self.data_api = data_api

    def get_employees(self):
        return self.data_api.get_employees()

    def get_filtered(self, attribute_list):
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

    def find_employee(self, new_emp):
        ''' Takes Employee from UI and checks if he exist in database '''
        try:
            emp_list = self.get_employees()
            emp_inst = None
            for emp in emp_list:
                if emp.ssn == new_emp.ssn:
                    emp_inst = emp
                    break
            return emp_inst               
        except AttributeError:
            return None

    def register_employee(self, emp):
        ''' Sends Employee to data to write to database '''
        # þarf að fá register_employee frá data api
        self.data_api.register_employee(emp)

    def change_employee_info(self, attribute_list):
        self.data_api.change_employee_info(attribute_list)

    