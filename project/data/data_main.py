import csv
import os
from project.models.employee import Employee

class DataMain():
    def __init__(self):
        pass

    def get_employees(self):
        ret_list = []
        print(os.getcwd())
        with open("data/data_files/employee.csv", encoding="utf8") as file_stream:
            reader = csv.DictReader(file_stream)
            for row in reader:
                emp = Employee(row["name"], row["address"], row["postal_code"], row["ssn"], row["home_phone"], row["mobile_phone"], row["email"], row["work_area"])
                ret_list.append(emp)
                
        return ret_list 