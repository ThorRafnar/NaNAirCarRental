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
                continue
            
            confirm = self.contract_ui.confirm_customer(customer)
            if confirm.lower() in self.ui_helper.YES:
                
                start_date = self.contract_ui.get_date("start")
                if start_date == None:
                    return

                end_date = self.contract_ui.get_date("end")
                if end_date == None:
                    return
                
                bills_list = self.logic_api.get_unpaid_contracts(customer.ssn, start_date, end_date)
                if len(bills_list) > 0:
                    self.confirm_bills(bills_list, customer, start_date, end_date)
                    return

                else:
                    self.no_bills_found(customer)

            else:
                return

    
    def confirm_bills(self, bills_list, customer, start_date, end_date, error_msg=""):
        ''' 
        Asks user if they want to confirm billing for the customer, 
        if yes, changes contract status to paid in every contract
        '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line(f"    Unpaid bills for {customer.name}, ssn {customer.ssn} from {start_date} to {end_date}")  
            self.ui_helper.print_blank_line()
            self.print_bills_list(bills_list)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_line("    Do you want to charge these bills? (y/n)")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_hash_line()
            print(error_msg)
            user_choice = input("Input: ")
            if user_choice.lower() in self.ui_helper.YES:
                self.send_bills(bills_list)
                return
            else:
                return


    def send_bills(self, bills_list):
        ''' Changes status of contracts in bills list to paid, and shows confirmation to user '''
        for contract in bills_list:
            self.logic_api.change_contract_status(contract.contract_id, "paid")
        self.payment_confirmed()

    
    def no_bills_found(self, customer):
        '''
        Informs user that no bills were found for this customer, enter to return to menu
        '''
        self.ui_helper.clear()
        self.ui_helper.print_header()
        self.ui_helper.print_line(f"No bills found for {customer.name}, ssn {customer.ssn}")
        self.ui_helper.print_line("Press enter to return")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_hash_line()
        print()
        _x = input("Input: ")
        return 


    def print_bills_list(self, bills_list):
        self.ui_helper.n_columns(["<< CONTRACT ID >>", "<< RETURN DATE >>", "<< BASE PRICE >>", "<< EXTENSIONS >>", "<< TOTAL PRICE >>"])
        amount_due = 0
        for contract in bills_list:
            amount_due += int(contract.total)
            self.ui_helper.n_columns([contract.contract_id, contract.return_date, contract.base_price, contract.extensions, contract.total])
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line(f"    AMOUNT DUE: {amount_due} Kr.")
        
    
    def payment_confirmed(self):
        '''
        Informs user that no bills were found for this customer, enter to return to menu
        '''
        self.ui_helper.clear()
        self.ui_helper.print_header()
        self.ui_helper.print_line(f"Bills have been charged")
        self.ui_helper.print_line("Press enter to return")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_hash_line()
        print()
        _x = input("Input: ")
        return 