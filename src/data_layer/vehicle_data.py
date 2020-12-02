from model_layer.vehicle import VehicleLogic
import csv
import os
# Hjálp!!!!
# Pæling að láta alla klasa í data_layer að opna sín skrár svo það þarf þess ekki alltaf í hverju einasta falli? O.o :D <3
class VehicleData():
    

    def all_vehicles_to_list(self):
        ''' Opens the file "vehicle.csv" and makes an instance of a vehicle with each line then returns
        a list of all vehicles in that particular file. '''

        vehicle_list = []
        with open("src/data_layer/data_files/vehicle.csv", encoding="utf-8") as file_stream:
            reader = csv.DictReader(file_stream)
            for row in reader:
                # Here we get an instance of a vehicle (might change)
                # manufacturer,model,type,status,man_year,color,licence_type,location
                attb = VehicleLogic(row["manufacturer"], row["model"], row["type"], row
                ["status"], row["man_year"], row["color"], row["licence_type"], row["Location"])
                vehicle_list.append(attb)
        return vehicle_list
    

    
    def new_vehicle(self,att):
    ''' Opens the vehicle.csv file and writes a new line wich is the new vehicle'''
        a_list = [att.manufacturer,att.model,att.type,att.status,att.man_year,att.color,att.license_type,att.location]
        with open("src/data_layer/data_files/vehicle.csv","a+", encoding="utf8",newline="") as file_stream:
            writer = csv.writer(file_stream)
            writer.writerow(a_list)
            

    def change_vehicle_condition(self, cond_string,ID):
    ''' Opens the vehicle.csv file and selects a specific vehicle from it
        and changes the vehicle status/condition, if it is rentable or not.
        Takes in a string.'''
        with open ("data_files/vehicle.csv", "r",encoding="utf-8") as file_stream:
            reader = csv.DictReader(file_stream)
            file_list = []
            for line in reader:
                if line["ID"] == ID:
                    line["status"] = cond_string
                file_list.append(line)
        
        with open("data_files/vehicle.csv", "w", encoding="utf-8", newline="") as file_stream:
            keys = file_list[0].keys()
            the_writer = csv.DictWriter(file_stream, keys)
            the_writer.writeheader()
            the_writer.writerows(file_list)