import csv
#name,phone,address,email,date_from,date_to,vehicle_id,location,vehicle_status,employee_id,loan_date,return_date,total,loan_status

class ContractData:
    def list_all_contracts(self):
        contract_list = []
        with open("src/data_layer/data_files/contracts.csv",encoding="utf-8") as file_stream:
            for row in file_stream:
                info = ContractLogic(row["name"], row["phone"], row["address"], row["email"], row["date_from"], row["date_to"], row["vehicle_id"], row["location"], row["vehicle_status"], row["employee_id"], row["loan_date"], row["return_date"], row["total"], row["loan_status"])
                contract_list.append(info)
        return contract_list

    def new_contract(self,info):
        info_list = [info.name,info.phone,info.address,info.email,info.date_from,info.date_to,info.vehicle_id,info.location,info.employee_id,info.loan_date,info.return_date,info.total,info.loan_status]
        with open("src/data_layer/data_files/contracts.csv",encoding="utf-8",newline="") as file_stream:
            writer = csv.writer(file_stream)
            writer.writerow(info_list)

    def terminate_contract(self):
        pass

    def change_contract(self):
        pass