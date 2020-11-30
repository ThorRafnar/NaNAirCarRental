import csv
from project.models.employee import Employee

class EmployeeData():
    def __init__(self):
        pass

    def get_employees(self):
        ret_list = []
        with open("data/data_files/employee.csv", newline="", encoding="utf-8") as file_stream:
            reader = csv.DictReader(file_stream)
            for row in reader:
                emp = Employee(row["name"], row["address"], row["postal_code"], row["ssn"], row["home_phone"], row["mobile_phone"], row["email"], row["work_area"])
                ret_list.append(emp)
                
        return ret_list 