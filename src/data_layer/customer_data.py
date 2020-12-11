from model_layer.customer import Customer
import csv

class CustomerData():

    def get_customers(self):
        ''' returns a list with instances of all customers  '''
        cust_list = []
        with open("data_layer/data_files/customers.csv", encoding='utf-8') as file_stream:
            cust_reader = csv.DictReader(file_stream)
            for row in cust_reader:
                cust = Customer(row["name"], row['ssn'], row["address"], row["postal_code"], row["phone"], row["email"], row["country"],row['licenses'])
                cust_list.append(cust)
            return cust_list

    def add_customer(self, cust):
        ''' writes new customer to database '''
        customer_list = [cust.name, cust.ssn, cust.address, cust.postal_code, cust.phone, cust.email, cust.country,cust.licenses]
        with open("data_layer/data_files/customers.csv", 'a+', encoding="utf-8", newline='') as file_stream:
            cust_writer = csv.writer(file_stream)
            cust_writer.writerow(customer_list)

    def change_customer_info(self, atttribute_list):
        '''Takes in a list with attributes. Uses thous attributes to 
        change certain info about the customer '''
        values = atttribute_list[1].split(",")
        file_list = []
        with open("data_layer/data_files/customers.csv", "r", encoding='utf-8') as read_file:
            reader = csv.DictReader(read_file)
            cust_ssn = atttribute_list[0]
            for row in reader:
                if row["ssn"] == cust_ssn:
                    for key, value in zip(row, values):
                        row[key] = value
                file_list.append(row)
                
        with open("data_layer/data_files/customers.csv", "w", encoding='utf-8', newline='') as write_file:
            keys = file_list[0].keys()
            writer = csv.DictWriter(write_file,keys)
            writer.writeheader()
            writer.writerows(file_list)
