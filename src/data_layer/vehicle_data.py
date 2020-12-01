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
    

    
    def new_vehicle(self, manufacturer, model, type, status, man_year, color, licence_type, Location):
        ''' Opens the vehicle.csv file and writes a new line wich is the new vehicle'''
        with open("src/data_layer/data_files/vehicle.csv","a", encoding="utf-8") as file_stream:
            file_stream.writerow(manufacturer, model, type, status, man_year, color, licence_type, Location)
            

    def delete_vehicle(self):
        ''' Opens the vehicle.csv file and deletes a specific line from it.'''

    def change_vehicle(self):
        ''' Opens the vehicle.csv file and selects a specific line from it and changes a 
        desired attribute in said line
        Kannski að gera það bara í logic layernum? - Ragnar
        Allanvega eina sem data layerinn á að gera er að opan skrár, logic getur síðan breytt henni og UI sér um 
        hvað á að koma í staðinn. '''