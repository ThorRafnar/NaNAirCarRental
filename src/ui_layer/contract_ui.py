from model_layer.contract import Contract
from model_layer.customer import Customer

class ContractUI():
    CREATE = "Create new contract"
    FIND = "Find a contract"
    VIEW_ALL = "View all contracts"



    def __init__(self, ui_helper, logic_api, employee_ui, vehicle_ui):
        self.ui_helper = ui_helper
        self.logic_api = logic_api
        self.employee_ui = employee_ui
        self.vehicle_ui = vehicle_ui
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

                    elif self.options_dict[user_choice] == self.FIND:
                        contract_id = self.get_contract_id(header_str)
                        self.search_by_id(contract_id, header_str)
                        
                            
                    elif self.options_dict[user_choice] == self.VIEW_ALL:
                        self.list_all_contracts(header_str)

            else:
                error_msg = "Please select an option from the menu"


    def search_by_id(self, contract_id, header_str, error_msg=""):
        the_contract = self.logic_api.find_contract(contract_id)
        if the_contract != None: 
            self.view_contract(the_contract, header_str)
            return input("...")
        else:
            #self.contract_not_found(header_str)
            pass

    
    def get_contract_id(self, header_str):
        ''' Gets contract id from user '''
        self.ui_helper.clear()
        self.ui_helper.print_header(header_str)
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line("    Enter contract ID")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_footer()
        print()
        contract_id = input("Input: ")
        if contract_id.lower() == self.ui_helper.QUIT.lower():
            self.ui_helper.quit_prompt(header_str)
        elif contract_id.lower() == self.ui_helper.BACK.lower():
            return
        else:
            return contract_id


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


    def view_contract_details(self, the_contract):
        ''' '''
        currency = "Kr."
        the_vehicle = self.logic_api.find_vehicle(the_contract.vehicle_id)
        the_customer = self.logic_api.find_customer(the_contract.customer_ssn)
        the_employee = self.logic_api.find_employee(the_contract.employee_ssn)
        self.ui_helper.print_line(f"    Contract {the_contract.contract_id} details:")
        self.ui_helper.seperator()
        self.ui_helper.print_line("1. RENTAL VEHICLE")
        self.ui_helper.print_line("    Nan air rentals hereby agree to rent to Renter a vehicle,")
        self.ui_helper.print_line("    identified as follows:")
        self.ui_helper.print_blank_line()
        self.ui_helper.left_aligned_columns([f"           MAKE:   {the_vehicle.manufacturer}", f"MODEL:  {the_vehicle.model}"])
        self.ui_helper.print_blank_line()
        self.ui_helper.left_aligned_columns([f"           COLOR:  {the_vehicle.color}", f"YEAR:   {the_vehicle.year}"])
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line(f"        ID Nr:  {the_vehicle.id}")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line("(hereinafter referred to as “Rental Vehicle”).")
        self.ui_helper.seperator()
        self.ui_helper.print_line("2. RENTAL TERM")
        self.ui_helper.print_line("    The term of this rental contract runs from the date of pickup")
        self.ui_helper.print_line("    as indicated below, until the return of the vehicle to Owner")
        self.ui_helper.print_blank_line()
        self.ui_helper.left_aligned_columns([f"           START DATE: {the_contract.loan_date}", f"END DATE:  {the_contract.end_date}"])
        self.ui_helper.seperator()
        self.ui_helper.print_line("3. SCOPE OF USE")
        self.ui_helper.print_line("    The renter is limited to use the rental vehicle only in the city in ")
        #TODO Get city as well ---------------------------------------v
        self.ui_helper.print_line(f"    which it is rented, {the_vehicle.location}, and the general vicinity. The renter")
        self.ui_helper.print_line("    will not sublease or rent the rental vehicle to another person.")
        self.ui_helper.seperator()
        self.ui_helper.print_line("4. RENTAL FEES")
        self.ui_helper.print_line(f"    Rental vehicle is of class {the_vehicle.type}, which has a rental rate of:")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line(f"        RATE:      {self.logic_api.get_types_rate(the_vehicle.type)} {currency} per day")
        self.ui_helper.print_line(f"        PRICE:     {the_contract.base_price} {currency}")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line(f"    Failure to return the vehicle on time will result in an extra charge of")
        self.ui_helper.print_line(f"    20% in addition to the rate, per day")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line(f"        LATE FEES: {self.logic_api.get_types_rate(the_vehicle.type) * 1.2} {currency} per late day")
        self.ui_helper.seperator()
        self.ui_helper.print_line("5. SIGNATURE")
        self.ui_helper.print_line(f"    This vehicle rental agreement constitutes the entire agreement between the")
        self.ui_helper.print_line(f"    Parties with respect to this rental arrangement")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_centered_line_dash("<< CUSTOMER >>")
        self.ui_helper.print_blank_line()
        self.ui_helper.left_aligned_columns([f"     NAME:  {the_customer.name}", f"ADDRESS:  {the_customer.address}"])
        self.ui_helper.print_blank_line()
        self.ui_helper.left_aligned_columns([f"     EMAIL: {the_customer.email}", f"PHONE:   {the_customer.phone}"])
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line("   SIGNATURE:___________________________     DATE:________________")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_centered_line_dash("<< EMPLOYEE >>")
        self.ui_helper.print_blank_line()
        self.ui_helper.left_aligned_columns([f"     NAME:  {the_employee.name}", f"WORK AREA:  {the_employee.work_area}"])
        self.ui_helper.print_blank_line()
        self.ui_helper.left_aligned_columns([f"     EMAIL: {the_employee.email}", f"PHONE:   {the_employee.mobile_phone}"])
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line("   SIGNATURE:___________________________     DATE:________________")
        

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
            self.ui_helper.print_line(f"    Enter contract {date_type_str} date (DD/MM/YYYY)")
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
                error_msg = "Please enter a valid date (DD/MM/YYYY)"

    
    def get_vehicle_type(self, location, header_str, error_msg=""):
        ''' Displays all vehicle types in a given location and allows user to choose '''
        vehicle_types = self.logic_api.filter_by_region(location.country)
        vehicle_type_list = [(str(ind + 1), vtype) for ind, vtype in enumerate(vehicle_types)]       
        vehicle_type_dict = dict(vehicle_type_list)
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.ui_helper.print_line("Select vehicle type:")
            for line in vehicle_type_list:
                self.ui_helper.print_line(f"    {line[0]}. {line[1].name}")
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

    
    def choose_vehicle(self, start_date, end_date, location, a_vehicle_type, header_str, error_msg=""):
        ''' Lists all vehicles that are available for given dates, in a given location of a given type '''
        vehicle_list = self.logic_api.get_filtered_vehicle(start_date, end_date, location, a_vehicle_type)
        id_list = [vehicle.id for vehicle in vehicle_list ]
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.ui_helper.print_line("Enter vehicle ID to select")
            self.ui_helper.print_line("if nothing is chosen one will be selected automatically")
            self.ui_helper.print_blank_line()
            self.vehicle_ui.print_vehicle_list(vehicle_list)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            id_choice = input("Input: ")
            if id_choice in id_list:
                return id_choice
            elif id_choice == "":
                return id_list[0]
            elif id_choice.lower() == self.ui_helper.QUIT.lower():
                self.ui_helper.quit_prompt(header_str)
            elif id_choice.lower() == self.ui_helper.BACK.lower():
                return id_choice
            else:
                error_msg = "Please select a vehicle id from the list"


    def create_contract(self, the_customer, the_employee, header_str, error_msg=""):
        ''' Gets input from user and creates a new contract '''
        the_contract = Contract(None, the_customer.ssn, the_employee.ssn, "", "", "", "", "")
        the_contract.loan_date = self.get_date("start", header_str)
        the_contract.end_date = self.get_date("end", header_str)
        location = self.get_location(header_str)
        vehicle_type = self.get_vehicle_type(location, header_str)
        the_vehicle_id = self.choose_vehicle(the_contract.loan_date, the_contract.end_date, location, vehicle_type, header_str)
        if the_vehicle_id.lower() == self.ui_helper.BACK.lower():
            return
        the_contract.vehicle_id = the_vehicle_id
        self.view_contract(the_contract, header_str)
        self.logic_api.create_new_contract(the_contract)

        
    def view_contract(self, the_contract, header_str, error_msg =""):
        options_list = [("1", "Bite me!")]
        while True:
            old_width = self.ui_helper.width
            self.ui_helper.width = 84                   #Sets ui window width to about A4 size
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.view_contract_details(the_contract)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            self.ui_helper.width = old_width            #Resets ui window width
            print(error_msg)
            user_choice = self.ui_helper.get_user_menu_choice(options_list)
            if user_choice.lower() == self.ui_helper.BACK.lower():
                return
            elif user_choice.lower() == self.ui_helper.QUIT.lower():
                self.ui_helper.quit_prompt(header_str)
            else:
                return user_choice
    
            
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


    def list_all_contracts(self, header_str):
        ''' Lists all contracts in a compact view and allows user to choose one to view '''
        contracts_list = self.logic_api.get_all_contracts()
        self.ui_helper.clear()
        self.ui_helper.print_header(header_str)
        self.ui_helper.print_line("    Enter contract ID for more information")
        self.ui_helper.print_blank_line()
        contract_header = ["<< ID >>", "<< STATUS >>", "<< TOTAL PRICE >>", "<< TYPE >>", "<< VEHICLE >>", "<< NAME >>", "<< SSN >>", "<< START DATE >>", "<< RETURN DATE >>"]
        self.ui_helper.n_columns(contract_header)
        for contract in contracts_list:
            self.compact_contract(contract)
        self.ui_helper.print_footer()
        user_choice = input("Input: ")
        if user_choice.lower() == self.ui_helper.BACK.lower():
            return
        elif user_choice.lower() == self.ui_helper.QUIT.lower():
            self.ui_helper.quit_prompt(header_str)
        else:
            self.search_by_id(user_choice, header_str)


    def compact_contract(self, a_contract):
        ''' Displays contract information in a compact format '''
        a_vehicle = self.logic_api.find_vehicle(a_contract.vehicle_id)
        a_customer = self.logic_api.find_customer(a_contract.customer_ssn)
        contract_column = [a_contract.contract_id, a_contract.status, a_contract.total, a_vehicle.type, f"{a_vehicle.manufacturer} {a_vehicle.model}", a_customer.name, a_customer.ssn, a_contract.loan_date, a_contract.end_date]
        self.ui_helper.n_columns(contract_column)


        '''
        Upplýsingar um leigjanda.
        Dagsetning á gerð samnings.
        Upplýsingar um farartækið.
        Gildistíma leigusamnings og land.
        Dagsetning og staðsetning á afhendingu farartækis (skráð við afhendingu).
        Dagsetning og staðsetning á móttöku farartækis (skráð við skil).
        '''