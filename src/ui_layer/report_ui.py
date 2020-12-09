class ReportUI():
    ### CLASS  CONSTANTS ###
    ## FOR MENU SELECTION ##
    PROFIT_REPORTS = "Profits"
    UTILIZATION_REPORTS = "Utilization Reports"
    BILLS = "Bills"


    def __init__(self, ui_helper, logic_api):

        self.ui_helper = ui_helper
        self.logic_api = logic_api
        self.options_dict = {
            "1": self.PROFIT_REPORTS,
            "2": self.UTILIZATION_REPORTS,
            "3": self.BILLS,
        }
    
# Menu section
    def reports_menu(self, error_msg = ""):
        ''' Shows the option menu from the reports section'''
        while True:
            user_choice = self.show_options(error_msg)

            if user_choice != None:

                if self.options_dict[user_choice].lower() == self.ui_helper.QUIT:
                    self.ui_helper.quit_prompt()

                elif self.options_dict[user_choice].lower() == self.ui_helper.BACK:
                    return

                else:
                    if self.options_dict[user_choice] == self.PROFIT_REPORTS:

                        self.profits_menu()
          

                    elif self.options_dict[user_choice] == self.UTILIZATION_REPORTS:
                        start_date, end_date = self.ask_end_and_start_date()
                        if start_date == self.ui_helper.BACK or end_date == self.ui_helper.BACK:
                            return
                        elif start_date == self.ui_helper.QUIT or end_date == self.ui_helper.QUIT:
                            self.ui_helper.quit_prompt()

                        location = self.ask_location()
                        self.show_utilization_report(start_date, end_date,location)
                        pass

                    elif self.options_dict[user_choice] == self.BILLS:
                        # Call a function wich deals with bills.
                        pass
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
        self.ui_helper.print_line("    Tasks:")
        self.ui_helper.print_blank_line()
        for option in options_list:
            self.ui_helper.print_line(f"    {option[0]}. {option[1]}")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_footer()
        print(error_msg)
        return self.ui_helper.get_user_menu_choice(options_list)
# End of menu section

# Start of profit section
    def show_profit_reports(self, start_date, end_date):
        profit_reports = self.logic_api.calculate_profits(start_date, end_date)
        total_profits = profit_reports[0]
        vehicle_profit_dict = profit_reports[1]
        location_profit_dict = profit_reports[2]
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line(f"    Profit Report from {start_date} to {end_date}")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_line(f"    TOTAL PROFITS {total_profits}")
            self.ui_helper.print_blank_line()
            self.print_profts(location_profit_dict)
            return input("...")

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
        steps = max_val // 9
        top_of_scale = max_val + max_val % 9
        column_width = 3
        grapth_width = (column_width + 2) * len(profits_dict)
        scale = self.make_scale(top_of_scale, steps)

        #prints columns
        for ind, row in enumerate(scale):
            if ind == 0:
                a_str = "_" * (grapth_width - 2)
                a_str += f"_{row} {symbol}"
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
        
        self.ui_helper.seperator()
        
        #Prints keys
        key_str = ""
        for key in profits_dict:
            key = self.logic_api.city_to_iata(key)
            if len(key) > column_width:
                for i in range(column_width):
                    key_str += key[i]
                key_str += " "
                
            else:
                spaces = column_width - len(key) + 1
                key_str = key + (" " * spaces)

        self.ui_helper.print_line(key_str)
        self.ui_helper.seperator()



        

        
    def get_date(self, a_str):
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_blank_line()
            self.ui_helper.print_line(f"    Enter {a_str} date: (dd/mm/yyyy)")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            the_date = input("Input: ")
            if the_date == self.ui_helper.BACK:
                return

            elif the_date == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()

            the_date = self.logic_api.check_date(the_date)  #Checks if valid
            if the_date != None:
                return the_date

    
# Start of utilization section
    def ask_location(self):
        valid_locations = self.logic_api.destinations_option_list()
        self.ui_helper.clear()
        self.ui_helper.print_header()
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line("    Enter location (optional):")
        self.ui_helper.print_blank_line()
        for location in valid_locations:
            user_input = location[0]
            location_str = location[1]
            final_str = f"{user_input}: {location_str}"
            self.ui_helper.print_line(f"    {final_str}")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_footer()
        user_choice = input("Input: ")
        if user_choice == "":
            return None
        else:
            for location in valid_locations:
                if user_choice == location[0].lower():
                    return location
    

    def show_utilization_report(self, start_date, end_date, location):
        if location == None:
            location = "all locations"
            util_logs = self.logic_api.get_utilization_logs()
        else:
            util_logs = self.logic_api.get_utilization_for_location(location)
        self.ui_helper.clear()
        self.ui_helper.print_header()
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line("    Vehicle uitilization report in:")
        self.ui_helper.print_line(f"    {location}")
        self.ui_helper.print_line(f"    From: {start_date}")
        self.ui_helper.print_line(f"    To:   {end_date}")
        # Let's forget this until logic has done their part >:(
    
# End of utilization section
    

        
    

