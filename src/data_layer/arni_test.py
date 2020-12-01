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


def change_employee_info(att_list):
    ''' Takes in att_list :^)  '''
    with open("testcsv.csv",'r' ,encoding="utf-8",) as read_file:
        reader = csv.DictReader(read_file)
        file_list = []
        for row in reader:
            if row["ssn"] == att_list[0]:
                key = att_list[1]
                new = att_list[2]
                row[key] = new
            file_list.append(row)
        
    with open("testcsv.csv", "w", encoding="utf-8", newline='') as write_file:
        keys = file_list[0].keys()
        the_writer = csv.DictWriter(write_file,keys)
        the_writer.writeheader()
        the_writer.writerows(file_list)






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



            
    
        


        
           

            
           
        
change_employee_info(att)
att = ["300279-1289","address","Vestursíða 38"]


