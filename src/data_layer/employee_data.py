from model_layer.employee import Employee
import csv
import os

class EmployeeData():

    def get_employees(self):
        ret_list = []
        with open("data_layer/data_files/employee.csv", encoding="utf-8") as file_stream:
            reader = csv.DictReader(file_stream)
            for row in reader:
                emp = Employee(row["name"], row["address"], row["postal_code"], row["ssn"], row["home_phone"], row["mobile_phone"], row["email"], row["work_area"])
                ret_list.append(emp)
        return ret_list 


    def register_employee(self,emp):
        ''' Writes new employee to database'''
        a_list = [emp.name,emp.address,emp.postal_code,emp.ssn,emp.home_phone,emp.mobile_phone,emp.email,emp.work_area]
        with open("data_layer/data_files/employee.csv", 'a+',encoding="utf8",newline='') as file_stream:
            csvwriter = csv.writer(file_stream)
            csvwriter.writerow(a_list)
        #test
        

            
        
