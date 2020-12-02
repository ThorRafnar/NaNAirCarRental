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
        opt_str = "Select task"
        user_choice = None

        while user_choice != self.ui_helper.QUIT:

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

                    else:
                        opt_str = self.options_dict[user_choice]
                        self.find_employee(header_str, opt_str)
                    
            else:
                error_msg = "Please select an option from the menu"
                self.show_options(header_str, error_msg)



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
            if user_choice:
                pass

    def view_employee_details(self, employee):
        ''' shows all details of an employee '''
        self.ui_helper.print_line(f"    NAME:....................{employee.name}")
        self.ui_helper.print_line(f"    SOCIAL SECURITY NR:......{employee.ssn}")
        self.ui_helper.print_line(f"    ADDRESS:.................{employee.address}")
        self.ui_helper.print_line(f"    POSTAL CODE:.............{employee.postal_code}")
        self.ui_helper.print_line(f"    MOBILE PHONE:...........{employee.mobile_phone}")
        self.ui_helper.print_line(f"    HOME PHONE:.............{employee.home_phone}")
        self.ui_helper.print_line(f"    EMAIL:...................{employee.email}")
        self.ui_helper.print_line(f"    WORK AREA:...............{employee.work_area}")
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
        self.ui_helper.clear()
        self.ui_helper.print_header(header_str)
        self.ui_helper.print_line(opt_str)
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line("    Enter employee's social security number")
        self.ui_helper.print_line("    (DDMMYY-NNNN)")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_footer()
        ssn = input("Input: ")
        emp = self.logic_api.find_employee(ssn)

        
        if emp != None:                     #if the employee already exists
            
            if opt_str == self.CREATE:      #If the user wants to create the employee but one already exists with that ssn
                alert_str_a = "Employee with this social security number already exists!"
                alert_str_b = "Do you wish to modify? (y/n)"
                self.ui_helper.clear()
                self.ui_helper.print_header(header_str)
                self.ui_helper.print_line(alert_str_a)
                self.ui_helper.print_line(alert_str_b)
                self.ui_helper.print_blank_line()
                self.view_employee_details(emp)
                self.ui_helper.print_footer()
                print(error_msg)
            
            elif opt_str == self.FIND:         #If the user wants to find an employee and it exists
                message_str = "Employee information:"
                self.ui_helper.clear()
                self.ui_helper.print_header(header_str)
                self.ui_helper.print_line(message_str)
                self.ui_helper.print_blank_line()
                self.view_employee_details(emp)
                self.ui_helper.print_footer()
                print(error_msg)
            
            elif opt_str == self.CHANGE:        #If the user wants to change an employee and it exists
                self.ui_helper.clear()
                self.ui_helper.print_header(header_str)
                self.ui_helper.print_line("Change employee")
                self.ui_helper.print_line("Please select an option:")
                self.ui_helper.print_blank_line()
                self.change_employee_details(emp)
                self.ui_helper.print_footer()
                print(error_msg)
        
        else:                                   #If the employee does not exist

            if opt_str == self.CREATE:          #If the user wants to create an employee and it does not exist
                self.create_employee(ssn)

            elif opt_str == self.FIND:          #If the user wants to find an employee and it does not exist
                pass

            elif opt_str == self.CHANGE:        #If the user wants to change and employee and it does not exist
                pass



        self.ui_helper.get_user_menu_choice()
        

    def change_employee_details(self, employee):
        ''' shows all details of an employee '''
        self.ui_helper.print_line(f"        NAME:....................{employee.name}")
        self.ui_helper.print_line(f"        SOCIAL SECURITY NR:......{employee.ssn}")
        self.ui_helper.print_line(f"    1.  ADDRESS:.................{employee.address}")
        self.ui_helper.print_line(f"    2.  POSTAL CODE:.............{employee.postal_code}")
        self.ui_helper.print_line(f"    3.  MOBILE PHONE:...........{employee.mobile_phone}")
        self.ui_helper.print_line(f"    4.  HOME PHONE:.............{employee.home_phone}")
        self.ui_helper.print_line(f"    5.  EMAIL:...................{employee.email}")
        self.ui_helper.print_line(f"    6.  WORK AREA:...............{employee.work_area}")
        self.ui_helper.print_blank_line()


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

    def create_employee(self, ssn):
        name = input("Enter Name: ")
        address = input("Enter Address: ")
        postal_code = input("Enter postal code: ")
        home_phone = input("Enter home phone: ")
        mobile_phone = input("Enter mobile phone: ")
        email = input("Enter email: ")
        work_area = input("Enter work area: ")
        new_employee = Employee(name, address, postal_code, ssn, home_phone, mobile_phone, email, work_area)
        self.view_employee_details(new_employee)


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
        