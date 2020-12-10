class BillingUI():

    def __init__(self, ui_helper, logic_api, contract_ui):
        self.ui_helper = ui_helper
        self.logic_api = logic_api
        self.contract_ui = contract_ui

    def billing_menu(self):
        '''
        Asks for a customer ssn and finds it
        then gets a start and end date and asks if user wants to bill user for that timeframe, if any
        '''
        while True:
            customer, ssn = self.contract_ui.find_customer()
            if ssn == None:
                return

            if customer == None:
                self.contract_ui.customer_not_found()
            
            confirm = self.contract_ui.confirm_customer(customer)
            if confirm.lower() in self.ui_helper.YES:
                
                start_date = self.contract_ui.get_date("start")
                if start_date == None:
                    return

                end_date = self.contract_ui.get_date("end")
                if end_date == None:
                    return
                
                #bills_list = self.logic_api.get_unpaid_contracts(customer.ssn, start_date, end_date)
                print("whats up")
                return input("...")

            else:
                continue
    
    def send_bills(self, bills_list, customer):
        ''' 
        Asks user if they want to confirm billing for the customer, 
        if yes, changes contract status to paid in every contract
        '''
        pass