from model_layer.customer import Customer
import csv

class CustomerData():

    def get_customers(self):
        cust_list = []
        with open("test.csv", encoding='utf-8') as file_stream:
            cust_reader = csv.DictReader(file_stream)
            for row in cust_reader:
                cust = Customer(row["name"], row["address"], row["postal_code"], row["phone"], row["email"], row["country"])
                cust_list.append(cust)
            return cust_list