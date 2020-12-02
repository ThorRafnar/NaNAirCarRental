from model_layer.destination import Destination

import csv
import os


class DestinationData():
    

    
    def get_destinations(self):
        ''' Returns all destinations in a list'''
        dest_list = []
        with open("data_layer/data_files/destinations.csv", encoding='utf-8') as file_stream:
            dest_reader = csv.DictReader(file_stream)
            for row in dest_reader:
                dest = Destination(row["country"], row["airport"], row["phone"], row["hours"], row["iata"])
                dest_list.append(dest)
            return dest_list

