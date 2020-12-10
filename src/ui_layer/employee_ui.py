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


    def show_options(self, error_msg=""):
        options_list = self.ui_helper.dict_to_list(self.options_dict)
        
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_options(options_list, "Select task:")
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = self.ui_helper.get_user_menu_choice(options_list)

            if user_choice != None:

                if user_choice.lower() == self.ui_helper.BACK:
                    return

                elif user_choice.lower() == self.ui_helper.QUIT:
                    self.ui_helper.quit_prompt()

                #The actual options
                else:
                    
                    if self.options_dict[user_choice] == self.VIEW_ALL:
                        self.get_employees()

                    elif self.options_dict[user_choice] == self.CREATE:
                        self.new_employee()

                    elif self.options_dict[user_choice] == self.CHANGE:
                        self.modify_employee()

                    elif self.options_dict[user_choice] == self.FIND:
                        self.find_employee()
                    
            else:
                error_msg = "Please select an option from the menu"


    def get_employees(self, error_msg=""):
        ''' 
        Gets a list of all employees and displays them for the user, takes input from user,
        to navigate back or quit
        '''
        while True:
            options_list = []
            emps = self.logic_api.get_employees()   #Gets all employees from logic
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.print_employee_list(emps)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = self.ui_helper.get_user_menu_choice(options_list)
            if user_choice != None:
                if user_choice.lower() == self.ui_helper.BACK:
                    return

                elif user_choice.lower() == self.ui_helper.QUIT:
                    self.ui_helper.quit_prompt()
                    
                else:
                    error_msg = "Please select an option from the menu"
            else:
                error_msg = "Please select an option from the menu"


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


    def check_if_employee_exists(self, option, error_msg=""):
        ''' Gets ssn from user and returns an employee if it exists and none if it doesn't '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line(option)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_line("    Enter employee's social security number")
            self.ui_helper.print_line("    (DDMMYY-NNNN)")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            ssn = input("Input: ")
            if ssn.lower() == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()
            elif ssn.lower() == self.ui_helper.BACK:
                return  None, None  #Because caller is expecting two variables
            
            ssn = self.logic_api.check_ssn(ssn)         #Formats and checks ssn, returning none if invalid

            #Checks ssn is valid or not
            if ssn == None:
                error_msg = "Please provide a correcly formatted social security number, DDMMYY-NNNN"
                continue

            return self.logic_api.find_employee(ssn), ssn    #finds employee with the ssn, returning none if it doesnt exist, returning the ssn as well


    def emp_not_found(self, ssn):
        ''' Says employee doesnt exist and asks if user wants to create it '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line("No employee with this social security number found")
            self.ui_helper.print_line("Do you want to create one? (y/n)")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print()
            user_choice = input("Input: ")
            if user_choice.lower() in self.ui_helper.YES:
                self.create_employee(ssn)
                return
            else:
                return


    def find_employee(self, error_msg=""):
        '''
        Searches for an employee and displays it if it exists
        if it doesn't, asks the user if they want to create it
        '''
        emp, ssn = self.check_if_employee_exists(self.FIND)

        if ssn == None:     #If user wants to back
            return          #go back

        else:
            
            if emp != None:                     #if the employee already exists
                self.view_employee(emp)
                return
                    
            else:                                   #If the employee does not exist
                self.emp_not_found(ssn)             #Tells user and asks if they want to create a new one
                return


    def modify_employee(self, error_msg=""):
        ''' 
        Gets ssn from user and checks if emp exists, if it does, goes to change employee details,
        if emp doesn't exist, asks if user wants to create it 
        '''
        emp, ssn = self.check_if_employee_exists(self.CHANGE)

        if ssn == None:     #If user wants to back
            return          #go back

        else:
                
            if emp != None:                     #if the employee exists
                self.change_employee_details(emp)
                return
                    
            else:                               #If employee doesn't exist
                self.emp_not_found(ssn)         #Tells user and asks if they want to create a new one
                return


    def new_employee(self, error_msg=""):
        '''
        Searches for an employee and if it does not exists, allows user to create.
        if it already exists, asks user if they want to modify
        '''
        emp, ssn = self.check_if_employee_exists(self.CREATE)

        if ssn == None:     #If user returned from check
            return          #Just go back

        else:
                
            if emp != None:                     #if the employee already exists
                self.emp_already_exists(emp)
                return
                    
            else:                                   #If the employee does not exist
                self.create_employee(ssn)             #Tells user and asks if they want to create a new one
                return

    
    def emp_already_exists(self, emp):
        ''' Informs user that an employee already exists and asks if the user wants to change it '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line("An employee with this social security already exists")
            self.ui_helper.print_line("Do you want to modify? (y/n)")
            self.ui_helper.print_blank_line()
            self.view_employee_details(emp)
            self.ui_helper.print_footer()
            print()
            user_choice = input("Input: ")
            if user_choice.lower() in self.ui_helper.YES:
                self.change_employee_details(emp)
                return
            else:
                return


    def view_employee(self, employee, error_msg=""):
        ''' Shows full view employee interface, returning or quitting based on input'''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line("Employee information:")
            self.ui_helper.print_blank_line()
            self.view_employee_details(employee)
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = input("Input: ")
            if user_choice.lower() == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()
            elif user_choice.lower() == self.ui_helper.BACK:
                return
            else:
                error_msg = f"Select either {self.ui_helper.QUIT.upper()} to quit or {self.ui_helper.BACK.upper()} to go back"


    def change_employee_details(self, employee, error_msg=""):
        ''' 
        shows all details of an employee, with indices and takes user choice in what to change, and changes it, 
        when user confirms, sends an instance of the employee down to logic 
        If an attribute has been changed, allows user to undo
        '''
        old_attr_list = []
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line("Change employee")
            self.ui_helper.print_line("Please select an option:")
            self.ui_helper.print_blank_line()
            self.emp_change_view(employee)
            if old_attr_list != []:         #Undo option if any changes have been made
                self.ui_helper.print_line(f"    ({self.ui_helper.UNDO.upper()})ndo: Undo last changes")
            else:
                self.ui_helper.print_blank_line()
            self.ui_helper.print_line(f"    ({self.ui_helper.SAVE.upper()})ave: Save Changes")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = input("Input: ")
            if user_choice.lower() == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()
            elif user_choice.lower() == self.ui_helper.BACK:
                if old_attr_list != []:      #If the user has unsaved changes
                    user_choice = self.unsaved_changes(employee)
                    if user_choice.lower() in self.ui_helper.YES:
                        return
                    else:
                        continue
                else:
                    return

            else:

                if user_choice == "1":
                    old_attr_list.append(self.ui_helper.get_old_attributes(employee, "address"))        #Stores old values before changing
                    setattr(employee, "address", f"<< ENTER NEW ADDRESS >>")
                    employee.address = self.change_employee_attribute(employee, "address")

                elif user_choice == "2":
                    old_attr_list.append(self.ui_helper.get_old_attributes(employee, "postal_code"))    #Stores old values before changing
                    setattr(employee, "postal_code", f"<< ENTER NEW POSTAL CODE >>")
                    employee.postal_code = self.change_employee_attribute(employee, "postal_code")

                elif user_choice == "3":
                    old_attr_list.append(self.ui_helper.get_old_attributes(employee, "mobile_phone"))   #Stores old values before changing
                    setattr(employee, "mobile_phone", f"<< ENTER NEW MOBILE PHONE NR >>")
                    employee.mobile_phone = self.change_employee_attribute(employee, "mobile_phone")

                elif user_choice == "4":
                    old_attr_list.append(self.ui_helper.get_old_attributes(employee, "home_phone"))     #Stores old values before changing
                    setattr(employee, "home_phone", f"<< ENTER NEW HOME PHONE NR >>")
                    employee.home_phone = self.change_employee_attribute(employee, "home_phone")

                elif user_choice == "5":
                    old_attr_list.append(self.ui_helper.get_old_attributes(employee, "email"))          #Stores old values before changing
                    setattr(employee, "email", f"<< ENTER NEW EMAIL ADDRESS >>")
                    employee.email = self.change_employee_attribute(employee, "email")

                elif user_choice == "6":
                    old_attr_list.append(self.ui_helper.get_old_attributes(employee, "work_area"))      #Stores old values before changing
                    setattr(employee, "work_area", f"<< ENTER NEW WORK AREA >>")
                    employee.work_area = self.change_employee_attribute(employee, "work_area")

                elif user_choice.lower() == self.ui_helper.SAVE:
                    self.confirm_changes(employee)
                    return

                elif user_choice.lower() == self.ui_helper.UNDO and old_attr_list != []:
                    ''' Undo the last changes stored in the old attribute list, and removes the last item in the list '''
                    undo_key = old_attr_list[-1][0]
                    undo_value = old_attr_list[-1][1]
                    del old_attr_list[-1]
                    setattr(employee, undo_key, undo_value)
                    continue                

                else:
                    error_msg = "Please select an option from the menu"

    
    def emp_change_view(self, employee):
        ''' Displays Attributes of an employee and indices to change each attribute '''
        self.ui_helper.print_line(f"        NAME:....................{employee.name}")
        self.ui_helper.print_line(f"        SOCIAL SECURITY NR:......{employee.ssn}")
        self.ui_helper.print_line(f"    1.  ADDRESS:.................{employee.address}")
        self.ui_helper.print_line(f"    2.  POSTAL CODE:.............{employee.postal_code}")
        self.ui_helper.print_line(f"    3.  MOBILE PHONE:...........{employee.mobile_phone}")
        self.ui_helper.print_line(f"    4.  HOME PHONE:.............{employee.home_phone}")
        self.ui_helper.print_line(f"    5.  EMAIL:...................{employee.email}")
        self.ui_helper.print_line(f"    6.  WORK AREA:...............{employee.work_area}")
        self.ui_helper.print_blank_line()
        
    
    def change_employee_attribute(self, employee, attribute, error_msg = ""):
        ''' Changes and error checks a single attribute change, when modifying an employee '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line("Change employee")
            self.ui_helper.print_line(f"Please enter a new {attribute}")
            self.ui_helper.print_blank_line()
            self.emp_change_view(employee)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_blank_line()
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            new_attr = input("Input: ")
            new_attr = self.logic_api.check_attribute(new_attr, attribute)
            if new_attr != None:
                return new_attr
            else:
                error_msg = f"Please enter a valid {attribute}"


    def confirm_changes(self, employee):
        ''' Asks the user if he wants to save his changes on an employee, and changes it if yes '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.view_employee_details(employee)
            self.ui_helper.print_line("Are you sure you want to save these changes? (y/n)")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print()
            confirm_choice = input("Input: ")
            if confirm_choice.lower() in self.ui_helper.YES:
                self.logic_api.change_employee_info(employee)
                return
            else:
                return

    
    def unsaved_changes(self, employee):
        ''' Asks user if they want to go back without saving their changes '''
        self.ui_helper.clear()
        self.ui_helper.print_header()
        self.view_employee_details(employee)
        self.ui_helper.unsaved_prompt()
        self.ui_helper.print_blank_line()
        self.ui_helper.print_hash_line()
        print()
        return input("Input: ")


    def create_employee(self, ssn, error_msg =""):
        emp = Employee("", "", "", ssn, ".", ".", "", "")
        attribute_list = ["name", "address", "postal code", "mobile phone", "home phone", "email", "work area"]
        for attribute in attribute_list:
            while True:
                placeholder_text = f"<< Enter {attribute} >>"
                attr_key = attribute.replace(" ", "_")
                setattr(emp, attr_key, placeholder_text)
                self.ui_helper.clear()
                self.ui_helper.print_header()
                self.view_employee_details(emp)
                self.ui_helper.print_blank_line()
                self.ui_helper.print_footer()
                print(error_msg)
                attr_value = input(f"Enter employee's {attribute}: ")
                if attr_value.lower() == self.ui_helper.BACK:
                    back_choice = self.unsaved_changes(emp)
                    if back_choice.lower() in self.ui_helper.YES:
                        return
                    else:
                        continue

                elif attr_value.lower() == self.ui_helper.QUIT:
                    self.ui_helper.quit_prompt()
                    continue

                else:
                    attr_value = self.logic_api.check_attribute(attr_value, attr_key)
                    if attr_value != None:
                        setattr(emp, attr_key, attr_value)     #Sets attribute to input
                        break
                    else:
                        error_msg = f"Please enter a valid {attribute}"

        self.ui_helper.clear()
        self.ui_helper.print_header()
        self.view_employee_details(emp)
        self.ui_helper.print_blank_line()
        self.ui_helper.print_footer()
        print("Confirm changes? (y/n)")
        user_choice = input("Input: ")
        if user_choice in self.ui_helper.YES:
            self.logic_api.register_employee(emp)
            self.employee_has_been_registered(emp)
            return
        else:
            return


    def employee_has_been_registered(self, employee):
        ''' Shows that the employee has been registered, enter to continue '''
        self.ui_helper.clear()
        self.ui_helper.print_header()
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
        email_header = "<< E-MAIL >>"
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
        