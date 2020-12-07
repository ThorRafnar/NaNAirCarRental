from model_layer.contract import Contract
from model_layer.customer import Customer

class ContractUI():
    CREATE = "Create new contract"
    FIND = "Find a contract"
    VIEW_ALL = "View all contracts"



    def __init__(self, ui_helper, logic_api):
        self.ui_helper = ui_helper
        self.logic_api = logic_api
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
        self.ui_helper.print_line(f"        PHONE NUMBER:............{the_customer.phone}")
        self.ui_helper.print_line(f"        EMAIL:...................{the_customer.email}")
        self.ui_helper.print_line(f"        COUNTRY:.................{the_customer.work_area}")
        self.ui_helper.print_blank_line()


    def create_customer(self, ssn, header_str, error_msg =""):
        ''' Creates a new customer and passes it along to logic '''
        the_customer = Customer("", ssn, "", "", "", "", "")
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

        self.ui_helper.clear()
        self.ui_helper.print_header(header_str)
        self.view_customer_details(the_customer)
        self.ui_helper.print_blank_line()
        self.ui_helper.print_footer()
        print("Confirm changes? (y/n)")
        user_choice = input("Input: ")
        '''
        if user_choice in self.ui_helper.YES:
            self.logic_api.register_employee(emp)
            self.employee_has_been_registered(header_str, emp)
            return
        else:
            return'''


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

            return self.logic_api.get_customer(ssn), ssn

    
    def employee_for_contract(self, header_str, error_msg=""):
        ''' Gets employee for the contract '''
        pass


    def new_contract(self, header_str, error_msg=""):
        ''' Composite method for creating a contract'''
        the_customer, ssn = self.find_customer(header_str)
        if the_customer == None:    #If customer doesn't exists
            the_customer = self.create_customer(ssn)
        
        self.create_contract(the_customer, header_str)
    

    def create_contract(self, a_customer, header_str, error_msg=""):
        ''' Gets input from user and creates a new contract '''
        
            
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