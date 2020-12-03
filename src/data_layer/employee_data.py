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
    def change_employee_info(self,atttribute_list):

        ''' Takes in a list with attributes, the attributes are values for what to change  '''
        values = atttribute_list[1].split(",")
        file_list = []
        with open("test.csv",'r' ,encoding="utf-8") as read_file:
            reader = csv.DictReader(read_file)
            emp_ssn = atttribute_list[0]
            for row in reader:
                if row["ssn"] == emp_ssn:
                    for key, value in zip(row, values):
                        row[key] = value
                file_list.append(row)

        with open("test.csv", "w", encoding='utf-8', newline='') as write_file:
            keys = file_list[0].keys()
            the_writer = csv.DictWriter(write_file,keys)
            the_writer.writeheader()
            the_writer.writerows(file_list)

            
        
