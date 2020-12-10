from model_layer.vehicle_type import VehicleType
import csv

class VehicleTypeData:

    def get_all_vehicle_types(self):
        ''' Opens the vehicle_type.csv file and returns all info in a list.'''
        with open("data_layer/data_files/vehicle_type.csv","r",encoding="utf-8") as file_stream:
            vehicle_type_list = []

            reader = csv.DictReader(file_stream)
            for line in reader:
                info = VehicleType(line["name"], line["rate"])
                vehicle_type_list.append(info)
            return vehicle_type_list
    
    def change_vehicle_rate(self, new_rate, vehicle_type):
        ''' Takes in a new desired rate and a vehicle type then changes the rate of that vehicle type
        to the new_desired rate.'''
        with open("data_layer/data_files/vehicle_type.csv","r",encoding="utf-8") as file_stream:
            reader = csv.DictReader(file_stream)
            file_list = []

            for row in reader:
                if row["name"] == vehicle_type: 
                    row["rate"] = new_rate
                file_list.append(row)
        
        with open("data_layer/data_files/vehicle_type.csv","w",encoding="utf-8") as file_stream:
            keys = file_list[0].keys()
            the_writer = csv.DictWriter(file_stream,keys)
            the_writer.writeheader()
            the_writer.writerows(file_list)
    
    def new_vehicle_type(self,info):
        ''' Takes in information about new type in a list and writes it to the
        vehicle_type.csv file. '''
        a_list = [info.name,info.rate]
        with open("data_layer/data_files/vehicle_type.csv","a+",encoding="utf-8", newline='') as file_stream:
            writer = csv.writer(file_stream)
            writer.writerow(a_list)

