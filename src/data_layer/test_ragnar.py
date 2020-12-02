# Main File for testing
# Do not change this shit
import csv

def new_vehicle_type(self, info):
    ''' Takes in information about new type in a list and writes it to the
    vehicle_type.csv file. '''
    a_list = [info.name,info.regions,info.rate]
    with open("data_layer/data_files/vehicle_type.csv","w",encoding="utf-8") as file_stream:
        writer = csv.writer(file_stream)
        writer.writerow(a_list)