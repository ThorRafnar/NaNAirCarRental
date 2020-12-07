from model_layer.destination import Destination

class LocationUI():
    CREATE = "Create new location"
    FIND = "Find a location"
    VIEW_ALL = "View all locations"



    def __init__(self, ui_helper, logic_api, employee_ui, vehicle_ui):
        self.ui_helper = ui_helper
        self.logic_api = logic_api
        self.employee_ui = employee_ui
        self.vehicle_ui = vehicle_ui
        self.options_dict = {
            "1": self.CREATE, 
            "2": self.FIND, 
            "3": self.VIEW_ALL,
        }

    def show_options(self, header_str, error_msg=""):
        ''' Main loop in location ui, displays options and allows user to select a task '''
        options_list = [(k, v) for k, v in self.options_dict.items()]
        while True:
            opt_str = "Select task"

            self.ui_helper.clear()

            self.ui_helper.print_header(header_str)
            self.ui_helper.print_options(options_list, opt_str)
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = self.ui_helper.get_user_menu_choice(options_list)
            if user_choice != None:

                if user_choice.lower() == self.ui_helper.BACK.lower():
                    return

                elif user_choice.lower() == self.ui_helper.QUIT.lower():
                    self.ui_helper.quit_prompt(header_str)

                else:
                    
                    if self.options_dict[user_choice] == self.CREATE:
                        self.create_location(header_str)

                    elif self.options_dict[user_choice] == self.FIND:
                        the_location = self.find_location(header_str)
                        self.single_location_options(the_location, header_str)
                                                                  

                    elif self.options_dict[user_choice] == self.VIEW_ALL:
                        location_list = self.logic_api.get_destinations()
                        self.view_all_locations(location_list, header_str)

            else:
                error_msg = "Please select an option from the menu"


    def view_all_locations(self, location_list,header_str, error_msg = ""):
        ''' Gets all locations and displays them '''
        headers = ["<< COUNTRY >>", "<< CITY >>", "<< PHONE >>", "<< OPENING HOURS >>", "<< IATA >>"]
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.ui_helper.n_columns(headers)
            for location in location_list:
                self.ui_helper.n_columns([location.country, location.airport, location.phone, location.hours, location.iata])
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = input("Input: ")
            if user_choice.lower() == self.ui_helper.QUIT.lower():
                self.ui_helper.quit_prompt(header_str)
            elif user_choice.lower() == self.ui_helper.BACK.lower():
                return
            else:
                return

    def find_location(self, header_str, error_msg=""):
        """ Asks user for airportcode and returns a destination instance """
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.ui_helper.print_line("    Please enter an airport code: ")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            airport_code = input("Input: ")
            
            if airport_code.lower() == self.ui_helper.QUIT.lower():
                self.ui_helper.quit_prompt(header_str)
            elif airport_code.lower() == self.ui_helper.BACK.lower():
                return 
            else:
                the_dest = self.logic_api.find_destination(airport_code.upper())
                if the_dest != None:
                    return the_dest
                else:
                    error_msg = "Please enter a valid airport code!"
                    continue


    def single_location_options(self, the_dest, header_str, error_msg=""):
        ''' Displays a single location and displays options, allows user to select a task '''
        view_staff = "View location's staff"
        view_vehicles = "View location's vehicles"
        opening_hours = "Change opening hours"
        options_dict = {
            "1": view_staff,
            "2": view_vehicles,
            "3": opening_hours
        }
        options_list = self.ui_helper.dict_to_list(options_dict)
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.ui_helper.print_line("Location details:")
            self.display_location(the_dest)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_options(options_list, "Select an option:")
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = self.ui_helper.get_user_menu_choice(options_list)
            if user_choice.lower() == self.ui_helper.BACK.lower():
                return

            elif user_choice.lower() == self.ui_helper.QUIT.lower():
                self.ui_helper.quit_prompt(header_str)
                
            elif user_choice in options_dict:

                if options_dict[user_choice] == view_staff:
                    self.view_location_emps(the_dest, header_str)
                    

                elif options_dict[user_choice] == view_vehicles:
                    self.vehicle_ui.get_all_vehicles(the_dest, header_str)

                elif options_dict[user_choice] == opening_hours:
                    pass

            else:
                error_msg = "Please select an option from the menu"


    def view_location_emps(self, the_dest, header_str):
        filter_attributes = ["work_area", the_dest.iata]
        emps = self.logic_api.get_filtered_employees()
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.print_employee_list(emps)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = self.ui_helper.get_user_menu_choice(options_list)
            if user_choice != None:
                if user_choice.lower() == self.ui_helper.BACK.lower():
                    return

                elif user_choice.lower() == self.ui_helper.QUIT.lower():
                    self.ui_helper.quit_prompt(header_str)
                    
                else:
                    error_msg = "Please select an option from the menu"
            else:
                error_msg = "Please select an option from the menu"


    def create_location(self, header_str, error_msg=""):
        ''' Gets user input for all components of a destination and creates it '''
        iata = input("Input: ")
        the_dest = self.logic_api.find_destination(iata)
        if the_dest == None:
            the_dest = Destination("", "", ".", "", iata)
            the_dest.country = self.get_country(the_dest, header_str)
            the_dest.airport = self.get_city(the_dest, header_str)
            the_dest.phone = self.get_phone(the_dest, header_str)
            the_dest.hours = self.get_hours(the_dest, header_str)
            self.confirm_dest(the_dest, header_str)
        else:
            self.single_location_options(the_dest, header_str)


    def get_country(self, the_dest, header_str, error_msg=""):
        ''' Gets country from user '''
        while True:
            placeholder_text = f"<< Enter country >>"
            setattr(the_dest, "country", placeholder_text)
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.display_location(the_dest)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print()
            return input("Enter location's country: ")


    def get_city(self, the_dest, header_str, error_msg=""):
        ''' Gets city from user '''
        while True:
            placeholder_text = f"<< Enter city >>"
            setattr(the_dest, "airport", placeholder_text)
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.display_location(the_dest)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print()
            return input("Enter location's city: ")

    
    def get_phone(self, the_dest, header_str, error_msg=""):
        ''' gets phone number from user '''
        while True:
            placeholder_text = f"<< Enter phone nr >>"
            setattr(the_dest, "phone", placeholder_text)
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.display_location(the_dest)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print()
            return input("Enter location's phone nr: ")

        
    def get_hours(self, the_dest, header_str, error_msg=""):
        ''' gets phone number from user '''
        while True:
            placeholder_text = f"<< Enter opening hours >>"
            setattr(the_dest, "hours", placeholder_text)
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.display_location(the_dest)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print()
            return input("Enter location's opening hours (HH:MM - HH:MM): ")


    def confirm_dest(self, the_dest, header_str):
        ''' Asks user if they want to save their location/destination '''
        self.ui_helper.clear()
        self.ui_helper.print_header(header_str)
        self.display_location(the_dest)
        self.ui_helper.print_blank_line()
        self.ui_helper.print_footer()
        print("Confirm changes (y/n)?")
        user_choice = input("Input: ")
        if user_choice.lower() in self.ui_helper.YES:
            self.logic_api.create_destination(the_dest)
            return
        else:
            return


    def display_location(self, the_dest):
        ''' Displays locations attributes at the correct indentation '''
        self.ui_helper.print_line(f"    COUNTRY:............{the_dest.country}")
        self.ui_helper.print_line(f"    CITY:...............{the_dest.airport}")
        self.ui_helper.print_line(f"    PHONE:.............{the_dest.phone}")
        self.ui_helper.print_line(f"    OPNENING HOURS:.....{the_dest.hours}")
        self.ui_helper.print_line(f"    IATA:...............{the_dest.iata}")