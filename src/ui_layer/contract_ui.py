from model_layer.contract import Contract
from model_layer.customer import Customer

class ContractUI():
    CREATE = "Create new contract"
    FIND = "Find a contract"
    VIEW_ALL = "View all contracts"



    def __init__(self, ui_helper, logic_api, employee_ui):
        self.ui_helper = ui_helper
        self.logic_api = logic_api
        self.employee_ui = employee_ui
        self.options_dict = {
            "1": self.CREATE, 
            "2": self.FIND, 
            "3": self.VIEW_ALL
        }
    
    def show_options(self, header_str, error_msg=""):
        ''' shows available options and allows user to select '''
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
                        self.new_contract(header_str)
                        pass
                        #Create contract                        

                    elif self.options_dict[user_choice] == self.FIND:
                        pass
                        #find contract
                            
                    elif self.options_dict[user_choice] == self.VIEW_ALL:
                        pass
                        #View all contracts

            else:
                error_msg = "Please select an option from the menu"


    def view_customer_details(self, the_customer):
        ''' '''
        self.ui_helper.print_line(f"        NAME:....................{the_customer.name}")
        self.ui_helper.print_line(f"        SOCIAL SECURITY NR:......{the_customer.ssn}")
        self.ui_helper.print_line(f"        ADDRESS:.................{the_customer.address}")
        self.ui_helper.print_line(f"        POSTAL CODE:.............{the_customer.postal_code}")
        self.ui_helper.print_line(f"        PHONE NUMBER:...........{the_customer.phone}")
        self.ui_helper.print_line(f"        EMAIL:...................{the_customer.email}")
        self.ui_helper.print_line(f"        COUNTRY:.................{the_customer.country}")
        self.ui_helper.print_blank_line()


    def view_contract_details(self, the_contract, vehicle_type):
        ''' '''
        self.ui_helper.print_line(f"        CUSTOMER ID:.............{the_contract.customer_ssn}")
        self.ui_helper.print_line(f"        EMPLOYEE ID:.............{the_contract.employee_ssn}")
        self.ui_helper.print_line(f"        VEHICLE TYPE:............{vehicle_type}")
        self.ui_helper.print_line(f"        VEHICLE ID:..............{the_contract.vehicle_id}")
        self.ui_helper.print_line(f"        START DATE:..............{the_contract.loan_date}")
        self.ui_helper.print_line(f"        END DATE:................{the_contract.end_date}")
        self.ui_helper.print_blank_line()


    def create_customer(self, ssn, header_str, error_msg =""):
        ''' Creates a new customer and passes it along to logic '''
        the_customer = Customer("", ssn, "", "", ".", "", "")
        attribute_list = ["name", "address", "postal code", "phone", "email", "country"]
        for attribute in attribute_list:
            while True:
                placeholder_text = f"<< Enter {attribute} >>"
                attr_key = attribute.replace(" ", "_")
                setattr(the_customer, attr_key, placeholder_text)
                self.ui_helper.clear()
                self.ui_helper.print_header(header_str)
                self.view_customer_details(the_customer)
                self.ui_helper.print_blank_line()
                self.ui_helper.print_footer()
                print()
                attr_value = input(f"Enter customer's {attribute}: ")
                if attr_value.lower() == self.ui_helper.BACK.lower():
                    #back_choice = self.unsaved_changes(the_customer, header_str)
                    #if back_choice.lower() in self.ui_helper.YES:
                    #    return
                    #else:
                    #    continue
                    return

                elif attr_value.lower() == self.ui_helper.QUIT.lower():
                    self.ui_helper.quit_prompt(header_str)
                    continue

                else:
                    setattr(the_customer, attr_key, attr_value)     #Sets attribute to input
                    break

        self.logic_api.add_customer(the_customer)
        return the_customer


    def find_customer(self, header_str, error_msg=""):
        ''' Searches for a customer, returning none if no customer exists with that ssn '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_line("    Enter customer's social security number")
            self.ui_helper.print_line("    (DDMMYY-NNNN)")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            ssn = input("Input: ")

             #Check if the user wants to back or quit
            if ssn.lower() == self.ui_helper.QUIT.lower():
                self.ui_helper.quit_prompt(header_str)
            elif ssn.lower() == self.ui_helper.BACK.lower():
                return

            ssn = self.ui_helper.ssn_formatter(ssn)
            if ssn == None:
                error_msg = "Please provide a correcly formatted social security number, DDMMYY-NNNN"
                continue

            #If the new one is valid we need to reset the error message
            else:
                error_msg = ""

            return self.logic_api.find_customer(ssn), ssn

    
    def employee_for_contract(self, header_str, error_msg=""):
        ''' Gets employee for the contract '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_line("    Enter employee's social security number")
            self.ui_helper.print_line("    (DDMMYY-NNNN)")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            ssn = input("Input: ")

             #Check if the user wants to back or quit
            if ssn.lower() == self.ui_helper.QUIT.lower():
                self.ui_helper.quit_prompt(header_str)
            elif ssn.lower() == self.ui_helper.BACK.lower():
                return

            ssn = self.ui_helper.ssn_formatter(ssn)
            if ssn == None:
                error_msg = "Please provide a correcly formatted social security number, DDMMYY-NNNN"
                continue

            #If the new one is valid we need to reset the error message
            else:
                error_msg = ""

            return self.logic_api.find_employee(ssn)

            

    def new_contract(self, header_str, error_msg=""):
        ''' Composite method for creating a contract'''
        the_customer, ssn = self.find_customer(header_str)
        if the_customer == None:    #If customer doesn't exists
            the_customer = self.create_customer(ssn, header_str)    #Creates new customer
    
        self.confirm_customer(the_customer, header_str)             #Asks user to confirm

        the_employee = self.employee_for_contract(header_str) 

        if the_employee != None:                                    #If emp exists, confirm it
            self.confirm_employee(the_employee, header_str)

        else:                                                       #If emp doesn't, create it
            self.employee_ui.create_employee(header_str, ssn)
            the_employee = self.logic_api.find_employee(ssn)

        the_contract = self.create_contract(the_customer, the_employee, header_str)              #Creates contract with the customer

    
    def confirm_customer(self, the_customer, header_str, error_msg=""):
        ''' Asks user if customer info is correct, and allows changes in everything except name and ssn '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.ui_helper.print_line("    Is this information correct? (y/n)")
            self.ui_helper.print_blank_line()
            self.view_customer_details(the_customer)
            self.ui_helper.print_footer()
            print(error_msg)
            return input("Input: ")

    
    def confirm_employee(self, the_employee, header_str, error_msg=""):
        ''' Asks user if employee info is correct, and allows changes in everything except name and ssn '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.ui_helper.print_line("    Is this information correct? (y/n)")
            self.ui_helper.print_blank_line()
            self.employee_ui.view_employee_details(the_employee)
            self.ui_helper.print_footer()
            print(error_msg)
            input("Input: ")
            return

        
    def get_location(self, header_str, error_msg=""):
        ''' Gets a location from the user '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.ui_helper.print_line("    Enter contract location")
            self.ui_helper.print_blank_line()
            #self.employee_ui.view_employee_details(the_employee)
            self.ui_helper.print_footer()
            print(error_msg)
            user_input = input("Input: ")
            if user_input.lower() == self.ui_helper.QUIT.lower():
                self.ui_helper.quit_prompt(header_str)

            elif user_input.lower() == self.ui_helper.BACK.lower():
                return

            location = self.logic_api.find_destination(user_input)
            if location != None:
                return location
            else:
                error_msg = "Please enter a valid location (IATA)"

    
    def get_date(self, date_type_str, header_str, error_msg=""):
        ''' gets a date from the user '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.ui_helper.print_line(f"    Enter contract {date_type_str} date (DD/MM/YY)")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            date_str = input("Input: ")
            if date_str.lower() == self.ui_helper.QUIT.lower():
                self.ui_helper.quit_prompt(header_str)

            elif date_str.lower() == self.ui_helper.BACK.lower():
                return

            date_str = self.logic_api.check_date(date_str)
            if date_str != None:
                return date_str
            else:
                error_msg = "Please enter a valid date (DD/MM/YY)"

    
    def get_vehicle_type(self, location, header_str, error_msg=""):
        ''' Displays all vehicle types in a given location and allows user to choose '''
        vehicle_types = self.logic_api.get_filtered_vehicle_types(location)
        vehicle_type_list = [(str(ind + 1),vtype.name) for ind, vtype in enumerate(vehicle_types)]       
        vehicle_type_dict = dict(vehicle_type_list)
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.ui_helper.print_options(vehicle_type_list, "Select vehicle type:")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            user_choice = self.ui_helper.get_user_menu_choice(vehicle_type_list)
            if user_choice.lower() == self.ui_helper.BACK.lower():
                return
            elif user_choice.lower() == self.ui_helper.QUIT.lower():
                self.ui_helper.quit_prompt(header_str)
            elif user_choice in vehicle_type_dict:
                return vehicle_type_dict[user_choice]
            else:
                error_msg = "Fuck off"



    def create_contract(self, the_customer, the_employee, header_str, error_msg=""):
        ''' Gets input from user and creates a new contract '''
        the_contract = Contract(None, the_customer.ssn, the_employee.ssn, "", "", "", "", "")
        the_contract.start_date = self.get_date("start", header_str)
        the_contract.end_date = self.get_date("end", header_str)
        location = self.get_location(header_str)
        vehicle_type = self.get_vehicle_type(location, header_str)
        the_vehicle = self.choose_vehicle(the_contract.start_date, the_contract.end_date, location, vehicle_type, header_str)
        
            
    def unsaved_changes(self, the_customer, header_str):
        ''' Asks user if they want to go back without saving their changes '''
        self.ui_helper.clear()
        self.ui_helper.print_header(header_str)
        self.view_customer_details(the_customer)
        self.ui_helper.unsaved_prompt()
        self.ui_helper.print_blank_line()
        self.ui_helper.print_hash_line()
        print()
        return input("Input: ")