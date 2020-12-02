from ui_layer.employee_ui import EmployeeUI

class TaskMenu():

    def __init__(self, ui_helper, logic_api, width):
        self.width = width
        self.ui_helper = ui_helper
        self.logic_api = logic_api
        self.employee_ui = EmployeeUI(self.ui_helper, self.logic_api)
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

    def show_tasks(self, staff_type, error_msg=""):
        
            
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
                    print("I'm back")
                    return

                elif user_choice == self.ui_helper.QUIT:
                    self.ui_helper.quit_prompt(header_str)

                else:
                    next_menu = available_options[user_choice]
                    if next_menu == "Employees":
                        self.employee_ui.show_options(header_str)
                        
                        
                    elif next_menu == "Vehicles":
                        print("Vehicles")

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

            
            ### Rest of options ###
