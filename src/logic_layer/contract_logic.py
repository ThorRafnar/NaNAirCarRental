from datetime import date

class ContractLogic():
    def __init__(self, data_api, vehicle_logic, type_logic):
        self.data_api = data_api
        self.vehicle_logic = vehicle_logic
        self.type_logic = type_logic

    def get_all_contracts(self):
        return self.data_api.list_all_contracts()

    def create_new_contract(self, contract):
        contract.base_price = self.set_contract_base_price(contract)
        contract.contract_id = self.set_contract_id()
        self.data_api.new_contract(contract)
    
    def set_contract_base_price(self, contract):
        vehicle = self.vehicle_logic.find_vehicle(contract.vehicle_id)
        type_rate = self.type_logic.get_types_rate(vehicle.type)
        number_of_days = self.calculate_number_of_days(contract.loan_date, contract.end_date)
        return type_rate * number_of_days
    
    def set_contract_id(self):
        contr_list = self.get_all_contracts()
        return len(contr_list) + 1
        
    def view_customer_contracts(self, ssn):
        contracts_list = self.get_all_contracts()
        customer_contracts = []
        for contract in contracts_list:
            if contract.ssn == ssn:
                customer_contracts.append(contract)
        return customer_contracts
    
    def find_contract(self, cont_id):
        contracts_list = self.get_all_contracts()
        correct_contract = None
        for contract in contracts_list:
            if contract.contract_id == cont_id:
                correct_contract = contract
        return correct_contract
    
    def change_contract_status(self, contract_id, status):
        day_fine = 200
        cont = self.find_contract(contract_id)
        cont.status = status
        if status == 'returned':
            cont.return_date = date.today().strftime('%d/%m/%Y')
            self.vehicle_logic.change_vehicle_condition(cont.vehicle_id, 'rentable')
            date_status = self.calculate_number_of_days(cont.end_date, cont.return_date)
            if date_status > 0:
                cont.extensions = day_fine * date_status
            cont.total = self.get_contract_total_price(cont)
        elif status == 'paid':
            pass
        else:
            pass

        attr_str = f'{cont.contract_id},{cont.customer_ssn},{cont.employee_ssn},{cont.vehicle_id},{cont.loan_date},{cont.end_date},{cont.base_price},{cont.return_date},{cont.extensions},{cont.total},{cont.status}'
        attr_list = [cont.contract_id, attr_str]
        self.data_api.change_contract_status(attr_list)
    
    def calculate_number_of_days(self, start_date, end_date):
        d,m,y = int(start_date[:2]),int(start_date[3:5]),int(start_date[6:])
        e_d,e_m,e_y = int(end_date[:2]),int(end_date[3:5]),int(end_date[6:])
        f_date = date(y, m, d)
        l_date = date(e_y, e_m, e_d)
        delta = l_date - f_date
        return delta.days
    
    def get_contract_total_price(self, contract):
        return int(contract.base_price) + int(contract.extensions)

    def get_contracts_by_attr(self, attr_list):
        col = attr_list[0]
        value = attr_list[1]
        contracts_list = self.get_all_contracts()
        filtered_list = [c for c in contracts_list if getattr(c, col).lower() == value.lower()]
        return filtered_list
        