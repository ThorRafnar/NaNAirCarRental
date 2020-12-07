from model_layer.destination import Destination

class LocationUI():
    CREATE = "Create new location"
    FIND = "Find a location"
    VIEW_ALL = "View all locations"



    def __init__(self, ui_helper, logic_api):
        self.ui_helper = ui_helper
        self.logic_api = logic_api
        self.options_dict = {
            "1": self.CREATE, 
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

                if user_choice.lower() == self.ui_helper.BACK.lower():
                    return

                elif user_choice.lower() == self.ui_helper.QUIT.lower():
                    self.ui_helper.quit_prompt(header_str)

                else:
                    
                    if self.options_dict[user_choice] == self.CREATE:
                        #Create location
                        pass

                    elif self.options_dict[user_choice] == self.FIND:
                        #Find location
                        pass                                               

                    elif self.options_dict[user_choice] == self.VIEW_ALL:
                        #View all locations
                        pass

            else:
                error_msg = "Please select an option from the menu"