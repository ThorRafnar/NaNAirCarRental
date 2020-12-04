from model_layer.contract import Contract
import csv

class ContractData():
    def list_all_contracts(self):
        ''' Opens up the file contracts.csv as file_stream and returns a list of contracts and their info.'''
        contract_list = []
        with open("src/data_layer/data_files/contracts.csv",encoding="utf-8") as file_stream:
            dest_reader = csv.DictReader(file_stream)
            for row in dest_reader:
                info = Contract(row["name"], row["ssn"], row["phone"], row["address"], row["email"], row["date_from"],
                row["date_to"], row["vehicle_id"], row["location"], row["vehicle_status"], row["employee_id"],
                row["loan_date"], row["return_date"], row["total"], row["loan_status"], row["contract_id"], row["contract_status"])
                contract_list.append(info)
        return contract_list

    def new_contract(self, contr):
        ''' Takes in instance of contract class and puts the information to contracts.csv file'''
        contr_list = [contr.name,contr.ssn,contr.phone,contr.address,contr.email,contr.date_from,contr.date_to,contr.vehicle_id,
        contr.location,contr.employee_id,contr.loan_date,contr.return_date,contr.total,contr.loan_status,
        contr.contract_id,contr.contract_status]
        with open("src/data_layer/data_files/contracts.csv",'a+' , encoding="utf-8",newline="") as file_stream:
            writer = csv.writer(file_stream)
            writer.writerow(contr_list)

    def change_contract_status(self, contract_id, contract_status):
        file_list = []
        with open("src/data_layer/data_files/contracts.csv","r",encoding="utf-8") as file_stream:
            reader = csv.DictReader(file_stream)
            for row in reader:
                if row["contract_id"] == contract_id:
                    row["contract_status"] = contract_status
                file_list.append(row)
        
        with open("src/data_layer/data_files/contracts.csv", "w", encoding="utf-8", newline="") as file_stream:
            keys = file_list[0].keys()
            the_writer = csv.DictWriter(file_stream, keys)
            the_writer.writeheader()
            the_writer.writerows(file_list)