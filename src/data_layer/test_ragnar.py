# Main File for testing
# Do not change this shit
import csv

class Destination():
    def __init__(self, country, airport, phone, hours, iata):
        self.country = country
        self.airport = airport
        self.phone = phone
        self.hours = hours
        self.iata = iata


def create_destination(dest):
    new_dest_list = [dest.country, dest.airport, dest.phone, dest.hours, dest.iata]
    with open("data_layer/data_files/destinations.csv", 'a+', encoding='utf-8', newline="") as file_stream:
        destwriter = csv.writer(file_stream)
        destwriter.writerow(new_dest_list)


a = Destination("aaa","aaa","aaa","aaa","aaa")
create_destination(a)