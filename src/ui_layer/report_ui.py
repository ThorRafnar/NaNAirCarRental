class ReportUI():
    ### CLASS  CONSTANTS ###
    ## FOR MENU SELECTION ##
    PROFIT_REPORTS = "Profits"
    UTILIZATION_REPORTS = "Utilization Reports"
    BILLS = "Billing information"


    def __init__(self, ui_helper, logic_api):

        self.ui_helper = ui_helper
        self.logic_api = logic_api
        self.options_dict = {
            "1": self.PROFIT_REPORTS,
            "2": self.UTILIZATION_REPORTS,
            "3": self.BILLS
        }
    
# Menu section
    def reports_menu(self, error_msg = ""):
        ''' Shows the option menu from the reports section'''
        while True:
            user_choice = self.show_options(error_msg)

            if user_choice != None:

                if user_choice.lower() == self.ui_helper.QUIT:
                    self.ui_helper.quit_prompt()

                elif user_choice.lower() == self.ui_helper.BACK:
                    return

                else:
                    if self.options_dict[user_choice] == self.PROFIT_REPORTS:

                        self.profits_menu()
          

                    elif self.options_dict[user_choice] == self.UTILIZATION_REPORTS:
                        
                        self.uitilization_menu()

                    elif self.options_dict[user_choice] == self.BILLS:

                        self.bill_information_menu()
            else:
                error_msg = "Please select an option from the menu"


    def profits_menu(self):
        ''' Shows profit report, asks for start and end date '''
        start_date = self.get_date("start")
        if start_date != None:
            if start_date == self.ui_helper.BACK:
                return

            elif start_date == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()

            else:

                end_date = self.get_date("end")
                if end_date != None:
                    if end_date == self.ui_helper.BACK:
                        return

                    elif end_date == self.ui_helper.QUIT:
                        self.ui_helper.quit_prompt()

                    else:
                        self.show_profit_reports(start_date, end_date)

                else:
                    return
        else:
            return
    

    def show_options(self, error_msg=""):
        options_list = self.ui_helper.dict_to_list(self.options_dict)
        self.ui_helper.clear()
        self.ui_helper.print_header()
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line("Select Task:")
        for option in options_list:
            self.ui_helper.print_line(f"    {option[0]}. {option[1]}")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_footer()
        print(error_msg)
        return self.ui_helper.get_user_menu_choice(options_list)
# End of menu section

# Start of profit section
    def show_profit_reports(self, start_date, end_date, error_msg=""):
        profit_reports = self.logic_api.calculate_profits(start_date, end_date)
        total_profits = profit_reports[0]
        vehicle_profit_dict = profit_reports[1]
        location_profit_dict = profit_reports[2]
        
        if total_profits == 0: 
            self.no_data_to_report(f"No data to report on from {start_date} to {end_date}")
            return

        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_centered_line_dash(f"<< Profit Report from {start_date} to {end_date} >>")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_centered_line_dash("<< PROFITS BY LOCATION >>----------------------")
            self.ui_helper.print_blank_line()
            self.print_profts(location_profit_dict)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_centered_line_dash("<< PROFITS BY VEHICLE TYPE >>------------------")
            self.ui_helper.print_blank_line()
            self.print_profts(vehicle_profit_dict)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_line(f"TOTAL PROFITS FROM {start_date} TO {end_date}: {total_profits}")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = self.ui_helper.get_user_menu_choice([])
            if user_choice != None:
                if user_choice.lower() == self.ui_helper.BACK:
                    return
                elif user_choice.lower() == self.ui_helper.QUIT:
                    self.ui_helper.quit_prompt()
            else:
                error_msg = f"Please enter {self.ui_helper.QUIT.upper()} to quit or {self.ui_helper.BACK.upper()} to go back"


    def make_scale(self, top_of_scale, steps):
        ''' Returns a scale (list) in reverse order '''
        lowest = 0
        current = top_of_scale
        scale_list = []
        while current >= lowest:
            scale_list.append(current)
            current -= steps

        return scale_list

        
    def print_profts(self, profits_dict):
        ''' Prints profits as columns '''
        symbol = "Kr."
        
        max_val = max(val for key, val in profits_dict.items())
        steps = max_val // 10
        column_width = 15
        grapth_width = (column_width + 1) * len(profits_dict) + 1
        scale = self.make_scale(max_val, steps)

        #prints columns
        for ind, row in enumerate(scale):
            if ind == 0:
                a_str = " " + "_" * (grapth_width)
                a_str += f"__{row} {symbol}"
            else:
                a_str = "| "
                for _key, val in profits_dict.items():

                    if val > row:
                        a_str += "#" * column_width + " "
                    else:
                        a_str += " " * column_width + " "

                if ind % 2 != 1:
                    a_str += f"|_{row} {symbol}"
                else:
                    a_str += "|"
            
            self.ui_helper.print_line(a_str)
        
        self.ui_helper.print_line("|" + ("‾" * (grapth_width) + "|"))     
        #Prints keys
        key_str = "| "
        val_str = "| "
        for key, val in profits_dict.items():
            #key = self.logic_api.city_to_iata(key)
            key_str += "{: ^{width}}".format(key, width = column_width + 1)

            val = f"{str(val)} {symbol}"
            val_str += "{: ^{width}}".format(val, width = column_width + 1)

        key_str += "|"
        val_str += "|"
        self.ui_helper.print_line(key_str)
        self.ui_helper.print_line(val_str)
        self.ui_helper.print_line("|" + ("_" * (grapth_width) + "|"))

        
    def get_date(self, a_str, error_msg=""):
        ''' gets a date from user and error checks it '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_blank_line()
            self.ui_helper.print_line(f"    Enter {a_str} date: (dd/mm/yyyy)")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            the_date = input("Input: ")
            if the_date == self.ui_helper.BACK:
                return

            elif the_date == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()

            the_date = self.logic_api.check_date(the_date)  #Checks if valid

            if the_date != None:
                return the_date

            else:
                error_msg = "Please enter a valid date (DD/MM/YYYY)"

    
# Start of utilization section
    def uitilization_menu(self):
        ''' Gets location and then shows utilization report for it '''
        location = self.ui_helper.get_location("Select location for utilization report:")
        if location != None:
            self.show_utilization_report(location)
            
        else:
            return
    

    def show_utilization_report(self, location_name, error_msg=""):
        ''' Shows utilization reports per vehicle for either all locations or just one'''
        padding = 70
        scale_length = 100
        location = self.logic_api.find_destination(location_name)
        util_logs = self.logic_api.get_utilization_for_location(location.airport)

        if util_logs != {}:

            while True:
                self.ui_helper.clear()
                self.ui_helper.print_header()
                self.ui_helper.print_blank_line()
                self.ui_helper.print_centered_line_dash(f"<< VEHICLE UTILIZATION IN {location.airport}, {location.country} >>---------------")

                #DO NOT TOUCH THIS LINE!!!
                header = "{: ^6}{: ^38}{: ^12}{: ^12}{: ^100}".format("ID", "MAKE, MODEL", "FIRST USE", "LAST RETURN", "UTILIZATION PERCENTAGE")
                self.ui_helper.print_blank_line()
                self.ui_helper.print_line(header)
                for vehicle_type, values in util_logs.items():
                    self.ui_helper.seperator()
                    self.ui_helper.print_line(vehicle_type.upper())
                    self.ui_helper.print_line(" " * padding + "_" * (scale_length + 2))
                    for vehicle in values:
                        vehicle_id = vehicle[0]
                        vehicle_name = vehicle[1]
                        first_use_date = vehicle[2].strftime("%d/%m/%y")
                        recent_use_date = vehicle[3].strftime("%d/%m/%y")
                        percent = vehicle[4]
                        ratio = percent 

                        #DO NOT TOUCH THIS LINE!!!
                        info_str = "{: ^6}{: ^38}{: ^12}{: ^12}  ".format(vehicle_id, vehicle_name, first_use_date, recent_use_date)
                        percent_string = ("|" + "#" * ratio + " " * (scale_length - ratio) + f"| {str(percent)} %")
                        self.ui_helper.print_line(f"{info_str}{percent_string}")
                    self.ui_helper.print_line(" " * padding + "‾" * (scale_length + 2))
                self.ui_helper.print_footer()
                print()
                user_choice = input("Input: ")
                if user_choice.lower() == self.ui_helper.BACK:
                    return
                elif user_choice.lower() == self.ui_helper.QUIT:
                    self.ui_helper.quit_prompt()
                else:
                    error_msg = f"Enter {self.ui_helper.QUIT.upper()} to quit or {self.ui_helper.BACK.upper()} to go back"

        else:
            self.no_data_to_report(f"No data to display in {location.iata}")
            return


    def no_data_to_report(self, a_str):
        ''' Informs user that location has no data to report '''
        self.ui_helper.clear()
        self.ui_helper.print_header()
        self.ui_helper.print_line(a_str)
        self.ui_helper.print_line("Press enter to continue")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_hash_line()
        print()
        _x = input("Input: ")
        return
    

#Bill information section
    def bill_information_menu(self, error_msg =""):
        ''' Allows user to see different billing reports, paid and unpaid '''
        start_date = self.get_date("start")
        if start_date == None:
            return

        end_date = self.get_date("end")
        if start_date == None:
            return

        contracts_dict = self.logic_api.get_paid_and_unpaid_contracts(start_date, end_date)

        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            if len(contracts_dict) > 0:
                contract_header = ["<< ID >>", "<< TOTAL PRICE >>", "<< BASE PRICE >>", "<< EXTENSIONS >>", "<< START DATE >>", "<< RETURN DATE >>"]
                self.ui_helper.print_centered_line_dash(f"<< BILLING FROM {start_date} TO {end_date} >>----------------------------")
                self.ui_helper.print_blank_line()
                self.ui_helper.n_columns(contract_header)
                self.ui_helper.print_blank_line()
                for customer_name, contracts in contracts_dict.items():
                    self.ui_helper.seperator()
                    self.ui_helper.print_blank_line()
                    self.ui_helper.print_line(f"    << Billing overview for {customer_name} >>")

                    if "paid" in contracts:
                        self.ui_helper.print_centered_line_dash(f"<< PAID >>")
                        self.ui_helper.print_blank_line()
                        for contract in contracts["paid"]:
                            self.print_bill(contract)
                    else:
                        pass

                    self.ui_helper.print_blank_line()

                    if "unpaid" in contracts:
                        self.ui_helper.print_centered_line_dash(f"<< UNPAID >>")
                        self.ui_helper.print_blank_line()
                        for contract in contracts["unpaid"]:
                            self.print_bill(contract)
                    else:
                        pass

                    self.ui_helper.print_blank_line()
                    self.ui_helper.seperator()
            else:
                self.ui_helper.print_line(f"No contracts from {start_date} to {end_date}")
           
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            user_input = input("Input: ")

            if user_input.lower() == self.ui_helper.BACK:
                return

            elif user_input.lower() == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()

            else:
                error_msg = f"Please enter {self.ui_helper.QUIT.upper()} to quit or {self.ui_helper.BACK.upper()} to go back"


    def print_bill(self, contract):
        ''' Prints a single contract for billing overview '''
        contract_column = [contract.contract_id, contract.total, contract.base_price, contract.extensions, contract.loan_date, contract.end_date]
        self.ui_helper.n_columns(contract_column)

