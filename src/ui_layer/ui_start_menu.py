from ui_layer.admin_menu import AdminMenu
from ui_layer.ui_helper import UIHelper

class UIStartMenu():



    def __init__(self, width):
        self.width = width
        self.ui_helper = UIHelper(self.width)
        self.airport_menu = "Hello, airport"
        self.admin_menu = AdminMenu(self.ui_helper, self.width)
        self.office_menu = "Office life is 9 to 5"


    def show_locations(self, error_msg=""):
        
        options_list = [("GOH", "Nuuk, Greenland"), ("KEF", "Reykjavík, Iceland"), ("KUS", "Kulusuk, Greenland"), ("FAE", "Tórshavn, Faroe Island"), ("LWK", "Tingwall, Shetland"), ("LYR", "Longyearbyen, Svalbard"), ("ADM", "Administrator")]
        opt_str = "Please select your airport code:"
        staff_type = None
        while staff_type != self.ui_helper.QUIT:
            
            self.ui_helper.clear()

            self.ui_helper.print_header("Welcome!")
            self.ui_helper.print_options(options_list, opt_str)
            self.ui_helper.print_start_footer()
            print(error_msg)
            staff_type = self.ui_helper.get_user_menu_choice(options_list)
            if staff_type != None:

                if staff_type.lower() == "adm":
                    self.admin_menu.show_tasks()

                elif staff_type.lower() == "kef":
                    print(self.office_menu)

                elif staff_type == self.ui_helper.QUIT:
                    print("Quitting")
                    quit()

                else:
                    print(self.airport_menu)

            else:
                #Villuskilabod#
                error_msg = "Please select an airport code from the list, or 9 to quit"
                self.show_locations(error_msg)
            


        

        

#f = UIStartMenu(75)
#f.show_locations()