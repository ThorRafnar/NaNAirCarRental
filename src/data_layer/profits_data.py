import csv
from model_layer.profit import Profit


class ProfitsData():

    def add_profits(self, a_list):
        ''' Writes profit logs in DB '''
        with open("data_layer/data_files/profits.csv", "a+", encoding="utf-8", newline='') as file_stream:
            csv_writer = csv.writer(file_stream)
            csv_writer.writerow(a_list)

    def get_profits(self):
        ''' Returns Profits intstances to logic'''
        ret_list = []
        with open('data_layer/data_files/profits.csv', 'r', encoding='utf-8') as file_stream:
            csv_reader = csv.DictReader(file_stream)
            for row in csv_reader:
                profits = Profit(row["date"], row["contract_id"], row["base_price"], row["extensions"], row["total"])
                ret_list.append(profits)
            return ret_list
