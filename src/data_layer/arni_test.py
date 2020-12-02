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
        


        
           

            
           
        
=======



class Destination():
    def __init__(self, country, airport, phone, hours, iata):
        self.country = country
        self.airport = airport
        self.phone = phone
        self.hours = hours
        self.iata = iata




def get_destinations():

    ''' Returns all destinations in a list'''
    dest_list = []
    with open("testcsv.csv", encoding='utf-8') as file_stream:
        dest_reader = csv.DictReader(file_stream)
        for row in dest_reader:
            dest = Destination(row["country"], row["airport"], row["phone"], row["hours"], row["iata"])
            dest_list.append(dest)
        print(dest_list)
        return dest_list

        


get_destinations()


# def change_employee_info(att_list):
#     ''' Takes in att_list  '''
#     with open("testcsv.csv",'r' ,encoding="utf-8",) as read_file:
#         reader = csv.DictReader(read_file)
#         for row in reader:
#             if row["ssn"] == att_list[0]:
#                 emp = Employee(row["name"], row["address"], row["postal_code"], row["ssn"], 
#                 row["home_phone"], row["mobile_phone"], row["email"], row["work_area"])
#                 key = att_list[1]
#                 new = att_list[2]
#                 #Sets emp.key as new, changes the attribute
#                 setattr(emp, key, new)
#         write



>>>>>>> b6a23edf217b22626bb27b3a795aef63e2cf5b05
