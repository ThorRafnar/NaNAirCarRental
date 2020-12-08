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
                        contract_list = self.logic_api.get_all_contracts()
                        self.list_contracts(contract_list, header_str)

            else:
                error_msg = "Please select an option from the menu"


    def search_by_id(self, contract_id, header_str, error_msg=""):
        the_contract = self.logic_api.find_contract(contract_id)
        if the_contract != None: 
            #self.view_contract(the_contract, header_str)
            self.single_contract_options(the_contract, header_str)
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


    def single_contract_options(self, a_contract, header_str, error_msg =""):
        ''' Shows a contract in a compacted view and allows user to choose options, what to do '''
        a_customer = self.logic_api.find_customer(a_contract.customer_ssn)
        a_vehicle = self.logic_api.find_vehicle(a_contract.vehicle_id)
        a_employee = self.logic_api.find_employee(a_contract.employee_ssn)

        change_start = "Change start date"
        change_end = "Change end date"
        change_vehicle = "Change vehicle"
        terminate = "Terminate contract"
        printable = "View printable contract"

        contract_options_dict = {
            "1": change_start,
            "2": change_end,
            "3": change_vehicle,
            "4": terminate,
            "5": printable
        }
        contract_options_list = self.ui_helper.dict_to_list(contract_options_dict)
        options_string = "Please select an option"
        while True:

            ### printing contract info and menu ###
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.ui_helper.seperator()
            self.ui_helper.print_line(f"    << CONTRACT ID {a_contract.contract_id} INFORMATION >>")
            self.ui_helper.print_blank_line()
            self.ui_helper.left_aligned_columns([f"       START DATE: {a_contract.loan_date}", f"END DATE: {a_contract.end_date}", f"LOCATION: {a_vehicle.location}", f"STATUS: {a_contract.status}"])
            self.ui_helper.print_blank_line()
            self.ui_helper.left_aligned_columns([f"       RATE: {self.logic_api.get_types_rate(a_vehicle.type)}",f"BASE PRICE: {a_contract.base_price}", f"TOTAL PRICE: {a_contract.total}", "REGISTRATION DATE: N/A"])
            self.ui_helper.print_blank_line()
            self.ui_helper.seperator()
            self.ui_helper.print_line("    << CUSTOMER >>")
            self.ui_helper.print_blank_line()
            self.ui_helper.left_aligned_columns([f"       NAME: {a_customer.name}", f"SSN: {a_customer.ssn}", f"TEL: {a_customer.phone}", f"EMAIL: {a_customer.email}"])
            self.ui_helper.print_blank_line()
            self.ui_helper.left_aligned_columns([f"       ADDRESS: {a_customer.address}",f"POSTAL: {a_customer.postal_code}", f"COUNTRY: {a_customer.country}", ""])
            self.ui_helper.print_blank_line()
            if a_customer.licenses == "None":
                self.ui_helper.left_aligned_columns([f"       DRIVING LICENCE [ ]", "DIVING LICENCE [ ]", "", ""])
            else:
                if "Driving" in a_customer.licenses and "Diving" in a_customer.licenses:
                    self.ui_helper.left_aligned_columns([f"       DRIVING LICENCE [x]", "DIVING LICENCE [x]", "", ""])
                elif "Driving" in a_customer.licenses and "Diving" not in a_customer.licenses:
                    self.ui_helper.left_aligned_columns([f"       DRIVING LICENCE [x]", "DIVING LICENCE [ ]", "", ""])
                elif "Diving" in a_customer.licenses and "Driving" not in a_customer.licenses:
                    self.ui_helper.left_aligned_columns([f"       DRIVING LICENCE [ ]", "DIVING LICENCE [x]", "", ""])
                else:
                    self.ui_helper.print_blank_line()
            self.ui_helper.print_blank_line()
            self.ui_helper.seperator()
            self.ui_helper.print_line("    << VEHICLE >>")
            self.ui_helper.print_blank_line()
            self.ui_helper.left_aligned_columns([f"       MAKE: {a_vehicle.manufacturer}", f"MODEL: {a_vehicle.model}", f"COLOR: {a_vehicle.color}", f"YEAR: {a_vehicle.year}"])
            self.ui_helper.print_blank_line()
            self.ui_helper.left_aligned_columns([f"       TYPE: {a_vehicle.type}",f"ID: {a_vehicle.id}", "", ""])
            self.ui_helper.print_blank_line()
            self.ui_helper.seperator()
            self.ui_helper.print_line("    << EMPLOYEE >>")
            self.ui_helper.print_blank_line()
            self.ui_helper.left_aligned_columns([f"       NAME: {a_employee.name}", f"SSN: {a_employee.ssn}", f"TEL: {a_employee.mobile_phone}", f"EMAIL: {a_employee.email}"])
            self.ui_helper.print_blank_line()
            self.ui_helper.seperator()
            self.ui_helper.print_blank_line()
            self.ui_helper.print_options(contract_options_list, options_string)
            self.ui_helper.print_footer()

            ### input decision making ###
            user_choice = self.ui_helper.get_user_menu_choice(contract_options_list)
            if user_choice != None:
                if user_choice.lower() == self.ui_helper.QUIT.lower():
                    self.ui_helper.quit_prompt(header_str)
                elif user_choice.lower() == self.ui_helper.BACK.lower():
                    return
                else:
                    if contract_options_dict[user_choice] == change_start:
                        _new_start = self.get_user_input("Enter new start date (DD/MM/YYYY)", header_str)

                    elif contract_options_dict[user_choice] == change_end:
                        _new_end = self.get_user_input("Enter new end date (DD/MM/YYYY)", header_str)

                    elif contract_options_dict[user_choice] == change_vehicle:
                        pass

                    elif contract_options_dict[user_choice] == terminate:
                        pass

                    elif contract_options_dict[user_choice] == printable:
                        self.view_contract(a_contract, header_str)

            else:
                error_msg = "Please select an option from the menu"


    def get_user_input(self, prompt_str, header_str):
        ''' Asks user for input and returns it '''
        self.ui_helper.clear()
        self.ui_helper.print_header(header_str)
        self.ui_helper.print_line(prompt_str)
        self.ui_helper.print_blank_line()
        self.ui_helper.print_footer()
        print()
        return input("Input: ")



    def view_customer_details(self, the_customer):
        ''' Shows the attributes of a customer'''
        self.ui_helper.print_line(f"        NAME:....................{the_customer.name}")
        self.ui_helper.print_line(f"        SOCIAL SECURITY NR:......{the_customer.ssn}")
        self.ui_helper.print_line(f"        ADDRESS:.................{the_customer.address}")
        self.ui_helper.print_line(f"        POSTAL CODE:.............{the_customer.postal_code}")
        self.ui_helper.print_line(f"        PHONE NUMBER:...........{the_customer.phone}")
        self.ui_helper.print_line(f"        EMAIL:...................{the_customer.email}")
        self.ui_helper.print_line(f"        COUNTRY:.................{the_customer.country}")
        self.ui_helper.print_line(f"        LICENCES:................{the_customer.licenses}")
        self.ui_helper.print_blank_line()


    def view_contract_details(self, the_contract):
        ''' Printable version of the contract '''
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
        self.ui_helper.print_line("  SIGNATURE:___________________________     DATE:________________")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_centered_line_dash("<< EMPLOYEE >>")
        self.ui_helper.print_blank_line()
        self.ui_helper.left_aligned_columns([f"     NAME:  {the_employee.name}", f"WORK AREA:  {the_employee.work_area}"])
        self.ui_helper.print_blank_line()
        self.ui_helper.left_aligned_columns([f"     EMAIL: {the_employee.email}", f"PHONE:   {the_employee.mobile_phone}"])
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line("  SIGNATURE:___________________________     DATE:________________")
        self.ui_helper.seperator()
        

    def create_customer(self, ssn, header_str, error_msg =""):
        ''' Creates a new customer and passes it along to logic '''
        the_customer = Customer("", ssn, "", "", ".", "", "", "", "")
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
                    return

                elif attr_value.lower() == self.ui_helper.QUIT.lower():
                    self.ui_helper.quit_prompt(header_str)
                    continue

                else:
                    setattr(the_customer, attr_key, attr_value)     #Sets attribute to input
                    break
        
        licences = self.get_licences(the_customer, header_str)                 #Gets licence(s) for the customer
        setattr(the_customer, "licenses", licences) 

        self.logic_api.add_customer(the_customer)
        return the_customer


    def get_licences(self, a_customer, header_str, error_msg=""):
        ''' Displays valid licences, numbered and asks user to inpur which licences the customer has, then adds them as an attribute, seperated by a dash (-)'''
        valid_licences= self.logic_api.licenses_options_list()
        valid_licence_dict = { str(ind + 1): licence for ind, licence in enumerate(valid_licences) }   #To convert input to licence easily
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_line("Select which licences the customer has")
            self.ui_helper.print_line("If the customer has more than one, enter them all, seperated by a dash(-)")
            self.ui_helper.print_line("If the customer has none, input nothing and press enter")
            self.ui_helper.print_blank_line()
            for key, val in valid_licence_dict.items():
                self.ui_helper.print_line(f"    {key}: {val} licence")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            user_choice = input("Input: ")
            if user_choice == "":
                setattr(a_customer, "license_type", "None")
            elif user_choice.lower() == self.ui_helper.QUIT.lower():
                self.ui_helper.quit_prompt(header_str)
            elif user_choice.lower() == self.ui_helper.BACK.lower():
                return 
            else:
                licence_list = []
                licence_keys = user_choice.split("-")
                for key in licence_keys:
                    if key in valid_licence_dict:
                        licence_list.append(valid_licence_dict[key])
                    else:
                        error_msg = "Please enter numbers seperated by a dash(-) to select licences"
                        break
                
                return "-".join(licence_list)
                




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

        self.create_contract(the_customer, the_employee, header_str)              #Creates contract with the customer

    
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

    
    def get_vehicle_type(self, start_date, end_date, location, header_str, error_msg=""):
        ''' Displays all vehicle types in a given location and allows user to choose '''
        vehicle_types = self.logic_api.filter_by_region(location.country)                                                                     
        vehicle_type_list = [ (str(ind + 1), vtype) for ind, vtype in enumerate(vehicle_types) if (self.logic_api.get_filtered_vehicle(start_date, end_date, location, vtype) != []) ]       
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
                error_msg = "Please select a vehicle type from the list"

    
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
        vehicle_type = self.get_vehicle_type(the_contract.loan_date, the_contract.end_date, location, header_str)
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


    def list_contracts(self, contract_list, header_str):
        ''' Lists all contracts in a compact view and allows user to choose one to view '''
        self.ui_helper.clear()
        self.ui_helper.print_header(header_str)
        self.ui_helper.print_line("    Enter contract ID for more information")
        self.ui_helper.print_blank_line()
        contract_header = ["<< ID >>", "<< STATUS >>", "<< TOTAL PRICE >>", "<< TYPE >>", "<< VEHICLE >>", "<< NAME >>", "<< SSN >>", "<< START DATE >>", "<< RETURN DATE >>"]
        self.ui_helper.n_columns(contract_header)
        for contract in contract_list:
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


    def pick_up_vehicle(self, header_str, error_msg=""):
        ''' Menu for when a customer is picking up a vehicle, asks for ssn and goes through the steps '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.ui_helper.print_line("    Enter customer ssn:")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = input("Input: ")
            if user_choice.lower() == self.ui_helper.BACK.lower():
                return
            elif user_choice.lower() == self.ui_helper.QUIT.lower():
                self.ui_helper.quit_prompt(header_str)
            ssn = self.ui_helper.ssn_formatter(user_choice)
            if ssn == None:
                error_msg = "Please enter a valid social security number (DDMMYY-NNNM)"
                continue
            
            else:
                the_customer = self.logic_api.find_customer(ssn)

                if the_customer != None:
                    conf_choice = self.confirm_customer(the_customer, header_str)
                    if conf_choice.lower() in self.ui_helper.YES:                   #If the customer is confirmed
                        
                        ### The contracts <3 ###
                        contract_list = self.logic_api.view_customer_contracts(ssn)
                        if contract_list == []:
                            pass
                            #No contract for this customer today

                        else:
                            returning_choice = self.customer_vehicle_selection(contract_list, header_str)   #To return to menu if user finished a task
                            if returning_choice == self.ui_helper.BACK.lower():
                                return

                    else:
                        continue

                else:                       #If customer is not found
                    error_msg = "No customer with this ssn found!"
                    continue


    def customer_vehicle_selection(self, contract_list, header_str, error_msg=""):
        ''' Displays vehicles in a list and allows user to select (A)ll or one at a time to lend them out '''
        activate_list = []
        undo_list = []
        activate_all = "a"
        save = "s"
        undo = "u"
        while True:
            vehicle_id_dict =  { contract.vehicle_id: contract for contract in contract_list }      #Contains vehicle id as key and contract as value, updates if user activates a contract
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.ui_helper.print_line(f"    ({activate_all.upper()})ll: Activate all contracts")
            self.ui_helper.print_line("        --OR--")
            self.ui_helper.print_line("    Enter vehicle ID to activate contract")
            self.ui_helper.print_blank_line()
            if contract_list != []:
                self.ui_helper.print_centered_line_dash("<< PENDING >>")
                self.list_vehicle_and_contract_info(contract_list)
                self.ui_helper.print_blank_line()
            if activate_list != []:
                self.ui_helper.print_centered_line_dash("<< TO ACTIVATE >>")
                self.list_vehicle_and_contract_info(activate_list)
                self.ui_helper.print_blank_line()
                self.ui_helper.print_line(f"    ({save.upper()})ave: Save changes")
            if undo_list != []:
                self.ui_helper.print_line(f"    ({undo.upper()})ndo: Undo last change")
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = input("Input: ")
            if user_choice.lower() == self.ui_helper.QUIT.lower():
                self.ui_helper.quit_prompt(header_str)

            elif user_choice.lower() == self.ui_helper.BACK.lower():
                return

            elif user_choice.lower() == undo:

                if isinstance(undo_list[-1], list):             #if the last item in undo list is a list
                    contract_list.extend(undo_list[-1])
                    for contract in undo_list[-1]:
                        activate_list.remove(contract)
                    undo_list.pop()

                else:                                           #if it is not
                    contract_list.append(undo_list[-1])
                    activate_list.remove(undo_list[-1])
                    undo_list.pop()
            
            elif user_choice.lower() == save:                   #Saves changes through logic API
                for contract in activate_list:
                    self.logic_api.change_contract_status(contract.contract_id, "Active")
                self.contracts_activated(header_str)
                return self.ui_helper.BACK.lower()              #Makes user return to staff type menu if they finish the task

            else:
                if user_choice.lower() == activate_all:
                    activate_list.extend(contract_list)     #in case user has added some and then wants to add all
                    undo_list.append(contract_list)         #Appends list to undo, so user can undo all changes at once
                    contract_list = []
                
                elif user_choice in vehicle_id_dict:
                    activate_list.append(vehicle_id_dict[user_choice])
                    undo_list.append(vehicle_id_dict[user_choice])
                    contract_list.remove(vehicle_id_dict[user_choice])
                else:
                    error_msg = "Please select an option from the menu"
                    continue
                
    
    def contracts_activated(self, header_str):
        ''' Confirm screen to tell user contracts have been activated '''
        self.ui_helper.clear()
        self.ui_helper.print_header(header_str)
        self.ui_helper.print_line("Contract(s) have been activated")
        self.ui_helper.print_line("Press enter to return")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_footer()
        print()
        return input("Input: ")
    
    def list_vehicle_and_contract_info(self, contract_list):
        ''' Lists info about vehicles and rates for pickup '''
        header_list = ["<< VEHICLE ID >>", "<< TYPE >>", "<< MAKE >>", "<< MODEL >>", "<< RETURN DATE >>", "<< RATE >>", "<< PRICE >>", "<< CONTRACT ID >>"]
        self.ui_helper.n_columns(header_list)
        for contract in contract_list:
            vehicle = self.logic_api.find_vehicle(contract.vehicle_id)
            self.logic_api.get_types_rate(vehicle.type)
            self.ui_helper.n_columns([vehicle.id, vehicle.type, vehicle.manufacturer, vehicle.model, contract.end_date, self.logic_api.get_types_rate(vehicle.type), contract.base_price, contract.contract_id])


    def returns_menu(self, header_str):
        ''' Guides user through returning a vehicle '''
        contract_list = []
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header(header_str)
            self.ui_helper.print_line("Returning vehicle(s), enter vehicle ID:")
            self.ui_helper.print_blank_line()
            if contract_list != []:
                self.ui_helper.print_centered_line_dash("<< RETURNING VEHICLES >>")
                self.list_vehicle_and_contract_info(contract_list)
                self.ui_helper.print_blank_line()
                self.ui_helper.print_line(f"    ({self.ui_helper.SAVE.upper()})ave: Save changes")
                self.ui_helper.print_line(f"    ({self.ui_helper.UNDO.upper()})ndo: Undo last change")
            else:
                self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print()
            user_choice = input("Input: ")
            if user_choice.lower() == self.ui_helper.QUIT.lower():
                self.ui_helper.quit_prompt(header_str)

            elif user_choice.lower() == self.ui_helper.BACK.lower():
                return

            elif user_choice.lower() == self.ui_helper.SAVE:
                pass #TODO Register contracts as returned

            elif user_choice.lower() == self.ui_helper.UNDO:
                contract_list.pop()

            else:
                contracts = self.logic_api.get_contracts_by_attr(["vehicle_id", user_choice])
                if contracts != []:
                    contract_list.extend(contracts)

                else:               #If vehicle contract doesn't exist
                    self.contract_not_found(header_str)

    
    def contract_not_found(self, header_str):
        ''' Displays that no contract was found, returning after user presses enter, not saving input '''
        self.ui_helper.clear()
        self.ui_helper.print_header(header_str)
        self.ui_helper.print_line("No contract found")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_footer()
        print()
        _x = input("Input: ")
        return 