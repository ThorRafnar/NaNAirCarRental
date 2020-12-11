from model_layer.vehicle import Vehicle
from model_layer.vehicle_type import VehicleType

class VehicleUI():
# Constants
    REGISTER = "Register new vehicle"
    FIND = "Find a vehicle"
    VIEW_ALL = "View all vehicles"
    VEHICLE_RATES = "Vehicle rates"
    AVAILABLE = "View available vehicles"

    def __init__(self, ui_helper, logic_api):
    # Use of logic_api and ui_helper is essential for the program
        self.logic_api = logic_api
        self.ui_helper = ui_helper


# Menu for the vehicle section part   
    def show_options(self, error_msg=""):
        # Available options in vehicle section depends on what kind
        # of employee is the user.
        if self.ui_helper.header_string == "Office Employee":
            options_dict = {
                "1": self.VIEW_ALL,
                "2": self.FIND, 
                "3": self.VEHICLE_RATES,
                "4": self.AVAILABLE
            }
        else:
            options_dict = {
                "1": self.VIEW_ALL,
                "2": self.FIND,
                "3": self.VEHICLE_RATES,
                "4": self.AVAILABLE,
                "5": self.REGISTER
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
                        self.find_vehicle()
                            
                    elif options_dict[user_choice] == self.VIEW_ALL:
                        self.get_all_vehicles()
                    
                    elif options_dict[user_choice] == self.VEHICLE_RATES:
                        self.vehicle_rate_menu()

                    elif options_dict[user_choice] == self.AVAILABLE:
                        self.available_vehicles()

            else:
                error_msg = "Please select an option from the menu"

# Start of list vehicles section
    def get_all_vehicles(self, error_msg=""):
        ''' Gets all vehicles from logic and calls list_vehicles menu, which gets input from user to quit or back'''
        vehicles = self.logic_api.all_vehicles_to_list()
        self.list_vehicles_menu(vehicles)


    def available_vehicles(self, error_msg=""):
        ''' Gets available vehicles from logic, if user is an airport staff, gets vehicles from their location, if office, they have to select a location '''
        if self.ui_helper.user_location.upper() != "KEF":
            location = self.logic_api.find_destination(self.ui_helper.user_location).airport

        else:
            dest = self.ui_helper.get_location("Select a location to view available vehicles:")
            if dest == None:
                return
            else:
                location = self.logic_api.find_destination(dest).airport

        vehicles = self.logic_api.availble_vehicles_by_location(location)
        self.list_vehicles_menu(vehicles)

    
    def list_vehicles_menu(self, vehicles, error_msg=""):
        ''' Shows a list of vehicles '''
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
# End of list section           

# Start of help functions
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
# End of help functions

# Start of new/register vehicle section
    def register_vehicle(self, error_msg=""):
        new_vehicle = Vehicle("", "", "", "rentable", "", "", "", self.ui_helper.user_location, None)
        attribute_list = ["manufacturer", "model", "type", "year", "color", "license_type",]
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
                attr_value = input(f"Input: ")

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
                    if attribute == "type":                                                 #to allow user to create a new vehicle type if they want
                        temp_type = self.logic_api.check_attribute(attr_value, "type")
                        if temp_type != None:
                            new_type = temp_type
                        else:
                            new_type = self.new_type_prompt(attr_value)

                        if new_type == None:
                            return

                        elif new_type.lower() == "no":
                            continue
                        
                        else:
                            new_type =  new_type.capitalize()
                            setattr(new_vehicle, attr_key, new_type)
                            break


                    else:
                        attr_value = self.logic_api.check_attribute(attr_value, attr_key)
                        if attr_value != None:
                            setattr(new_vehicle, attr_key, attr_value)     #Sets attribute to input
                            break   

                        else:                                      #Goes to next value in for loop
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
# End of new/register vehicle section

# Start of find vehicle section
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
                the_vehicle = self.logic_api.find_vehicle(vehicle_id)
                if the_vehicle == None:
                    self.vehicle_not_found()
                self.vehicle_options(the_vehicle)
                return


    def vehicle_options(self, the_vehicle, error_msg=""):
        ''' Views a vehicle and asks user what to do '''
        if self.ui_helper.user_location != "KEF":                                                       #Office staff cant change vehicle status
            opt_change_status = "C"
        else:
            opt_change_status = ""    #bugfix

        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line("    Vehicle details:")
            self.ui_helper.print_blank_line()
            self.view_vehicle_details(the_vehicle)
            if self.ui_helper.user_location != "KEF":                                                   #Office staff cant change vehicle status
                self.ui_helper.print_line(f"    ({opt_change_status})hange: Change Vehicle Status")
            else:
                self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print()
            user_choice = input("Input: ")

            if user_choice.lower() == opt_change_status.lower() and self.ui_helper.user_location != "KEF":  #Office staff cant change vehicle status
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
            "R": "rentable",
            "W": "workshop"
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
                    setattr(a_vehicle, "status", options_dict[user_choice.upper()])
                    confirm_choice = self.confirm_status(a_vehicle)

                    if confirm_choice in self.ui_helper.YES:                                        #Saves changes if input is y or yes, not case sensetive
                        self.logic_api.change_vehicle_condition(a_vehicle.id, a_vehicle.status)
                        return

                    else:
                        return
# End of find vehicle section
                        
# Start of new vehicle type rate section       
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
            available_options.append(("n", "new_type"))
            self.ui_helper.print_blank_line()
            self.ui_helper.print_line(f"    ({new_type.upper()})ew type: Create new vehicle type")
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = self.ui_helper.get_user_menu_choice(available_options)
            options_dict = dict(available_options)
            if user_choice != None:

                if user_choice.lower() == self.ui_helper.BACK:
                    return

                elif user_choice.lower() == self.ui_helper.QUIT:
                    self.ui_helper.quit_prompt()

                elif user_choice.lower() == new_type:
                    self.new_vehicle_type()
                    vehicle_type_list = self.logic_api.get_vehicle_types()   # To refresh list after creating a new one.

                else:
                    the_type = options_dict[user_choice].name
                    the_rate = self.new_vehicle_type_rate()
                    if the_rate == None:
                        continue
                    else:
                        self.logic_api.change_types_rate(the_type, the_rate)
                        vehicle_type_list = self.logic_api.get_vehicle_types()

            else:
                error_msg = "Please select an option from the list"
# End of new vehicle type rate section        

# Start of new vehicle type section    
    def new_vehicle_type(self,error_msg=""):
        ''' Creates a new vehicle type '''
        error_msg = "Please choose an option from the menu."
        while True:
            type_name = self.new_vehicle_type_name()
            if type_name.lower() == self.ui_helper.BACK:
                return
            elif type_name.lower() == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()
            else:
                type_rate = self.new_vehicle_type_rate()
                if type_rate == None:
                    return
                new_vehicle_type = VehicleType(type_name, type_rate)
                user_choice = self.v_type_info_check(new_vehicle_type)
                if user_choice != None:
                    if user_choice.lower() == self.ui_helper.NO:
                        return
                    elif user_choice.lower() == self.ui_helper.BACK:
                        return
                    elif user_choice.lower() == self.ui_helper.QUIT:
                        self.ui_helper.quit_prompt()
                    elif user_choice.lower() in self.ui_helper.YES:
                        self.logic_api.create_new_type(new_vehicle_type)
                        return
                    else:
                        return
                else:
                    error_msg = "Please choose an option from the menu."
                    return


    def new_vehicle_type_name(self):
        self.ui_helper.clear()
        self.ui_helper.print_header()
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line("    Enter a new vehicle type name:")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_hash_line()
        user_choice = input("Input: ")
        return user_choice
    

    def new_vehicle_type_rate(self,error_msg=""):
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_blank_line()
            self.ui_helper.print_line("    Enter a new rate for the vehicle type:")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = input("Input: ")
            if user_choice.lower() == self.ui_helper.BACK:
                return
            elif user_choice.lower() == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()
            else:
                user_choice = self.logic_api.check_if_only_number(user_choice)
                if user_choice != None:
                    return user_choice
                else:
                    error_msg = "Please input a fee containing only numbers."
                    continue
    

    def v_type_info_check(self, vehicle_type):
        self.ui_helper.clear()
        self.ui_helper.print_header()
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line("    Is this information correct? (y/n)")
        self.ui_helper.print_blank_line()
        v_type = vehicle_type.name
        v_rate = vehicle_type.rate
        self.ui_helper.print_line("    {:.<36}{}".format(v_type, v_rate))
        self.ui_helper.print_blank_line()
        self.ui_helper.print_hash_line()
        print()
        user_choice = input("Input: ")
        return user_choice


    def new_type_prompt(self, type_name, error_msg=""):
        ''' Informs user that type doesnt exist, asks if they want to create one, returning the type name if they do and none if they don't '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line(f"Vehicle type: {type_name} doesn't exist, do you want to create it (y/n)")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = input("Input: ")
            if user_choice.lower() in self.ui_helper.YES:

                while True:
                    type_rate = self.new_vehicle_type_rate()
                    if type_rate == None:
                        return
                    new_vehicle_type = VehicleType(type_name, type_rate)
                    user_choice = self.v_type_info_check(new_vehicle_type)
                    if user_choice != None:
                        if user_choice.lower() == self.ui_helper.BACK:
                            return 

                        elif user_choice.lower() == self.ui_helper.QUIT:
                            self.ui_helper.quit_prompt()

                        elif user_choice.lower() in self.ui_helper.YES:
                            self.logic_api.create_new_type(new_vehicle_type)
                            return new_vehicle_type.name

                        else:
                            return
                    else:
                        error_msg = "Please choose an option from the menu."
                    
            elif user_choice.lower() == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()
                continue

            elif user_choice.lower() in self.ui_helper.NO:  #If user doesnt want to create
                return "no"
            
            else:
                return None
# End of new vehicle type section
