from model_layer.vehicle_type import VehicleType
import csv

class VehicleTypeData:

    def get_all_vehicle_types(self):
        with open("data_layer/data_files/vehicle_type.csv","r",encoding="utf-8") as file_stream:
            vehicle_type_list = []
            for line in file_stream:
                info = VehicleTypeLogic(line["name"], line["regions"], line["rate"])
                line = line.strip()
                vehicle_type_list.append(info)
            return vehicle_type_list
    
    def change_vehicle_rate(self,new_rate, vehicle_type):
        with open("data_layer/data_files/vehicle_type.csv","w",encoding="utf-8") as file_stream:
            reader = csv.DictReader(file_stream)
            file_list = []
            for line in file_stream:
                if line["name"] == vehicle_type:
                    line["rate"] = new_rate
                file_list.append(line)
        
        with open("data_layer/data_files/vehicle_type.csv","w",encoding="utf-8") as file_stream:
            keys = file_list[0].keys()
            the_writer = csv.DictWriter(file_stream,keys)
            the_writer.writeheader()
            the_writer.writerows(file_list)
    
    def new_vehicle_type(self, info):
        ''' Takes in information about new type in a list and writes it to the
        vehicle_type.csv file. '''
        a_list = [info.name,info.regions,info.rate]
        with open("data_layer/data_files/vehicle_type.csv","w",encoding="utf-8") as file_stream:
            writer = csv.writer(file_stream)
            writer.writerow(a_list)

