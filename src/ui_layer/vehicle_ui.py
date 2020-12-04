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

                if user_choice == self.ui_helper.BACK:
                    print("I'm back")
                    return

                elif user_choice == self.ui_helper.QUIT:
                    self.ui_helper.quit_prompt(header_str)

                else:
                    
                    if self.options_dict[user_choice] == self.REGISTER:
                        self.register_vehicle(header_str)
                        

                    elif self.options_dict[user_choice] == self.FIND:
                        #self.find_vehicle(header_str)
                        pass

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
            self.print_vehicle_list(vehicles)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = self.ui_helper.get_user_menu_choice(options_list)
            if user_choice == self.ui_helper.BACK:
                return

            elif user_choice == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt(header_str)
            else:
                error_msg = "Please select an option, or enter 9 to quit and 0 to go back"
            

        
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
        self.ui_helper.print_line("Vehicle overview:")
        self.ui_helper.print_blank_line()
        self.ui_helper.n_columns([manu_str, model_str, type_str, year_str, color_str, status_str, licence_str, location_str])

        for vehicle in vehicle_list:
            manu = vehicle.manufacturer
            model = vehicle.model
            vtype = vehicle.type
            year = vehicle.year
            color = vehicle.color
            status = vehicle.status
            licence = vehicle.licence_type
            location = vehicle.location
            self.ui_helper.n_columns([manu, model, vtype, year, color, status, licence, location])


    def register_vehicle(self, header_str, error_msg=""):
        new_vehicle = Vehicle("", "", "", "", "", "", "", "", None)
        attribute_list = ["manufacturer", "model", "type", "year", "color", "status", "licence_type", "location"]
        for attribute in attribute_list:
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.view_vehicle_details(new_vehicle)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print()
            attr_value = input(f"Enter vehicles's {attribute}: ")
            attr_key = attribute.replace(" ", "_")
            setattr(new_vehicle, attr_key, attr_value)
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.ui_helper.print_line("Confirm new vehicle? (y/n)")
            self.view_vehicle_details(new_vehicle)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print()
            user_choice = input("Input: ")
            if user_choice == self.ui_helper.YES:
                

            elif user_choice == self.ui_helper.QUIT:
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
        self.ui_helper.print_blank_line()

    
    def unsaved_changes(self, a_vehicle, header_str):
        ''' Asks user if they want to go back without saving their changes '''
        self.ui_helper.clear()
        self.ui_helper.print_header(header_str)
        self.ui_helper.print_line("You have unsaved changes!")
        self.ui_helper.print_line("Are you sure you want to go back? (y/n)")
        self.ui_helper.print_line("Your unsaved changes will be lost")
        self.ui_helper.print_blank_line()
        self.view_vehicle_details(a_vehicle)
        self.ui_helper.print_blank_line()
        self.ui_helper.print_hash_line()
        print()
        return input("Input: ")
