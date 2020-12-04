import csv

class ContractData:
    def list_all_contracts(self):
        ''' Opens up the file contracts.csv as file_stream and returns a list of contracts and their info.'''
        contract_list = []
        with open("src/data_layer/data_files/contracts.csv",encoding="utf-8") as file_stream:
            dest_reader = csv.DictReader(file_stream)
            for row in dest_reader:
                info = Contract(row["name"], row["ssn"], row["phone"], row["address"], row["email"], row["date_from"],
                row["date_to"], row["vehicle_id"], row["location"], row["vehicle_status"], row["employee_id"],
                row["loan_date"], row["return_date"], row["total"], row["loan_status"])
                contract_list.append(info)
        return contract_list

    def new_contract(self,info):
        ''' Takes in instance of contract class and puts the information to contracts.csv file'''
        info_list = [info.name,info,ssn,info.phone,info.address,info.email,info.date_from,info.date_to,info.vehicle_id,
        info.location,info.employee_id,info.loan_date,info.return_date,info.total,info.loan_status,
        info.contract_id,info.contract_status]
        with open("src/data_layer/data_files/contracts.csv",encoding="utf-8",newline="") as file_stream:
            writer = csv.writer(file_stream)
            writer.writerow(info_list)

    def change_contract_status(self, new_status, contract_id):
        reader = csv.DictReader(file_stream)
        file_list = []
        with open("data_later/data_files/contracts.csv","r",encoding="utf-8") as file_stream:
            for row in reader:
                if row["contract_id"] == info.contract_id:
                    row["contract_status"] = new_status
                file_list.append(row)
        
        with open("data_layer/data_files/contracts.csv", "w", encoding="utf-8", newline="") as file_stream:
            keys = file_list[0].keys()
            the_writer = csv.DictWriter(file_stream, keys)
            the_writer.writeheader()
            the_writer.writerows(file_list)