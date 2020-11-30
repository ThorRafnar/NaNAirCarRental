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
<<<<<<< HEAD

    def create_new(self, emp):
        self.data_api.create_new_employee(emp)
=======
>>>>>>> efe91c53425670bc46a9fba2179c86439ef175bc
