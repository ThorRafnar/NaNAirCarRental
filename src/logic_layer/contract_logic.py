from datetime import datetime,date

class ContractLogic():

    def __init__(self, data_api, vehicle_logic, type_logic, destination_logic, customer_logic):
        self.data_api = data_api
        self.vehicle_logic = vehicle_logic
        self.desination_logic = destination_logic
        self.customer_logic = customer_logic
        self.type_logic = type_logic
        self.today = date.today().strftime('%d/%m/%Y')

    def get_all_contracts(self):
        ''' Returns a list of all contracts as instances of Contract classes '''
        return self.data_api.list_all_contracts()

    def create_new_contract(self, contract):
        ''' Does initial operations on new contract like calculating base price, reserving given vehicle and giving contract new ID, than sending that contract to data layer to store in contract.csv '''
        contract.base_price = self.set_contract_base_price(contract)
        contract.contract_id = self.set_contract_id()
        contract.contract_created = self.today
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
    
    def get_pending_contracts(self, ssn):
        ''' Returns pending contracts by customer ssn '''
        customer_contracts = self.view_customer_contracts(ssn)
        pending_contracts = []
        for contract in customer_contracts:
            contract_date = datetime.strptime(contract.loan_date, '%d/%m/%Y')
            
            if self.today >= contract_date and contract.status.lower() == 'pending':
                pending_contracts.append(contract)
        return pending_contracts
    
    def find_contract(self, cont_id):
        ''' Searches for a contract from given contract ID and returns an instance of contract class if found, else returns None '''
        contracts_list = self.get_all_contracts()
        correct_contract = None
        for contract in contracts_list:
            if contract.contract_id == cont_id:
                correct_contract = contract
        return correct_contract
    
    def change_contract_status(self, contract_id, status):
        ''' Changes contract status for given contract by ID and does expected behavior for given status '''
        cont = self.find_contract(contract_id)
        cont.status = status.lower()

        if cont.status == 'active':
            cont.pickup_date = self.today
            self.vehicle_logic.change_vehicle_condition(cont.vehicle_id, 'in_rent')
        elif cont.status == 'returned':
            cont.return_date = self.today
            self.vehicle_logic.change_vehicle_condition(cont.vehicle_id, 'rentable')
            date_status = self.calculate_number_of_days(cont.end_date, cont.return_date)

            if date_status > 0:
                cont.extensions = self.calc_extensions(cont.vehicle_id, date_status)
            self.add_utilization_log(cont) # Adds utilization log for vehicle in utilization.csv
            cont.total = self.get_contract_total_price(cont)
        elif cont.status == 'paid':
            self.add_profit_log(cont) # Adds profit log for contract in profit.csv
        elif cont.status == 'terminated':
            self.data_api.terminate_contract(cont.contract_id) # Terminates contract from contracts.csv

        if cont.status != 'terminated':
            self.change_contract(cont) # Changes contract status if not terminated
            
    
    def calculate_number_of_days(self, start_date, end_date):
        ''' Calculates how many days are between given dates, returns it as integer '''
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

    def get_contracts_by_attr(self, attr_list):
        ''' Returns a list of contracts from given attributes '''
        col = attr_list[0]
        value = attr_list[1]
        contracts_list = self.get_all_contracts()
        filtered_list = [c for c in contracts_list if getattr(c, col).lower() == value.lower()]
        return filtered_list
    
    def add_utilization_log(self, contract):
        ''' Gets an instance of contract and creates a utilization log and adds it to utilization.csv '''
        vehicle = self.vehicle_logic.find_vehicle(contract.vehicle_id)
        util_list = [vehicle.id, self.today, vehicle.location, vehicle.type, vehicle.manufacturer, vehicle.model, contract.pickup_date, contract.return_date]
        self.data_api.add_utilization_log(util_list)
    
    def add_profit_log(self, contract):
        ''' Gets an instance of contract and creates a profit log and adds it to profit.csv '''
        vehicle = self.vehicle_logic.find_vehicle(contract.vehicle_id)
        profit_log = [self.today,contract.contract_id,contract.base_price,contract.extensions,contract.total,vehicle.type,vehicle.location]
        self.data_api.add_profits(profit_log)

    def get_unpaid_contracts(self, ssn, start_date, end_date):
        '''Retunrs a list of contracts instances that have yet to pay their contract '''
        ret_list = [] 
        d,m,y = int(start_date[:2]),int(start_date[3:5]),int(start_date[6:])
        e_d,e_m,e_y = int(end_date[:2]),int(end_date[3:5]),int(end_date[6:])
        start = date(y, m, d)
        end = date(e_y, e_m, e_d)

        contracts = self.get_all_contracts()
        for contract in contracts:
            try:
                d_r, m_r, y_r = int(contract.return_date[0:2]), int(contract.return_date[3:5]), int(contract.return_date[6:])
                return_date = date(y_r, m_r, d_r)
                if start <= return_date <= end and contract.status.lower() == 'returned' and contract.customer_ssn == ssn:
                    ret_list.append(contract)

            except ValueError:  #If contact hasn't been returned, there is no return date
                pass
            
        return ret_list

    def change_contract(self, contract):
        ''' Gets an instance of Contract class and sends it to data to be changed in database '''
        self.data_api.change_contract(contract)

    def find_paid_and_unpaid_contracts(self, start_date, end_date):
        ''' finds all paid and unpaid contract for given time, returns as dictionary with customer name as key '''
        d,m,y = int(start_date[:2]),int(start_date[3:5]),int(start_date[6:])
        e_d,e_m,e_y = int(end_date[:2]),int(end_date[3:5]),int(end_date[6:])
        start = date(y, m, d)
        end = date(e_y, e_m, e_d)
        contracts = self.get_all_contracts()
        bill_dict = {}

        for contract in contracts:
            try:
                d_r, m_r, y_r = int(contract.return_date[0:2]), int(contract.return_date[3:5]), int(contract.return_date[6:])
                return_date = date(y_r, m_r, d_r)
                customer = self.customer_logic.find_customer(contract.customer_ssn)
                if start <= return_date <= end:
                    if contract.status == 'returned' or contract.status == 'paid':
                        if contract.status == 'returned':
                            contract.status = 'unpaid'
                        if customer.name not in bill_dict:
                            bill_dict[customer.name] = [contract]
                        else:
                            bill_dict[customer.name].append(contract) 
            except ValueError:  #if contract has no return date yet
                pass
        
        return bill_dict

    def get_paid_and_unpaid_contracts(self, start_date, end_date):
        ''' Fetches a dictionary of paid and unpaid contracts and returns it with dictionaries for paid and unpaid contract for all customers '''
        filtered_dict = self.find_paid_and_unpaid_contracts(start_date,end_date)

        for customer in filtered_dict:
            customer_dict = {}
            for contract in filtered_dict[customer]:
                if contract.status not in customer_dict:
                    customer_dict[contract.status] = [contract]
                else:
                    customer_dict[contract.status].append(contract)
                filtered_dict[customer] = customer_dict

        return filtered_dict


    def get_active_contract(self, vehicle_id, location_iata):
        ''' Returns active contract for a given vehicle id in a location, returning none if none exists '''
        contracts = self.get_all_contracts()
        vehicle = self.vehicle_logic.find_vehicle(vehicle_id)
        user_location = self.desination_logic.find_destination(location_iata)
        if user_location.airport == vehicle.location:
            for contract in contracts:
                if contract.vehicle_id == vehicle_id and contract.status.lower() == "active":
                    return contract

            return None

        else:
            return None