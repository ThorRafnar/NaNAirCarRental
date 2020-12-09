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

        
    def get_date(self, a_str):
        ''' gets a date from user and error checks it '''
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
    def uitilization_menu(self):
        location = self.get_location()
        if location != None:
            self.show_utilization_report(location)
            
        else:
            return


    def get_location(self, error_msg=""):
        ''' Gets a location from user, allowing only valid existing locations '''
        valid_locations = self.logic_api.destinations_option_list()
        valid_locations.append(("ALL", "All locations"))
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_blank_line()
            self.ui_helper.print_line("    Select location for utilization report:")
            for iata, location in valid_locations:
                if iata != "ADM" and iata != "KEF":
                    self.ui_helper.print_line(f"    {iata}: {location}")
                else:
                    valid_locations.remove((iata, location))
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            user_choice = self.ui_helper.get_user_menu_choice(valid_locations)
            if user_choice != None:

                if user_choice.lower() == self.ui_helper.QUIT:
                    self.ui_helper.quit_prompt()

                elif user_choice.lower() == self.ui_helper.BACK:
                    return

                else:
                    return user_choice

            else:
                error_msg = "Please select an option from the menu"
    

    def show_utilization_report(self, location):
        ''' Shows utilization reports per vehicle for either all locations or just one'''
        padding = 48
        scale_length = 50
        if location == "All":
            #util_logs = self.logic_api.get_utilization_logs()
            pass
        else:
            util_logs = {
                "Medium road" : [ ["1", "TAILIG free fly II", "05/07/2019", "07/12/2020", 70] ]
            }
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_blank_line()
            self.ui_helper.print_centered_line_dash("<< VEHICLE UTILIZATION >>---------------")
            self.ui_helper.print_blank_line()
            for vehicle_type, values in util_logs.items():
                self.ui_helper.print_line(vehicle_type.upper())
                self.ui_helper.print_line(" " * padding + "_" * scale_length)
                for vehicle in values:
                    vehicle_id = vehicle[0]
                    vehicle_name = vehicle[1]
                    first_use_date = vehicle[2]
                    recent_use_date = vehicle[3]
                    percent = vehicle[4]
                    ratio = percent // 2
                    info_str = f"{vehicle_id} {vehicle_name} {first_use_date} {recent_use_date}"
                    info_string = "{: <{width}}".format(info_str, width = padding)
                    percent_string = ("|" + "#" * ratio + " " * (scale_length - ratio) + f"| {str(percent)} %")
                    self.ui_helper.print_line(f"{info_string}{percent_string}")

            return input("...")



