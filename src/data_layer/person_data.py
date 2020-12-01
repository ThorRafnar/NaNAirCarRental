import csv

class PersonData():
    def __init__(self):
        self.file_stream = open("data_layer/data_files/customer.csv", encoding="utf-8")
    
    def get_all_employees(self):
        employees_list = []
        for line in self.file_stream:
            person_info = 
        
    