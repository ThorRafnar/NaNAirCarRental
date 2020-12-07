from model_layer.vehicle import Vehicle
from model_layer.vehicle_type import VehicleType

class VehicleUI():

    REGISTER = "Register new vehicle"
    FIND = "Find a vehicle"
    VIEW_ALL = "View all vehicles"

    def __init__(self, ui_helper, logic_api):
        self.logic_api = logic_api
        self.ui_helper = ui_helper
        self.options_dict = {
            "1": self.REGISTER, 
            "2": self.FIND, 
            "3": self.VIEW_ALL,
        }

    
    def show_options(self, header_str, error_msg=""):
        options_list = self.ui_helper.dict_to_list(self.options_dict)

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
                    
                    if self.options_dict[user_choice] == self.REGISTER:
                        self.register_vehicle(header_str)
                        

                    elif self.options_dict[user_choice] == self.FIND:

                        while True:
                            the_vehicle = self.find_vehicle(header_str)
                            if the_vehicle != None:
                                self.vehicle_options(the_vehicle, header_str)
                                break
                            else:
                                self.vehicle_not_found(header_str)
                                continue
                            
                                               

                    elif self.options_dict[user_choice] == self.VIEW_ALL:
                        self.get_all_vehicles(header_str)
            else:
                error_msg = "Please select an option from the menu"


    def get_all_vehicles(self, header_str, error_msg=""):
        ''' Gets all vehicles from logic and calls print_vehicle_list, gets input from user to quit or back'''
        while True:
            options_list = []
            vehicles = self.logic_api.all_vehicles_to_list()
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.ui_helper.print_line("Vehicle overview:")
            self.ui_helper.print_blank_line()
            self.print_vehicle_list(vehicles)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = self.ui_helper.get_user_menu_choice(options_list)
            if user_choice.lower() == self.ui_helper.BACK.lower():
                return

            elif user_choice.lower() == self.ui_helper.QUIT.lower():
                self.ui_helper.quit_prompt(header_str)
            else:
                error_msg = "Please select an option, or enter 9 to quit and 0 to go back"
            

    def vehicle_not_found(self, header_str):
        ''' '''
        self.ui_helper.clear()
        self.ui_helper.print_header(header_str)
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
            licence = vehicle.licence_type
            location = vehicle.location
            id_nr = vehicle.id
            self.ui_helper.n_columns([id_nr, manu, model, vtype, year, color, status, licence, location])


    def register_vehicle(self, header_str, error_msg=""):
        new_vehicle = Vehicle("", "", "", "OK", "", "", "", "", None)
        attribute_list = ["manufacturer", "model", "type", "year", "color", "licence_type", "location"]
        for attribute in attribute_list:
            while True:                                           #To make back and quit options functional
                attr_key = attribute.replace(" ", "_")
                placeholder_text = f"<< Enter {attribute} >>"
                setattr(new_vehicle, attr_key, placeholder_text)
                self.ui_helper.clear()
                self.ui_helper.print_header(header_str)
                self.view_vehicle_details(new_vehicle)
                self.ui_helper.print_blank_line()
                self.ui_helper.print_footer()
                print()
                attr_value = input(f"Enter vehicles's {attribute}: ")

                if attr_value.lower() == self.ui_helper.BACK.lower():
                    back_choice = self.unsaved_changes(new_vehicle, header_str)
                    if back_choice.lower() in self.ui_helper.YES:
                        return
                    else:
                        continue

                elif attr_value.lower() == self.ui_helper.QUIT.lower():
                    self.ui_helper.quit_prompt(header_str)
                    continue

                else:
                    setattr(new_vehicle, attr_key, attr_value)     #Sets attribute to input
                    break                                          #Goes to next value in for loop
            
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.ui_helper.print_line("Confirm new vehicle? (y/n)")
            self.view_vehicle_details(new_vehicle)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print()
            user_choice = input("Input: ")
            if user_choice in self.ui_helper.YES:
                self.logic_api.register_new_vehicle(new_vehicle)
                return

            elif user_choice.lower() == self.ui_helper.BACK.lower():
                back_choice = self.unsaved_changes(new_vehicle, header_str)

                if back_choice in self.ui_helper.YES:
                    return
                else:
                    continue

            elif user_choice.lower() == self.ui_helper.QUIT.lower():
                self.ui_helper.quit_prompt(header_str)

            else:
                error_msg = "Please select an option, or enter 9 to quit and 0 to go back"


    def find_vehicle(self, header_str, error_msg=""):
        ''' takes vehicle id number from user and finds the vehicle, or none if it doesn't exist '''
        
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.ui_helper.print_line("    Enter vehicle ID number")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            vehicle_id = input("Input: ")
            if vehicle_id.lower() == self.ui_helper.BACK.lower():
                return 
            elif vehicle_id.lower() == self.ui_helper.QUIT.lower():
                self.ui_helper.quit_prompt(header_str) 

            else:   #Search for the vehicle in database
                return self.logic_api.find_vehicle(vehicle_id)


    def vehicle_options(self, the_vehicle, header_str, error_msg=""):
        ''' Views a vehicle and asks user what to do '''
        opt_change_status = "1"
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.ui_helper.print_line("    Vehicle details:")
            self.ui_helper.print_blank_line()
            self.view_vehicle_details(the_vehicle)
            self.ui_helper.print_line(f"    {opt_change_status}. Change Vehicle Status")
            self.ui_helper.print_footer()
            print()
            user_choice = input("Input: ")
            if user_choice == opt_change_status:
                self.change_vehicle_status(the_vehicle, header_str)
            elif user_choice.lower() == self.ui_helper.BACK.lower():
                return
            elif user_choice.lower() == self.ui_helper.QUIT.lower():
                self.ui_helper.quit_prompt(header_str)
            else:
                error_msg = "Please select an option, or enter 9 to quit and 0 to go back"


    def view_vehicle_details(self, a_vehicle):
        ''' Shows all attributes of a vehicle '''
        self.ui_helper.print_line(f"        MANUFACTURER:............{a_vehicle.manufacturer}")
        self.ui_helper.print_line(f"        MODEL:...................{a_vehicle.model}")
        self.ui_helper.print_line(f"        VEHICLE TYPE:............{a_vehicle.type}")
        self.ui_helper.print_line(f"        MODEL YEAR:..............{a_vehicle.year}")
        self.ui_helper.print_line(f"        COLOR:...................{a_vehicle.color}")
        self.ui_helper.print_line(f"        STATUS:..................{a_vehicle.status}")
        self.ui_helper.print_line(f"        LICENCE REQUIREMENTS:....{a_vehicle.licence_type}")
        self.ui_helper.print_line(f"        LOCATION:................{a_vehicle.location}")
        if a_vehicle.id != None:
            self.ui_helper.print_line(f"        ID NUMBER:...............{a_vehicle.id}")
        else:
            self.ui_helper.print_blank_line()
        self.ui_helper.print_blank_line()

    
    def unsaved_changes(self, a_vehicle, header_str):
        ''' Asks user if they want to go back without saving their changes '''
        self.ui_helper.clear()
        self.ui_helper.print_header(header_str)
        self.view_vehicle_details(a_vehicle)
        self.ui_helper.unsaved_prompt()
        self.ui_helper.print_blank_line()
        self.ui_helper.print_hash_line()
        print()
        return input("Input: ")
    

    def change_vehicle_status(self, a_vehicle, header_str, error_msg=""):
        ''' Asks user what to change vehicle status to and changes it '''
        options_dict = {
            "1": "Rentable",
            "2": "In workshop"
        }
        options_list = [(k, v) for k, v in options_dict.items()]
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            opt_str = "    What do you want to change the vehicle status to?"
            self.ui_helper.print_options(options_list, opt_str)
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = self.ui_helper.get_user_menu_choice(options_list)
            if user_choice == None:
                error_msg = "Please select an option from the menu"
            else:
                if user_choice.lower() == self.ui_helper.BACK.lower():
                    return

                elif user_choice.lower() == self.ui_helper.QUIT.lower():
                    self.ui_helper.quit_prompt(header_str)

                elif user_choice in options_dict:
                    setattr(a_vehicle, "status", options_dict[user_choice])
                    confirm_choice = self.confirm_status(a_vehicle, header_str)
                    if confirm_choice in self.ui_helper.YES:
                        self.logic_api.change_vehicle_condition(a_vehicle.id, a_vehicle.status)
                        return
                    else:
                        return
                        
            
    def confirm_status(self, a_vehicle, header_str):
        ''' Asks user to confirm new status, and saves it in the database if yes '''
        self.ui_helper.clear()
        self.ui_helper.print_header(header_str)
        self.view_vehicle_details(a_vehicle)
        self.ui_helper.print_line("    Do you want to confirm these changes? (y/n)")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_hash_line()
        print()
        return input("Input: ")