from model_layer.employee import Employee


class EmployeeUI():
    CREATE = "Create new employee"
    CHANGE = "Change employee information"
    FIND = "Find employee"
    VIEW_ALL = "View all employees"


    def __init__(self, ui_helper, logic_api):
        self.logic_api = logic_api
        self.ui_helper = ui_helper
        self.options_dict = {
            "1": self.CREATE, 
            "2": self.CHANGE, 
            "3": self.FIND,
            "4": self.VIEW_ALL
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

                #The actual options
                else:
                    
                    if self.options_dict[user_choice] == self.VIEW_ALL:
                        self.get_employees(header_str)

                    else:                                                   #Other options share a method, search, change and create
                        opt_str = self.options_dict[user_choice]
                        self.find_employee(header_str, opt_str)
                    
            else:
                error_msg = "Please select an option from the menu"


    def get_employees(self, header_str, error_msg=""):
        ''' 
        Gets a list of all employees and displays them for the user, takes input from user,
        to navigate back or quit
        '''
        
        while True:
            options_list = []
            emps = self.logic_api.get_employees()
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.print_employee_list(emps)
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


    def view_employee_details(self, employee):
        ''' shows all details of an employee '''
        self.ui_helper.print_line(f"        NAME:....................{employee.name}")
        self.ui_helper.print_line(f"        SOCIAL SECURITY NR:......{employee.ssn}")
        self.ui_helper.print_line(f"        ADDRESS:.................{employee.address}")
        self.ui_helper.print_line(f"        POSTAL CODE:.............{employee.postal_code}")
        self.ui_helper.print_line(f"        MOBILE PHONE:...........{employee.mobile_phone}")
        self.ui_helper.print_line(f"        HOME PHONE:.............{employee.home_phone}")
        self.ui_helper.print_line(f"        EMAIL:...................{employee.email}")
        self.ui_helper.print_line(f"        WORK AREA:...............{employee.work_area}")
        self.ui_helper.print_blank_line()


    def find_employee(self, header_str, opt_str, error_msg=""):
        '''
        Used for find, create and change employee,
        If the user chose find:
            returns and prints the employee information
        if the user chose to create:
            if the employee doesnt exist, goes to create emlpoyee,
            to prevent employees with the same ssn
            if the employee exists, shows employee information and
            asks the user if they want to modify
        if the user chose to change:
            if the employee doesnt exist:
                asks user if they want to create
            if employee exists
                asks for attributes to change (NOT ssn or name)
        '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.ui_helper.print_line(opt_str)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_line("    Enter employee's social security number")
            self.ui_helper.print_line("    (DDMMYY-NNNN)")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            ssn = input("Input: ")

            #Check if the user wants to back or quit
            if ssn == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt(header_str)
            elif ssn == self.ui_helper.BACK:
                return

            #TODO Make logic check ssn input
            ssn = self.ui_helper.ssn_formatter(ssn)     #Formats the ssn correctly

            #If the ssn is invalid
            if ssn == None:
                error_msg = "Please provide a correcly formatted social security number, DDMMYY-NNNN"
                continue

            #If the new one is valid we need to reset the error message
            else:
                error_msg = ""

            #Searches for employee by ssn, returning none if it doesnt exists, and returning an employee instance if it does
            emp = self.logic_api.find_employee(ssn)
            
            if emp != None:                     #if the employee already exists
                
                if opt_str == self.CREATE:      #If the user wants to create the employee but one already exists with that ssn

                    #Shows employee details and asks if user wants to modify it
                    while True:
                        self.ui_helper.clear()
                        self.ui_helper.print_header(header_str)
                        self.ui_helper.print_line("Employee with this social security number already exists!")
                        self.ui_helper.print_line("Do you wish to modify? (y/n)")
                        self.ui_helper.print_blank_line()
                        self.view_employee_details(emp)
                        self.ui_helper.print_footer()
                        print(error_msg)
                        user_choice = input("Input: ")
                        if user_choice == self.ui_helper.QUIT:
                            self.ui_helper.quit_prompt(header_str)
                        elif user_choice == self.ui_helper.BACK:
                            return
                        elif user_choice in self.ui_helper.YES:
                            self.change_employee_details(emp, header_str)
                            return
                        else:
                            return

                
                elif opt_str == self.FIND:         #If the user wants to find an employee and it exists
                    self.view_employee(emp, header_str)
                    return
                    #Shows employee details


                elif opt_str == self.CHANGE:        #If the user wants to change an employee and it exists
                    self.change_employee_details(emp, header_str)
                    return
                      
            else:                                   #If the employee does not exist

                if opt_str == self.CREATE:          #If the user wants to create an employee and it does not exist
                    self.create_employee(header_str, ssn)
                    return

                elif opt_str == self.FIND or opt_str == self.CHANGE:          #If the user wants to find (or change) an employee and it does not exist
                    self.ui_helper.clear()
                    self.ui_helper.print_header(header_str)
                    self.ui_helper.print_line("No employee with this social security number found")
                    self.ui_helper.print_line("Do you want to create one? (y/n)")
                    self.ui_helper.print_blank_line()
                    self.ui_helper.print_footer()
                    print(error_msg)
                    user_choice = input("Input: ")

                    if user_choice in self.ui_helper.YES:
                        self.create_employee(header_str, ssn)
                    
                    return

            user_choice = input("Input: ")


    def view_employee(self, employee, header_str, error_msg=""):
        ''' Shows full view employee interface, returning or quitting based on input'''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.ui_helper.print_line("Employee information:")
            self.ui_helper.print_blank_line()
            self.view_employee_details(employee)
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = input("Input: ")
            if user_choice == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt(header_str)
            elif user_choice == self.ui_helper.BACK:
                return
            else:
                error_msg = "Please enter 0 to go back or 9 to quit"


    def change_employee_details(self, employee, header_str, error_msg=""):
        ''' shows all details of an employee, with indices and takes user choice in what to change, and changes it, 
        when user confirms, sends an instance of the employee down to logic '''
        opt_address = "1"
        opt_postal_code = "2"
        opt_mobile = "3"
        opt_home_phone = "4"
        opt_email = "5"
        opt_work_area = "6"
        opt_undo = "U"
        opt_save = "S"
        old_attr_list = []
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.ui_helper.print_line("Change employee")
            self.ui_helper.print_line("Please select an option:")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_line(f"        NAME:....................{employee.name}")
            self.ui_helper.print_line(f"        SOCIAL SECURITY NR:......{employee.ssn}")
            self.ui_helper.print_line(f"    {opt_address}.  ADDRESS:.................{employee.address}")
            self.ui_helper.print_line(f"    {opt_postal_code}.  POSTAL CODE:.............{employee.postal_code}")
            self.ui_helper.print_line(f"    {opt_mobile}.  MOBILE PHONE:...........{employee.mobile_phone}")
            self.ui_helper.print_line(f"    {opt_home_phone}.  HOME PHONE:.............{employee.home_phone}")
            self.ui_helper.print_line(f"    {opt_email}.  EMAIL:...................{employee.email}")
            self.ui_helper.print_line(f"    {opt_work_area}.  WORK AREA:...............{employee.work_area}")
            if old_attr_list != []:         #Undo option if any changes have been made
                self.ui_helper.print_line(f"    {opt_undo}.  << Undo >>")
            else:
                self.ui_helper.print_blank_line()
            self.ui_helper.print_line(f"    {opt_save}.  << Save Changes >>")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = input("Input: ")
            if user_choice == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt(header_str)
            elif user_choice == self.ui_helper.BACK:
                if old_attr_list != []:      #If the user has unsaved changes
                    user_choice = self.unsaved_changes(employee, header_str)
                    if user_choice.lower() in self.ui_helper.YES:
                        return
                    else:
                        continue
                else:
                    return

            else:

                if user_choice == opt_address:
                    old_attr_list.append(self.ui_helper.get_old_attributes(employee, "address"))        #Stores old values before changing
                    employee.address = input("Enter new address: ")

                elif user_choice == opt_postal_code:
                    old_attr_list.append(self.ui_helper.get_old_attributes(employee, "postal_code"))    #Stores old values before changing
                    employee.postal_code = input("Enter new postal code: ")

                elif user_choice == opt_mobile:
                    old_attr_list.append(self.ui_helper.get_old_attributes(employee, "mobile_phone"))   #Stores old values before changing
                    employee.mobile_phone = input("Enter new mobile phone number: ")

                elif user_choice == opt_home_phone:
                    old_attr_list.append(self.ui_helper.get_old_attributes(employee, "home_phone"))     #Stores old values before changing
                    employee.home_phone = input("Enter new home phone number: ")

                elif user_choice == opt_email:
                    old_attr_list.append(self.ui_helper.get_old_attributes(employee, "email"))          #Stores old values before changing
                    employee.email = input("Enter new email address: ")

                elif user_choice == opt_work_area:
                    old_attr_list.append(self.ui_helper.get_old_attributes(employee, "work_area"))      #Stores old values before changing
                    employee.work_area = input("Enter new work area: ")

                elif user_choice.upper() == opt_save:
                    self.confirm_changes(employee, header_str)
                    return

                elif user_choice.upper() == opt_undo and old_attr_list != []:
                    ''' Undo the last changes stored in the old attribute list, and removes the last item in the list '''
                    undo_key = old_attr_list[-1][0]
                    undo_value = old_attr_list[-1][1]
                    del old_attr_list[-1]
                    setattr(employee, undo_key, undo_value)
                    continue                

                else:
                    error_msg = "Please select an option from the menu"


    def confirm_changes(self, employee, header_str):
        ''' Asks the user if he wants to save his changes on an employee, and changes it if yes '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.view_employee_details(employee)
            self.ui_helper.print_line("Are you sure you want to save these changes? (y/n)")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print()
            confirm_choice = input("Input: ")
            if confirm_choice in self.ui_helper.YES:
                self.logic_api.change_employee_info(employee)
                return
            else:
                return

    
    def unsaved_changes(self, employee, header_str):
        ''' Asks user if they want to go back without saving their changes '''
        self.ui_helper.clear()
        self.ui_helper.print_header(header_str)
        self.view_employee_details(employee)
        self.ui_helper.unsaved_prompt()
        self.ui_helper.print_blank_line()
        self.ui_helper.print_hash_line()
        print()
        return input("Input: ")


    def check_name(self, name):
        """
        Takes user input for a name, checks that all characters are either alphabetical or spaces,
        if input has invalid characters, returns none
        """
        for char in name:
            if char.isalpha() == False and char != " ":
                name = None
                continue       
        return name


    def get_name(self):
        a_str = input("Enter name: ")
        name = self.check_name(a_str)
        return name


    def create_employee(self, header_str, ssn):
        emp = Employee("", "", "", ssn, ".", ".", "", "")
        attribute_list = ["name", "address", "postal code", "mobile phone", "home phone", "email", "work area"]
        for attribute in attribute_list:
            while True:
                placeholder_text = f"<< Enter {attribute} >>"
                attr_key = attribute.replace(" ", "_")
                setattr(emp, attr_key, placeholder_text)
                self.ui_helper.clear()
                self.ui_helper.print_header(header_str)
                self.view_employee_details(emp)
                self.ui_helper.print_blank_line()
                self.ui_helper.print_footer()
                print()
                attr_value = input(f"Enter employee's {attribute}: ")
                if attr_value == self.ui_helper.BACK:
                    back_choice = self.unsaved_changes(emp, header_str)
                    if back_choice.lower() in self.ui_helper.YES:
                        return
                    else:
                        continue

                elif attr_value == self.ui_helper.QUIT:
                    self.ui_helper.quit_prompt(header_str)
                    continue

                else:
                    setattr(emp, attr_key, attr_value)     #Sets attribute to input
                    break

        self.ui_helper.clear()
        self.ui_helper.print_header(header_str)
        self.view_employee_details(emp)
        self.ui_helper.print_blank_line()
        self.ui_helper.print_footer()
        print("Confirm changes? (y/n)")
        user_choice = input("Input: ")
        if user_choice in self.ui_helper.YES:
            self.logic_api.register_employee(emp)
            self.employee_has_been_registered(header_str, emp)
            return
        else:
            return


    def employee_has_been_registered(self, header_str, employee):
        ''' Shows that the employee has been registered '''
        self.ui_helper.clear()
        self.ui_helper.print_header(header_str)
        self.ui_helper.print_line("    Employee has been registered, press enter to continue")
        self.view_employee_details(employee)
        self.ui_helper.print_blank_line()
        self.ui_helper.print_footer()
        input("Input: ")


    def print_employee_list(self, emp_list):
        ''' Prints and overview of all employees, showing name, ssn, mobile nr, email and work area '''  

        name_header = "<< NAME >>"
        ssn_header = "<< SOCIAL SECURITY NR >>"
        mobile_header = "<< MOBILE NR >>"
        email_header = "<< E MAIL >>"
        work_area_header = "<< WORK AREA >>"
        max_name_length = max(len(emp.name) for emp in emp_list)
        max_email_length = max(len(emp.email) for emp in emp_list)
        name_header = name_header + " " * (max_name_length - len(name_header))  #Padding name header to match names
        self.ui_helper.print_line("Employee overview:")
        self.ui_helper.print_blank_line()
        self.ui_helper.n_columns([name_header, ssn_header, mobile_header, email_header, work_area_header])
        
        for emp in emp_list:
            name = emp.name
            #pads name with spaces so that length is equal to the longest name
            #Done to left align names
            name = name + " " * (max_name_length - len(name))
            ssn = emp.ssn
            mobile = emp.mobile_phone
            email = emp.email
            #pads email with spaces so that length is equal to the longest email
            #Done to left align names
            email = email + " " * (max_email_length - len(email))
            work_area = emp.work_area
            self.ui_helper.n_columns([name, ssn, mobile, email, work_area])
        