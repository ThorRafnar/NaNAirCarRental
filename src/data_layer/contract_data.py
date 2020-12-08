from model_layer.contract import Contract
import csv

class ContractData():
    def list_all_contracts(self):
        ''' Opens up the file contracts.csv as file_stream and returns a list of contracts and their info.'''
        contract_list = []
        with open("data_layer/data_files/contracts.csv",encoding="utf-8") as file_stream:
            dest_reader = csv.DictReader(file_stream)
            for row in dest_reader:
                info = Contract(row["contract_id"], row["customer_ssn"], row["employee_ssn"], row["vehicle_id"], row["loan_date"], row["end_date"], row["base_price"],row['contract_created'],row['pickup_date'],row["return_date"], row["extensions"],row['total'], row["status"])
                contract_list.append(info)
        return contract_list

    def new_contract(self, contr):
        ''' Takes in instance of contract class and puts the information to contracts.csv file'''
        contr_list = [contr.contract_id,contr.customer_ssn,contr.employee_ssn,contr.vehicle_id,contr.loan_date,contr.end_date,contr.base_price,contr.contract_created,contr.pickup_date,contr.return_date,contr.extensions,contr.total,contr.status]
        with open("data_layer/data_files/contracts.csv",'a+' , encoding="utf-8",newline="") as file_stream:
            writer = csv.writer(file_stream)
            writer.writerow(contr_list)

    def change_contract_attributes(self, attribute_list):
        values = attribute_list[1].split(",")
        file_list = []
        with open("data_layer/data_files/contracts.csv","r",encoding="utf-8") as file_stream:
            reader = csv.DictReader(file_stream)
            contract_id = attribute_list[0]
            for row in reader:
                if row["contract_id"] == contract_id:
                    for key, value in zip(row, values):
                        row[key] = value
                file_list.append(row)
        
        with open("data_layer/data_files/contracts.csv", "w", encoding="utf-8", newline="") as file_stream:
            keys = file_list[0].keys()
            the_writer = csv.DictWriter(file_stream, keys)
            the_writer.writeheader()
            the_writer.writerows(file_list)

    def terminate_contract(self, contract_id):
        ''' Terminates contract by removing the contract from db '''
        file_list = []
        with open("data_layer/data_files/contracts.csv", 'r', encoding='utf-8') as file_stream:
            csv_reader = csv.DictReader(file_stream)
            for row in csv_reader:
                if row["contract_id"] != contract_id:
                    file_list.append(row)
        with open("data_layer/data_files/contracts.csv", "w", encoding="utf-8", newline="") as file_stream:
            keys = file_list[0].keys()
            the_writer = csv.DictWriter(file_stream, keys)
            the_writer.writeheader()
            the_writer.writerows(file_list)
            

