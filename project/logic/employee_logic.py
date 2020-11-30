class EmployeeLogic():

    def __init__(self, data_api):
        print("I am employee logic :)")
        self.data_api = data_api

    def get_employees(self):
        return self.data_api.get_employees()

    def get_administrators(self):
        emps = self.get_employees()
        ret_list = []
        for emp in emps:
            if emp.work_area.lower().strip() == "admin":
                ret_list.append(emp)

        return ret_list