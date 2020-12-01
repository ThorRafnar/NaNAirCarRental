# Main File for testing
# Do not change this shit
from vehicle_data import VehicleData
from contract_data import ContractData
import csv

# name,phone,address,email,date_from,date_to,vehicle_id,location,vehicle_status,employee_id,loan_date,return_date,total loan_status
class ContractLogic:
    def __init__(self, name, phone, address, email, date_from, date_to, vehicle_id, location, vehicle_status, employee_id, loan_date, return_date, total, loan_status):
        self.name = name
        self.phone = phone
        self.address = address
        self.email = email
        self.date_from = date_from
        self.date_to = date to
        self.vehicle_id = vehicle_id
        self.location = location
        self.vehicle_status = vehicle_status
        self.employee_id = employee_id
        self.loan_date = loan_date
        self.return_date = return_date
        self.loan_status = loan_status
        self.total = total



# class VehicleLogic:
#     def __init__(self, manufacturer, model, type, status, man_year, color, license_type, location):
#         self.manufacturer = manufacturer
#         self.model = model
#         self.type = status
#         self.status = status
#         self.man_year = man_year
#         self.color = color
#         self.license_type = license_type
#         self.location = location

# def new_vehicle(att):
#     ''' Opens the vehicle.csv file and writes a new line wich is the new vehicle'''
#     a_list = [att.manufacturer,att.model,att.type,att.status,att.man_year,att.color,att.license_type,att.location]
#     with open("src/data_layer/data_files/vehicle.csv","a+", encoding="utf8",newline="") as file_stream:
#         writer = csv.writer(file_stream)
#         writer.writerow(a_list)

# def new_v(att):
#     new_vehicle(att)

# r = VehicleLogic("asd","asd","asd","asd","asd","asd","asd","asd")
# new_v(r)