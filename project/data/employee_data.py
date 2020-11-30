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
    
    def create_new(self,emp):
        with open("data/data_files/employee.csv", newline="", encoding="utf-8") as file_stream:
            
            attributes = ["name", "address", "postal_code", "ssn", "home_phone", "mobile_phone", "email", "work_area"]
            a_list = []
            for attribute in attributes:
                a_list.append(getattr(emp, attribute))
            a_str = ",".join(a_list)
            print(a_str)
            
    
