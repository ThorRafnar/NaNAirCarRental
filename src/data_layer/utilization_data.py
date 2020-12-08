import csv
from model_layer.utilization import Utilization


class UtilizationData():

    def add_utilization_log(self, a_list):
        ''' Writes utilization logs in DB '''
        with open("data_layer/data_files/utilization.csv", "a+", encoding="utf-8", newline='') as file_stream:
            csv_writer = csv.writer(file_stream)
            csv_writer.writerow(a_list)

    def get_utilization(self):
        ''' Returns Profits intstances to logic'''
        ret_list = []
        with open('data_layer/data_files/utilization.csv', 'r', encoding='utf-8') as file_stream:
            csv_reader = csv.DictReader(file_stream)
            for row in csv_reader:
                utilization = Utilization(row["date"], row["location"], row["vehicle_type"], row['manufacturer'], row['model'], row["pick_up"], row["return_date"])
                ret_list.append(utilization)
            return ret_list
