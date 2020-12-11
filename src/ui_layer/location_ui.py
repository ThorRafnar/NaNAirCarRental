from model_layer.destination import Destination

class LocationUI():
    # Constants
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

# Menu section for locations
    def show_options(self, error_msg=""):
        ''' Main loop in location ui, displays options and allows user to select a task '''
        options_list = self.ui_helper.dict_to_list(self.options_dict)
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_options(options_list, "Select task")
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = self.ui_helper.get_user_menu_choice(options_list)
            if user_choice != None:

                if user_choice.lower() == self.ui_helper.BACK:
                    return

                elif user_choice.lower() == self.ui_helper.QUIT:
                    self.ui_helper.quit_prompt()

                else:
                    
                    if self.options_dict[user_choice] == self.CREATE:
                        self.new_location()

                    elif self.options_dict[user_choice] == self.FIND:
                        self.find_location()                                                                  

                    elif self.options_dict[user_choice] == self.VIEW_ALL:
                        location_list = self.logic_api.get_destinations()
                        self.view_location_list(location_list)

            else:
                error_msg = "Please select an option from the menu"
# End of menu section

# Start of new location option section

    def new_location(self, error_msg=""):
        ''' Gets user input for all components of a destination and creates it, if it exists, shows the location's menu '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line("    Enter airport code (IATA)")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            iata = input("Input: ")

            if iata.lower() == self.ui_helper.BACK:
                return

            elif iata.lower() == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()

            iata = self.logic_api.check_iata(iata)
            if iata == None:
                error_msg = "Please enter a valid IATA code (e.g. AEY / KEF)"
                continue
            elif iata == "1":
                error_msg = "This IATA code already exists"
                continue
                
            else:
                iata = iata.upper()
                the_dest = self.logic_api.find_destination(iata)
                if the_dest == None: 
                    self.create_location(iata)
                    return

                else:
                    self.single_location_options(the_dest)
                    return


    def create_location(self, iata, error_msg=""):
        ''' Creates a new location with an airport code '''
        the_dest = Destination("", "", ".", "", iata)
        the_dest.country = self.get_country(the_dest)
        if the_dest.country == None:
            return

        the_dest.airport = self.get_city(the_dest)
        if the_dest.airport == None:
            return

        the_dest.phone = self.get_phone(the_dest)
        if the_dest.phone == None:
            return

        the_dest.hours = self.get_hours(the_dest)
        if the_dest.hours == None:
            return

        self.confirm_dest(the_dest)
    

    def confirm_dest(self, the_dest):
        ''' Asks user if they want to save their location/destination '''
        self.ui_helper.clear()
        self.ui_helper.print_header()
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


# End of new location section

# Start of find location section

    def find_location(self, error_msg=""):
        """ Asks user for airportcode and returns a destination instance """
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line("    Please enter an airport code: ")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            airport_code = input("Input: ")            
            if airport_code.lower() == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()

            elif airport_code.lower() == self.ui_helper.BACK:
                return 
 
            else:
                the_dest = self.logic_api.find_destination(airport_code.upper())
                if the_dest != None:
                    self.single_location_options(the_dest)
                    return

                else:
                    airport_code = self.logic_api.check_iata(airport_code)
                    if airport_code == None:
                        error_msg = "Please enter a valid IATA (eg. AEY, KEF)"
                        continue

                    else:
                        self.no_thing_found(airport_code)
                        return
    

    def no_thing_found(self, iata, error_msg =""):
        ''' Informs user that no location was found, and asks if they want to create one '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line(f"    No location {iata} found, do you wish to create it? (y/n)")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_hash_line()
            print(error_msg)
            user_choice = input("Input: ")
            if user_choice.lower() in self.ui_helper.YES:
                self.create_location(iata)  # This function is in new location section
                return

            else:
                return

# End of find location section

# Start of view all locations section

    def view_location_list(self, location_list, error_msg = ""):
        ''' Displays a list of locations, allows user to enter iata to view more '''
        headers = ["<< COUNTRY >>", "<< CITY >>", "<< PHONE >>", "<< OPENING HOURS >>", "<< IATA >>"]
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.n_columns(headers)
            for location in location_list:
                self.ui_helper.n_columns([location.country, location.airport, location.phone, location.hours, location.iata])
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = input("Input: ")
            if user_choice.lower() == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()

            elif user_choice.lower() == self.ui_helper.BACK:
                return

            else:
                error_msg = f"Please enter {self.ui_helper.QUIT.upper()} to quit or {self.ui_helper.BACK.upper()} to go back"

# End of view all locations section


# Functions that print out in some way locations // Besides view_location_list function

    def single_location_options(self, the_dest, error_msg=""):
        ''' Displays a single location and displays options, allows user to select a task '''
        view_staff = "View location's staff"
        view_vehicles = "View location's vehicles"
        options_dict = {
            "1": view_staff,
            "2": view_vehicles,
        }
        options_list = self.ui_helper.dict_to_list(options_dict)
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line("Location details:")
            self.display_location(the_dest)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_options(options_list, "Select an option:")
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = self.ui_helper.get_user_menu_choice(options_list)
            if user_choice != None:

                if user_choice.lower() == self.ui_helper.BACK:
                    return

                elif user_choice.lower() == self.ui_helper.QUIT:
                    self.ui_helper.quit_prompt()
                    
                else:

                    if options_dict[user_choice] == view_staff:
                        self.view_location_emps(the_dest)
                        

                    elif options_dict[user_choice] == view_vehicles:
                        self.display_location_vehicles(the_dest)

            else:
                error_msg = "Please select an option from the menu"


    def display_location_vehicles(self, location, error_msg =""):
        ''' Gets all vehicles in a given location and prints them out '''
        vehicle_list = self.logic_api.get_vehicle_by_location(location.airport)
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line(f"Vehicles in {location.airport}, {location.country}")
            self.ui_helper.print_blank_line()
            self.vehicle_ui.print_vehicle_list(vehicle_list)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = input("Input: ")
            if user_choice.lower() == self.ui_helper.BACK:
                return

            elif user_choice.lower() == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()
                
            else: 
                error_msg = f"Please enter {self.ui_helper.QUIT.upper()} to quit or {self.ui_helper.BACK.upper()} to go back"


    def view_location_emps(self, the_dest, error_msg=""):
        ''' Shows the location's employees, if any '''
        filter_attributes = [("work_area", the_dest.iata)]
        emps = self.logic_api.get_filtered_employees(filter_attributes)
        if len(emps) > 0:
            while True:
                self.ui_helper.clear()
                self.ui_helper.print_header()
                self.employee_ui.print_employee_list(emps)
                self.ui_helper.print_blank_line()
                self.ui_helper.print_footer()
                print(error_msg)
                user_choice = self.ui_helper.get_user_menu_choice()
                if user_choice != None:
                    if user_choice.lower() == self.ui_helper.BACK:
                        return

                    elif user_choice.lower() == self.ui_helper.QUIT:
                        self.ui_helper.quit_prompt()
                        
                    else:
                        error_msg = "Please select an option from the menu"
                else:
                    error_msg = "Please select an option from the menu"
        else:
            self.no_employees()
    

    def display_location(self, the_dest):
        ''' Displays locations attributes at the correct indentation '''
        self.ui_helper.print_line(f"    COUNTRY:............{the_dest.country}")
        self.ui_helper.print_line(f"    CITY:...............{the_dest.airport}")
        self.ui_helper.print_line(f"    PHONE:.............{the_dest.phone}")
        self.ui_helper.print_line(f"    OPNENING HOURS:.....{the_dest.hours}")
        self.ui_helper.print_line(f"    IATA:...............{the_dest.iata}")
# End of printing funcitons


# Helper function section

    def no_employees(self):
        ''' Informs user that no employees were found, enter to return '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line(f"    No employees found, press enter to return")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_hash_line()
            print()
            _x = input("Input: ")
            return 


    def get_country(self, the_dest, error_msg=""):
        ''' Gets country from user '''
        while True:
            placeholder_text = f"<< Enter country >>"
            setattr(the_dest, "country", placeholder_text)
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.display_location(the_dest)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            country = input("Enter location's country: ")
            if country.lower() == self.ui_helper.BACK:
                return

            elif country.lower() == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()
                
            else:
                return country.capitalize()


    def get_city(self, the_dest, error_msg=""):
        ''' Gets city from user '''
        while True:
            placeholder_text = f"<< Enter city >>"
            setattr(the_dest, "airport", placeholder_text)
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.display_location(the_dest)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print()
            city = input("Enter location's city: ")
            if city.lower() == self.ui_helper.BACK:
                return

            elif city.lower() == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()
                
            else:
                return city.capitalize()

    
    def get_phone(self, the_dest, error_msg=""):
        ''' gets phone number from user '''
        while True:
            placeholder_text = f"<< Enter phone nr >>"
            setattr(the_dest, "phone", placeholder_text)
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.display_location(the_dest)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print()
            phone_nr =  input("Enter location's phone nr: ")
            if phone_nr.lower() == self.ui_helper.BACK:
                return

            elif phone_nr.lower() == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()
                
            else:
                phone_nr = self.logic_api.check_phone(phone_nr)
                if phone_nr != None:
                    return phone_nr
                
                else:
                    error_msg = "Please enter a valid phone number"

        
    def get_hours(self, the_dest, error_msg=""):
        ''' gets phone number from user '''
        while True:
            placeholder_text = f"<< Enter opening hours >>"
            setattr(the_dest, "hours", placeholder_text)
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.display_location(the_dest)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            hours = input("Enter location's opening hours (HH:MM - HH:MM): ")
            if hours.lower() == self.ui_helper.BACK:
                return

            elif hours.lower() == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()
                
            else:
                hours = self.logic_api.check_hours(hours)
                if hours != None:
                    return hours
                
                else:
                    error_msg = "Please enter opening hours in a valid format, eg. 08:15 - 12:30"

# End of helper functions section


