import csv
import os



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



