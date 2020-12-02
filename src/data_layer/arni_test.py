import csv
import os
#Jón Jónsson,Melagerð 99,200,300279-1289,+356 5815432,+354 6890012,jj@nan.is,KEF
att = ["300279-1289","work_area","KUS"]


class Employee():

    def __init__(self, name, address, postal_code, social_security_number, home_phone, mobile_phone, email, work_area):
        self.name = name
        self.address = address
        self.postal_code = postal_code
        self.ssn = social_security_number
        self.home_phone = home_phone
        self.mobile_phone = mobile_phone
        self.email = email
        self.work_area = work_area


def get_employees():
        ret_list = []
        with open("testcsv.csv", encoding="utf-8") as file_stream:
            reader = csv.DictReader(file_stream)
            for row in reader:
                emp = Employee(row["name"], row["address"], row["postal_code"], row["ssn"], row["home_phone"], row["mobile_phone"], row["email"], row["work_area"])
                ret_list.append(emp)
            for el in ret_list:
                print(el.ssn)
        
        return ret_list 

get_employees()
        


        
           

            
           
        
