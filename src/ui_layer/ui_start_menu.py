from ui_layer.ui_helper import UIHelper
from logic_layer.logic_api import LogicAPI
from ui_layer.employee_ui import EmployeeUI
from ui_layer.vehicle_ui import VehicleUI
from ui_layer.location_ui import LocationUI
from ui_layer.contract_ui import ContractUI
from ui_layer.report_ui import ReportUI

class UIStartMenu():

    def __init__(self, width):
        self.width = width              #Screen width
        self.logic_api = LogicAPI()
        self.ui_helper = UIHelper(self.width, "Welcome") #<- Starting header string
        self.employee_ui = EmployeeUI(self.ui_helper, self.logic_api)
        self.vehicle_ui = VehicleUI(self.ui_helper, self.logic_api)
        self.location_ui = LocationUI(self.ui_helper, self.logic_api, self.employee_ui, self.vehicle_ui)
        self.contract_ui = ContractUI(self.ui_helper, self.logic_api, self.employee_ui, self.vehicle_ui)
        self.report_ui = ReportUI(self.ui_helper, self.logic_api)


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
                "3": "Locations",
                "4": "Pick ups",
                "5": "Returns"
            }
        }


    def choose_location(self, error_msg=""):
        '''
        START SCREEN,
        shows user available airport codes and prompts user for code. 
        Then, calls task menu, showing and accepting only available options 
        '''
        norris_joke = self.logic_api.get_random_joke()
        options_list = self.logic_api.destinations_option_list()
        opt_str = "Please select your airport code:"

        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_options(options_list, opt_str)
            self.ui_helper.print_start_footer()
            if error_msg != "":
                print(error_msg)
            else:
                print(norris_joke, end="")
            staff_type = self.ui_helper.get_user_menu_choice(options_list)
            if staff_type != None:

                if staff_type.lower() == self.ui_helper.QUIT or staff_type.lower() == self.ui_helper.BACK:
                    self.ui_helper.quit_prompt()

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
        options_list = self.ui_helper.dict_to_list(available_options)

        #Sets ui helpers header to priviledge level, and shows location if user is an airport employee
        if priviledge == "Airport Employee":
            self.ui_helper.header_string = f"{priviledge}, {staff_type}"
        else:
            self.ui_helper.header_string = priviledge

        while True:

            self.ui_helper.clear()

            self.ui_helper.print_header()
            self.ui_helper.print_options(options_list, opt_str)
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = self.ui_helper.get_user_menu_choice(options_list)

            #If user choice is valid, helper class checks this
            if user_choice != None:

                if user_choice.lower() == self.ui_helper.BACK:
                    return

                elif user_choice.lower() == self.ui_helper.QUIT:
                    self.ui_helper.quit_prompt()

                else:
                    next_menu = available_options[user_choice]
                    if next_menu == "Employees":
                        self.employee_ui.show_options()
                        
                        
                    elif next_menu == "Vehicles":
                        self.vehicle_ui.show_options()

                    elif next_menu == "Locations":

                        if self.priviledge_dict[staff_type].lower() == "airport employee":          #Airport staff only goes to see all locations if they select locations
                            location_list = self.logic_api.get_destinations()
                            self.location_ui.view_location_list(location_list)

                        else:                                                                       #Office and admin can create and find specific locations
                            self.location_ui.show_options()
                        
                    elif next_menu == "Contracts":
                        self.contract_ui.show_options()
                        
                    elif next_menu == "Reports":
                        pass
                        self.report_ui.reports_menu()
                        
                    elif next_menu == "Pick ups":
                        self.contract_ui.pick_up_vehicle()

                    elif next_menu == "Returns":
                        self.contract_ui.returns_menu()

                    else:
                        pass
 
            else:
                error_msg = "Please select an option from the menu"
