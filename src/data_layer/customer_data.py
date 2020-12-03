from model_layer.customer import Customer
import csv

class CustomerData():

    def get_customers(self):
        cust_list = []
        with open("data_layer/data_files/customers.csv", encoding='utf-8') as file_stream:
            cust_reader = csv.DictReader(file_stream)
            for row in cust_reader:
                cust = Customer(row["name"], row["address"], row["postal_code"], row["phone"], row["email"], row["country"])
                cust_list.append(cust)
            return cust_list

    def add_customer(self, cust):
        ''' writes new customer to database '''
        customer_list = [cust.name, cust.address, cust.postal_code, cust.phone, cust.email, cust.country]
        with open("data_layer/data_files/customers.csv", 'a+', encoding="utf-8", newline='') as file_stream:
            cust_writer = csv.writer(file_stream)
            cust_writer.writerow(customer_list)

    def change_customer_info(self, att_list):
        '''Takes in a list with attributes. Uses thous attributes to 
        change certain info about the customer '''
        with open("data_layer/data_files/customers.csv", "r", encoding='utf-8') as read_file:
            reader = csv.DictReader(read_file)
            file_list = []
            for row in reader:
                # Key is the key for the attribute we want to change, and new is the new attribute
                if row["ssn"] == att_list[0]:
                    key = att_list[1]
                    new = att_list[2]
                    row[key] = new
                file_list.append(row)
                
        with open("data_layer/data_files/customers.csv", "w", encoding='utf-8', newline='') as write_file:
            keys = file_list[0].keys()
            writer = csv.DictWriter(write_file,keys)
            writer.writeheader()
            writer.writerows(file_list)
