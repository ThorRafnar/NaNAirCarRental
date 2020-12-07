import csv


class ProfitsData():

    def add_profits(self, a_list):
        ''' Writes profit logs in DB '''
        with open("test.csv", "a+", encoding="utf-8", newline='') as file_stream:
            csv_writer = csv.writer(file_stream)
            csv_writer.writerow(a_list)