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
    def reports_menu(self):
        ''' Shows the option menu from the reports section'''
        user_choice = ReportUI.show_options(self)
        while True:
            if self.options_dict[user_choice].lower() == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()

            elif self.options_dict[user_choice].lower() == self.ui_helper.BACK:
                return

            else:
                if self.options_dict[user_choice] == self.PROFIT_REPORTS:
                    # Call a function wich deals with profit reports
                    pass

                elif self.options_dict[user_choice] == self.UTILIZATION_REPORTS:
                    start_date, end_date = ReportUI.ask_end_and_start_date(self)
                    location = ReportUI.ask_location(self)
                    ReportUI.show_utilization_report(self, start_date, end_date,location)
                    pass

                elif self.options_dict[user_choice] == self.BILLS:
                    # Call a function wich deals with bills.
                    pass

    
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
        return input("Input: ")
# End of menu section

# Start of profit section
    def show_profit_reports(self):
        self.ui_helper.clear()
        self.ui_helper.print_header()
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line("    Profit Reports:")
        pass
        # Call a function wich calculates the profit report

# End on profit section


# Start of utilization section
    def ask_end_and_start_date(self):
        self.ui_helper.clear()
        self.ui_helper.print_header()
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line("    Enter start date: (dd/mm/yyyy)")
        self.ui_helper.print_line("    Enter end date: (dd/mm/yyyy)")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_footer()
        start_date = input("Input: ")
        end_date = input("Input: ")
        return start_date, end_date
    
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
                if user_choice == location[0]:
                    return location
    

    def show_utilization_report(self, start_date, end_date, location):
        all_vehicle_types = self.logic_api.get_vehicle_types()
        if location == None:
            location = "all locations"
        self.ui_helper.clear()
        self.ui_helper.print_header()
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line("    Vehicle uitilization report in:")
        self.ui_helper.print_line(f"    {location}")
        self.ui_helper.print_line(f"    From: {start_date}")
        self.ui_helper.print_line(f"    To:   {end_date}")
        # Let's forget this until logic has done their part >:(
    
# End of utilization section
    

        
    

