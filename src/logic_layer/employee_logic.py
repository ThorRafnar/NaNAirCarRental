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

    def check_employee(self, new_emp):
        '''  '''
        emp_list = self.get_employees()
        is_new = True
        for emp in emp_list:
            if emp.ssn == new_emp.ssn:
                is_new = False
                break
        print(is_new)
        return is_new

    def register_employee(self, emp):
        # þarf að fá register_employee frá data api
        self.data_api.register_employee(emp)
