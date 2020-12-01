from model_layer.employee import Employee
import csv
import os

class EmployeeData():

    def get_employees(self):
        ret_list = []
        print(os.getcwd())
        with open("data_layer/data_files/employee.csv", encoding="utf-8") as file_stream:
            reader = csv.DictReader(file_stream)
            for row in reader:
                emp = Employee(row["name"], row["address"], row["postal_code"], row["ssn"], row["home_phone"], row["mobile_phone"], row["email"], row["work_area"])
                ret_list.append(emp)
                
        return ret_list 