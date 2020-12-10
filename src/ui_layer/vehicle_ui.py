from model_layer.vehicle import Vehicle
from model_layer.vehicle_type import VehicleType

class VehicleUI():
    REGISTER = "Register new vehicle"
    FIND = "Find a vehicle"
    VIEW_ALL = "View all vehicles"
    VEHICLE_RATES = "Vehicle rates"

    def __init__(self, ui_helper, logic_api):
        self.logic_api = logic_api
        self.ui_helper = ui_helper


    
    def show_options(self, error_msg=""):

        if self.ui_helper.header_string == "Office Employee":
            options_dict = {
                "1": self.VIEW_ALL,
                "2": self.FIND, 
                "3": self.VEHICLE_RATES
            }
        else:
            options_dict = {
                "1": self.VIEW_ALL,
                "2": self.FIND,
                "3": self.VEHICLE_RATES,
                "4": self.REGISTER               
            }

        options_list = self.ui_helper.dict_to_list(options_dict)

        while True:
            opt_str = "Select task"

            self.ui_helper.clear()

            self.ui_helper.print_header()
            self.ui_helper.print_options(options_list, opt_str)
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = self.ui_helper.get_user_menu_choice(options_list)
            if user_choice != None:

                if user_choice.lower() == self.ui_helper.BACK:
                    return

                elif user_choice.lower() == self.ui_helper.QUIT:
                    self.ui_helper.quit_prompt()

                else:
                    
                    if options_dict[user_choice] == self.REGISTER:
                        self.register_vehicle()
                        

                    elif options_dict[user_choice] == self.FIND:

                        while True:
                            the_vehicle = self.find_vehicle()
                            if the_vehicle != None:
                                self.vehicle_options(the_vehicle)
                                break
                            else:
                                self.vehicle_not_found()
                                continue
                            
                    elif options_dict[user_choice] == self.VIEW_ALL:
                        self.get_all_vehicles()
                    
                    elif options_dict[user_choice] == self.VEHICLE_RATES:
                        self.vehicle_rate_menu()

            else:
                error_msg = "Please select an option from the menu"


    def get_all_vehicles(self, error_msg=""):
        ''' Gets all vehicles from logic and calls print_vehicle_list, gets input from user to quit or back'''
        vehicles = self.logic_api.all_vehicles_to_list()
        vehicle_dict = {vehicle.id: vehicle for vehicle in vehicles }               #Allows user to select a vehicle id from the list
        vehicle_list = self.ui_helper.dict_to_list(vehicle_dict)
        while True:            
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line("Vehicle overview, enter vehicle id to view")
            self.ui_helper.print_blank_line()
            self.print_vehicle_list(vehicles)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = self.ui_helper.get_user_menu_choice(vehicle_list)
            if user_choice != None:                                 #If user input a valid option, ie back or quit

                if user_choice.lower() == self.ui_helper.BACK:
                    return

                elif user_choice.lower() == self.ui_helper.QUIT:
                    self.ui_helper.quit_prompt()

                else:
                    self.vehicle_options(vehicle_dict[user_choice])

            else:
                error_msg = f"Please enter a valid vehicle ID, or {self.ui_helper.QUIT.upper()} to quit and {self.ui_helper.BACK.upper()} to go back"
            

    def vehicle_not_found(self):
        ''' Informs user that no vehicle was found, and to press enter to return'''
        self.ui_helper.clear()
        self.ui_helper.print_header()
        self.ui_helper.print_line("    No vehicle with this ID number found!")
        self.ui_helper.print_line("    Press enter to try again")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_footer()
        print()
        _user_choice = input("Input: ")

        
    def print_vehicle_list(self, vehicle_list):
        ''' Prints vehicle attributes as columns, including a header '''
        manu_str = "<< MANUFACTURER >>"
        model_str = "<< MODEL >>"
        type_str = "<< TYPE >>"
        year_str = "<< YEAR >>"
        color_str = "<< COLOR >>"
        status_str = "<< STATUS >>"
        licence_str = "<< LICENCE >>"
        location_str = "<< LOCATION >>"
        id_str = "<< ID >>"
        self.ui_helper.n_columns([id_str, manu_str, model_str, type_str, year_str, color_str, status_str, licence_str, location_str])

        for vehicle in vehicle_list:
            manu = vehicle.manufacturer
            model = vehicle.model
            vtype = vehicle.type
            year = vehicle.year
            color = vehicle.color
            status = vehicle.status
            licence = vehicle.license_type
            location = vehicle.location
            id_nr = vehicle.id
            self.ui_helper.n_columns([id_nr, manu, model, vtype, year, color, status, licence, location])


    def register_vehicle(self, error_msg=""):
        new_vehicle = Vehicle("", "", "", "OK", "", "", "", "", None)
        attribute_list = ["manufacturer", "model", "type", "year", "color", "license_type", "location"]
        for attribute in attribute_list:
            while True:                                           #To make back and quit options functional
                attr_key = attribute.replace(" ", "_")
                placeholder_text = f"<< Enter {attribute} >>"
                setattr(new_vehicle, attr_key, placeholder_text)
                self.ui_helper.clear()
                self.ui_helper.print_header()
                self.view_vehicle_details(new_vehicle)
                self.ui_helper.print_blank_line()
                self.ui_helper.print_footer()
                print(error_msg)
                attr_value = input(f"Enter vehicles's {attribute}: ")

                if attr_value.lower() == self.ui_helper.BACK.lower():
                    back_choice = self.unsaved_changes(new_vehicle)
                    if back_choice.lower() in self.ui_helper.YES:
                        return
                    else:
                        continue

                elif attr_value.lower() == self.ui_helper.QUIT:
                    self.ui_helper.quit_prompt()
                    continue

                else:
                    attr_value = self.logic_api.check_attribute(attr_value, attr_key)
                    if attr_value != None:
                        setattr(new_vehicle, attr_key, attr_value)     #Sets attribute to input
                        break                                          #Goes to next value in for loop

                    else:
                        error_msg = f"Please enter a valid {attribute}"
            
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line("Confirm new vehicle? (y/n)")
            self.view_vehicle_details(new_vehicle)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print()
            user_choice = input("Input: ")
            if user_choice in self.ui_helper.YES:
                self.logic_api.register_new_vehicle(new_vehicle)
                return

            elif user_choice.lower() == self.ui_helper.BACK:
                back_choice = self.unsaved_changes(new_vehicle)

                if back_choice in self.ui_helper.YES:
                    return
                else:
                    continue

            elif user_choice.lower() == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()

            else:
                error_msg = "Please select an option, or enter 9 to quit and 0 to go back"


    def find_vehicle(self):
        ''' takes vehicle id number from user and finds the vehicle, or none if it doesn't exist '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line("    Enter vehicle ID number")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print()
            vehicle_id = input("Input: ")
            if vehicle_id.lower() == self.ui_helper.BACK:
                return 
            elif vehicle_id.lower() == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt() 

            else:   #Search for the vehicle in database
                return self.logic_api.find_vehicle(vehicle_id)


    def vehicle_options(self, the_vehicle, error_msg=""):
        ''' Views a vehicle and asks user what to do '''
        opt_change_status = "1"
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line("    Vehicle details:")
            self.ui_helper.print_blank_line()
            self.view_vehicle_details(the_vehicle)
            self.ui_helper.print_line(f"    {opt_change_status}. Change Vehicle Status")
            self.ui_helper.print_footer()
            print()
            user_choice = input("Input: ")

            if user_choice == opt_change_status:
                self.change_vehicle_status(the_vehicle)

            elif user_choice.lower() == self.ui_helper.BACK:
                return

            elif user_choice.lower() == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()

            else:
                error_msg = f"Please select an option, or enter {self.ui_helper.QUIT.upper()} to quit and {self.ui_helper.BACK.upper()} to go back"


    def view_vehicle_details(self, a_vehicle):
        ''' Shows all attributes of a vehicle '''
        self.ui_helper.print_line(f"        MANUFACTURER:............{a_vehicle.manufacturer}")
        self.ui_helper.print_line(f"        MODEL:...................{a_vehicle.model}")
        self.ui_helper.print_line(f"        VEHICLE TYPE:............{a_vehicle.type}")
        self.ui_helper.print_line(f"        MODEL YEAR:..............{a_vehicle.year}")
        self.ui_helper.print_line(f"        COLOR:...................{a_vehicle.color}")
        self.ui_helper.print_line(f"        STATUS:..................{a_vehicle.status}")
        self.ui_helper.print_line(f"        LICENCE REQUIREMENTS:....{a_vehicle.license_type}")
        self.ui_helper.print_line(f"        LOCATION:................{a_vehicle.location}")
        if a_vehicle.id != None:
            self.ui_helper.print_line(f"        ID NUMBER:...............{a_vehicle.id}")
        else:
            self.ui_helper.print_blank_line()
        self.ui_helper.print_blank_line()

    
    def unsaved_changes(self, a_vehicle):
        ''' Asks user if they want to go back without saving their changes '''
        self.ui_helper.clear()
        self.ui_helper.print_header()
        self.view_vehicle_details(a_vehicle)
        self.ui_helper.unsaved_prompt()
        self.ui_helper.print_blank_line()
        self.ui_helper.print_hash_line()
        print()
        return input("Input: ")
    

    def change_vehicle_status(self, a_vehicle, error_msg=""):
        ''' Asks user what to change vehicle status to and changes it '''

        options_dict = {
            "1": "rentable",
            "2": "workshop"
        }
        options_list = self.ui_helper.dict_to_list(options_dict)
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            opt_str = "    What do you want to change the vehicle status to?"
            self.ui_helper.print_options(options_list, opt_str)
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = self.ui_helper.get_user_menu_choice(options_list)
            if user_choice == None:
                error_msg = "Please select an option from the menu"
            else:
                if user_choice.lower() == self.ui_helper.BACK:
                    return

                elif user_choice.lower() == self.ui_helper.QUIT:
                    self.ui_helper.quit_prompt()

                elif user_choice in options_dict:
                    setattr(a_vehicle, "status", options_dict[user_choice])
                    confirm_choice = self.confirm_status(a_vehicle)

                    if confirm_choice in self.ui_helper.YES:                                        #Saves changes if input is y or yes, not case sensetive
                        self.logic_api.change_vehicle_condition(a_vehicle.id, a_vehicle.status)
                        return

                    else:
                        return
                        
            
    def confirm_status(self, a_vehicle):
        ''' Asks user to confirm new status, returning the user input '''
        self.ui_helper.clear()
        self.ui_helper.print_header()
        self.view_vehicle_details(a_vehicle)
        self.ui_helper.print_line("    Do you want to confirm these changes? (y/n)")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_hash_line()
        print()
        return input("Input: ")
    

    def vehicle_rate_menu(self, error_msg=""):
        ''' The vehicle type rate menu, shows all available vehicle types'''
        vehicle_type_list = self.logic_api.get_vehicle_types()
        available_options = []
        new_type = "n"
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line("Select vehicle type to change rate")
            self.ui_helper.print_blank_line()
            for ind, vehicle_type in enumerate(vehicle_type_list):
                available_options.append((str(ind + 1), vehicle_type))
                v_type = vehicle_type.name
                v_rate = vehicle_type.rate
                self.ui_helper.print_line("{: >3}.  {:.<32}{}".format(str(ind + 1), v_type, v_rate))
            self.ui_helper.print_blank_line()
            self.ui_helper.print_line(f"    ({new_type.upper()})ew type: Create new vehicle type")
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = self.ui_helper.get_user_menu_choice(available_options)
            if user_choice != None:

                if user_choice.lower() == self.ui_helper.BACK:
                    return

                elif user_choice.lower() == self.ui_helper.QUIT:
                    self.ui_helper.quit_prompt()

                elif user_choice.lower() == new_type:
                    pass

            else:
                error_msg = "Please select an option from the list"
        
    
    def change_vehicle_type_rate(self, id_str):
        ''' Takes in a vehicle type id and changes the rate for 
        that particular vehicle type.'''
        # TODO Change this function, on hold.
        vehicle_type_str = " << TYPE >>"
        vehicle_region_str = " << REGION >>"
        vehicle_rate_str = " << RATE >>"
        # Remember to change this line
        vehicle_type_list = self.logic_api.get_vehicle_types()
        #
        self.ui_helper.clear()
        self.ui_helper.print_header()
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line("    Enter a new rate for this particular vehicle type:")
        self.ui_helper.print_blank_line()
        self.ui_helper.n_columns([vehicle_type_str, vehicle_region_str, vehicle_rate_str])
        for vehicle_type in vehicle_type_list:
            v_type = vehicle_type.name
            v_region = vehicle_type.regions
            v_rate = vehicle_type.rate
            self.ui_helper.n_columns([v_type, v_region, v_rate])
        self.ui_helper.print_blank_line()
        self.ui_helper.print_footer()

