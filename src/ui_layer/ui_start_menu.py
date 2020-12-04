from ui_layer.ui_helper import UIHelper
from logic_layer.logic_api import LogicAPI
from ui_layer.employee_ui import EmployeeUI
from ui_layer.vehicle_ui import VehicleUI

class UIStartMenu():

    def __init__(self, width):
        self.width = width              #Screen width
        self.logic_api = LogicAPI()
        self.ui_helper = UIHelper(self.width)
        self.employee_ui = EmployeeUI(self.ui_helper, self.logic_api)
        self.vehicle_ui = VehicleUI(self.ui_helper, self.logic_api)

        #TODO Make this get locations as dict from logic api
        self.priviledge_dict = {
            "ADM": "Administrator",
            "KEF": "Office Employee",
            "GOH": "Airport Employee",
            "KUS": "Airport Employee",
            "FAE": "Airport Employee",
            "LWK": "Airport Employee",
            "LYR": "Airport Employee"
        } 
        
        #To make sure user can only select an option they are allowed to choose
        self.options_dict = {
            "Administrator": {
                "1": "Employees", 
                "2": "Vehicles", 
                "3": "Locations",
                "4": "Contracts",
                "5": "Reports"
            },
            "Office Employee": {
                "1": "Employees",
                "2": "Vehicles",
                "3": "Locations",
                "4": "Contracts"
            },
            "Airport Employee": {
                "1": "Employees",
                "2": "Vehicles",
                "3": "Locations"
            }
        }


    def choose_location(self, error_msg=""):
        '''
        START SCREEN,
        shows user available airport codes and prompts user for code. 
        Then, calls task menu, showing and accepting only available options 
        '''
        
        options_list = self.logic_api.destinations_option_list()
        opt_str = "Please select your airport code:"

        while True:
            
            self.ui_helper.clear()
            self.ui_helper.print_header("Welcome!")
            self.ui_helper.print_options(options_list, opt_str)
            self.ui_helper.print_start_footer()
            print(error_msg)
            staff_type = self.ui_helper.get_user_menu_choice(options_list)
            if staff_type != None:

                if staff_type == self.ui_helper.QUIT or staff_type == self.ui_helper.BACK:
                    self.ui_helper.quit_prompt("Welcome!")

                else:
                    self.show_tasks(staff_type)

            else:
                #Villuskilabod#
                error_msg = "Please select an airport code from the list, or 9 to quit"




    def show_tasks(self, staff_type, error_msg=""):
        ''' Shows available tasks, depending on user priviledge level '''     
        if staff_type not in self.priviledge_dict:
            self.priviledge_dict[staff_type] = "Airport Employee"
        priviledge = self.priviledge_dict[staff_type]

        available_options = self.options_dict[priviledge]

        
        opt_str = "Select a task:"

        #Because helper functions need a list of tuples
        options_list = [(k, v) for k, v in available_options.items()]

        if priviledge == "Airport Employee":
            header_str = f"{priviledge}, {staff_type}"
        else:
            header_str = priviledge

        while True:

            self.ui_helper.clear()

            self.ui_helper.print_header(header_str)
            self.ui_helper.print_options(options_list, opt_str)
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = self.ui_helper.get_user_menu_choice(options_list)

            #If user choice is valid, helper class checks this
            if user_choice != None:

                if user_choice == self.ui_helper.BACK:
                    return

                elif user_choice == self.ui_helper.QUIT:
                    self.ui_helper.quit_prompt(header_str)

                else:
                    next_menu = available_options[user_choice]
                    if next_menu == "Employees":
                        self.employee_ui.show_options(header_str)
                        
                        
                    elif next_menu == "Vehicles":
                        self.vehicle_ui.show_options(header_str)

                    elif next_menu == "Locations":
                        #Do location things
                        print("Locations")
                        
                    elif next_menu == "Contracts":
                        #Do contract things
                        print("Contracts")
                        
                    elif next_menu == "Reports":
                        #Do report things
                        print("Reports")
                        
                    else:
                        pass
 
            else:
                error_msg = "Please select an option from the menu"
