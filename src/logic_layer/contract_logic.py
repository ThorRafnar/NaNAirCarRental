class ContractLogic():
    def __init__(self, data_api):
        self.data_api = data_api

    def get_all_contracts(self):
        return self.list_all_contracts()

    def create_new_contract(self, contract):
        self.data_api.new_contract(contract)
    
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
        self.data_api.change_contract_status(contract_id, status)

    def get_contracts_by_attr(self, attr_list):
        col = attr_list[0]
        value = attr_list[1]
        contracts_list = self.get_all_contracts()
        filtered_list = [c for c in contracts_list if getattr(c, col).lower() == value.lower()]
        return filtered_list
        