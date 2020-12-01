class AdminMenu():

    def __init__(self, ui_helper, width):
        self.width = width
        self.ui_helper = ui_helper

    def show_tasks(self, error_msg=""):
        options_list = [("1", "Contracts"), ("2", "Employees"), ("3", "Vehicles"), ("4", "Locations"), ("5", "Reports")]
        opt_str = "Select a task:"
        user_choice = None

        while user_choice != self.ui_helper.QUIT:

            self.ui_helper.clear()

            self.ui_helper.print_header("Administrator")
            self.ui_helper.print_options(options_list, opt_str)
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = self.ui_helper.get_user_menu_choice(options_list)
            if user_choice == self.ui_helper.BACK:
                print("I'm back")
                return

            elif user_choice == self.ui_helper.QUIT:
                print("heckin quittin'")
                quit()

            elif user_choice == options_list[0][0]:
                print("Contracts homie")
            
            ### Rest of options ###
