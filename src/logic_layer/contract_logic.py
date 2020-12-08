from datetime import date

class ContractLogic():
    def __init__(self, data_api, vehicle_logic, type_logic):
        self.data_api = data_api
        self.vehicle_logic = vehicle_logic
        self.type_logic = type_logic

    def get_all_contracts(self):
        ''' Returns a list of all contracts as instances of Contract classes '''
        return self.data_api.list_all_contracts()

    def create_new_contract(self, contract):
        ''' Does initial operations on new contract like calculating base price, reserving given vehicle and giving contract new ID, than sending that contract to data layer to store in contract.csv '''
        contract.base_price = self.set_contract_base_price(contract)
        contract.contract_id = self.set_contract_id()
        contract.contract_created = date.today().strftime('%d/%m/%Y')
        
        self.data_api.new_contract(contract)
    
    def set_contract_base_price(self, contract):
        ''' Calculates base price from vehicle type rate multiplied by number of days rented '''
        vehicle = self.vehicle_logic.find_vehicle(contract.vehicle_id)
        type_rate = self.type_logic.get_types_rate(vehicle.type)
        number_of_days = self.calculate_number_of_days(contract.loan_date, contract.end_date)
        return type_rate * number_of_days
    
    def set_contract_id(self):
        ''' Adds new ID on new contract '''
        contr_list = self.get_all_contracts()
        last_id = int(contr_list[-1].contract_id)
        return last_id + 1
        
    def view_customer_contracts(self, ssn):
        ''' Gets an customer ssn from UI and checks if customer owns contracts in database, returns a list of all contracst for given ssn if found, else returns an empty list '''
        contracts_list = self.get_all_contracts()
        customer_contracts = []
        for contract in contracts_list:
            if contract.customer_ssn == ssn:
                customer_contracts.append(contract)
        return customer_contracts
    
    def find_contract(self, cont_id):
        ''' Searches for a contract from given contract ID and returns an instance of contract class if found, else returns None '''
        contracts_list = self.get_all_contracts()
        correct_contract = None
        for contract in contracts_list:
            if contract.contract_id == cont_id:
                correct_contract = contract
        return correct_contract
    
    #hreinsa til method
    def change_contract_status(self, contract_id, status):
        ''' Changes contract status for given contract by ID '''
        cont = self.find_contract(contract_id)
        cont.status = status.lower()
        if cont.status == 'active':
            cont.pickup_date = date.today().strftime('%d/%m/%Y')
            self.vehicle_logic.change_vehicle_condition(cont.vehicle_id, 'in_rent')
        elif cont.status == 'returned':
            cont.return_date = date.today().strftime('%d/%m/%Y')
            self.vehicle_logic.change_vehicle_condition(cont.vehicle_id, 'rentable')
            date_status = self.calculate_number_of_days(cont.end_date, cont.return_date)
            if date_status > 0:
                cont.extensions = self.calc_extensions(cont.vehicle_id, date_status)
            cont.total = self.get_contract_total_price(cont)
        elif cont.status == 'paid':
            paid_date = date.today()
            profit_log = [paid_date,cont.contract_id,cont.base_price,cont.extensions,cont.total]
            self.data_api.add_profits(profit_log)
        elif cont.status == 'terminated':
            self.data_api.terminate_contract(cont.contract_id)
        
        attr_string = f'{cont.contract_id},{cont.customer_ssn},{cont.employee_ssn},{cont.vehicle_id},{cont.loan_date},{cont.end_date},{cont.base_price},{cont.contract_created},{cont.pickup_date},{cont.return_date},{cont.extensions},{cont.total},{cont.status}'

        attr_list = [cont.contract_id, attr_string]
        self.data_api.change_contract_attributes(attr_list)
    
    def calculate_number_of_days(self, start_date, end_date):
        ''' Calculates how many days are between given dates '''
        d,m,y = int(start_date[:2]),int(start_date[3:5]),int(start_date[6:])
        e_d,e_m,e_y = int(end_date[:2]),int(end_date[3:5]),int(end_date[6:])
        f_date = date(y, m, d)
        l_date = date(e_y, e_m, e_d)
        delta = l_date - f_date
        return delta.days
    
    def calc_extensions(self, vehicle_id, date_status):
        ''' Gets vehicle type for given vehicle and adds 50% on top of it then calculates that with number of days in late return '''
        vehicle = self.vehicle_logic.find_vehicle(vehicle_id)
        type_rate = int(self.type_logic.get_types_rate(vehicle.type))
        tax = type_rate * 1.2
        return date_status * tax

    def get_contract_total_price(self, contract):
        ''' Adds extensions with base price to calculate total price '''
        return int(contract.base_price) + int(contract.extensions)
    
    def change_contract_dates(self,contract_id,start_date,end_date):
        cont = self.find_contract(contract_id)
        cont.loan_date = start_date
        cont.end_date = end_date
        cont.base_price = self.set_contract_base_price(cont)

        attr_string = f'{cont.contract_id},{cont.customer_ssn},{cont.employee_ssn},{cont.vehicle_id},{cont.loan_date},{cont.end_date},{cont.base_price},{cont.contract_created},{cont.pickup_date},{cont.return_date},{cont.extensions},{cont.total},{cont.status}'

        attr_list = [cont.contract_id, attr_string]

        self.data_api.change_contract_attributes(attr_list)
    
    def change_contract_vehicle(self,contract_id, veh_id):
        cont = self.find_contract(contract_id)
        cont.vehicle_id = veh_id

        attr_string = f'{cont.contract_id},{cont.customer_ssn},{cont.employee_ssn},{cont.vehicle_id},{cont.loan_date},{cont.end_date},{cont.base_price},{cont.contract_created},{cont.pickup_date},{cont.return_date},{cont.extensions},{cont.total},{cont.status}'

        attr_list = [cont.contract_id, attr_string]

        self.data_api.change_contract_attributes(attr_list)

    def get_contracts_by_attr(self, attr_list):
        ''' Returns a list of contracts from given attributes '''
        col = attr_list[0]
        value = attr_list[1]
        contracts_list = self.get_all_contracts()
        filtered_list = [c for c in contracts_list if getattr(c, col).lower() == value.lower()]
        return filtered_list
