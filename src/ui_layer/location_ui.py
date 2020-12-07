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
                        the_location = self.find_location(header_str)
                        self.view_location_details(the_location, header_str)
                                                                  

                    elif self.options_dict[user_choice] == self.VIEW_ALL:
                        #View all locations
                        pass

            else:
                error_msg = "Please select an option from the menu"

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

    def view_location_details(self, the_dest, header_str):
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.display_location(the dest)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            return input("...")

    def display_location(self, the_dest):
        self.ui_helper.print_line(f"    COUNTRY:............{the_dest.country}")
        self.ui_helper.print_line(f"    CITY:...............{the_dest.airport}")
        self.ui_helper.print_line(f"    PHONE:.............{the_dest.phone}")
        self.ui_helper.print_line(f"    OPNENING HOURS:.....{the_dest.hours}")
        self.ui_helper.print_line(f"    IATA:...............{the_dest.iata}")