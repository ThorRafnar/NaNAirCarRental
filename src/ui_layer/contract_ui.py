from model_layer.contract import Contract
from model_layer.customer import Customer

class ContractUI():
    # Constants
    CREATE = "Create new contract"
    FIND = "Find a contract"
    VIEW_ALL = "View all contracts"
    VIEW_BY_CUSTOMER = "View contracts by customer"



    def __init__(self, ui_helper, logic_api, employee_ui, vehicle_ui):
        self.ui_helper = ui_helper
        self.logic_api = logic_api
        self.employee_ui = employee_ui
        self.vehicle_ui = vehicle_ui
        self.options_dict = {           # Only office employees have access to contract section // Airport employees have inderect access through pickups and returns 
            "1": self.CREATE, 
            "2": self.FIND, 
            "3": self.VIEW_ALL,
            "4": self.VIEW_BY_CUSTOMER
        }

# Contract menu section   
    def show_options(self, error_msg=""):
        ''' shows available options and allows user to select '''
        options_list = self.ui_helper.dict_to_list(self.options_dict)
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_options(options_list, "Select task")
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = self.ui_helper.get_user_menu_choice(options_list)
            if user_choice != None:

                if user_choice.lower() == self.ui_helper.BACK:
                    return

                elif user_choice.lower() == self.ui_helper.QUIT:
                    self.ui_helper.quit_prompt()

                else:
                    
                    if self.options_dict[user_choice] == self.CREATE:
                        self.new_contract()                      

                    elif self.options_dict[user_choice] == self.FIND:
                        self.search_by_id()
                        
                            
                    elif self.options_dict[user_choice] == self.VIEW_ALL:
                        contract_list = self.logic_api.get_all_contracts()
                        self.list_contracts(contract_list)

                    elif self.options_dict[user_choice] == self.VIEW_BY_CUSTOMER:
                        self.view_contracts_by_customer()

            else:
                error_msg = "Please select an option from the menu"
    

    def returns_menu(self):
        ''' Guides user through returning a vehicle '''
        returning_contract = None
        options_list = [("R", "rentable"),("W", "workshop")]
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line("Returning vehicle, enter vehicle ID:")
            self.ui_helper.print_blank_line()
            if returning_contract != None:
                self.ui_helper.print_centered_line_dash("<< RETURNING VEHICLE >>")
                self.list_vehicle_and_contract_info([returning_contract])
                self.ui_helper.print_blank_line()
                self.ui_helper.print_options(options_list, "What is the status of the returning vehicle?")
            else:
                self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print()
            user_choice = input("Input: ")

            if user_choice.lower() == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()

            elif user_choice.lower() == self.ui_helper.BACK:
                return

            elif user_choice.lower() == "r":
                self.logic_api.change_contract_status(returning_contract.contract_id, "returned")
                self.logic_api.change_vehicle_condition(returning_contract.vehicle_id, "rentable")
                self.vehicle_has_been_returned()
                return

            elif user_choice.lower() == "w":
                self.logic_api.change_contract_status(returning_contract.contract_id, "returned")
                self.logic_api.change_vehicle_condition(returning_contract.vehicle_id, "workshop")
                self.vehicle_has_been_returned()
                return

            else:
                contract = self.logic_api.get_active_contract(user_choice, self.ui_helper.user_location)
                if contract != None:
                    returning_contract = contract

                else:               #If vehicle contract doesn't exist
                    self.contract_not_found()
# End of contract menu section

# Start of new contract section
    def new_contract(self, error_msg=""):
        ''' Composite method for creating a contract'''
        the_customer, ssn = self.find_customer()
        if ssn == None: 
            return

        if the_customer == None:    #If customer doesn't exists
            the_customer = self.create_customer(ssn)    #Creates new customer
        
        if the_customer == None:
            return
    
        confirm = self.confirm_customer(the_customer)             #Asks user to confirm

        if confirm.lower() in self.ui_helper.NO:
            the_customer = self.modify_customer(the_customer)
            if the_customer == None:                            #If user backs while creating customer
                return

        elif confirm.lower() == self.ui_helper.BACK:
            return

        elif confirm.lower() == self.ui_helper.QUIT:
            self.ui_helper.quit_prompt()

        the_employee, ssn = self.employee_for_contract() 

        if ssn == None:
            return

        if the_employee == None:                                    #If emp doesn't exists, create it
            self.employee_ui.create_employee(ssn)
            the_employee = self.logic_api.find_employee(ssn)

        conf = self.confirm_employee(the_employee)
        if conf.lower() not in self.ui_helper.YES:
            return

        self.create_contract(the_customer, the_employee)              #Creates contract with the customer


    def create_contract(self, the_customer, the_employee, error_msg=""): # This function is called in line 103
        ''' Gets input from user and creates a new contract, continues making contract with the selected
        customer and emplpoyee '''
        the_contract = Contract(None, the_customer.ssn, the_employee.ssn, "", "", "")
        the_contract.loan_date = self.get_date("start")

        if the_contract.loan_date == None:
            return

        the_contract.end_date = self.get_date("end")

        if the_contract.end_date == None:
            return

        location = self.get_location()
        vehicle_type = self.get_vehicle_type(the_contract.loan_date, the_contract.end_date, location)
        the_vehicle_id = self.choose_vehicle(the_contract.customer_ssn, the_contract.loan_date, the_contract.end_date, location, vehicle_type)
        if the_vehicle_id.lower() == self.ui_helper.BACK.lower():
            return

        the_contract.vehicle_id = the_vehicle_id
        self.single_contract_options(the_contract)
        self.logic_api.create_new_contract(the_contract)

    
    def get_licences(self, a_customer, error_msg=""): 
        ''' Displays valid licences, numbered and asks user to inpur which licences the customer has, then adds them as an attribute, seperated by a dash (-)'''
        valid_licences= self.logic_api.licenses_options_list()
        valid_licence_dict = { str(ind + 1): licence for ind, licence in enumerate(valid_licences) }   #To convert input to licence easily
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_blank_line()
            self.ui_helper.print_line("Select which licences the customer has")
            self.ui_helper.print_line("If the customer has more than one, enter them all, seperated by a dash(-)")
            self.ui_helper.print_line("If the customer has none, input 0")
            self.ui_helper.print_blank_line()
            for key, val in valid_licence_dict.items():
                self.ui_helper.print_line(f"    {key}: {val} licence")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            user_choice = input("Input: ")

            if user_choice.lower() == "0":
                return "None"

            elif user_choice.lower() == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()

            elif user_choice.lower() == self.ui_helper.BACK:
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

# End of new contract section

# Start of find contract section

    def search_by_id(self):
        contract_id = self.get_contract_id()

        if contract_id != None:
            the_contract = self.logic_api.find_contract(contract_id)
            if the_contract != None: 
                self.single_contract_options(the_contract)
                return 

            else:
                #self.contract_not_found(header_str)
                pass

        else:
            return
    
    def get_contract_id(self):
        ''' Gets contract id from user '''
        self.ui_helper.clear()
        self.ui_helper.print_header()
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line("    Enter contract ID")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_footer()
        print()
        contract_id = input("Input: ")
        if contract_id.lower() == self.ui_helper.QUIT:
            self.ui_helper.quit_prompt()

        elif contract_id.lower() == self.ui_helper.BACK:
            return

        else:
            return contract_id
    


# End of find contract section

# Start of view all contract functions

    def list_contracts(self, contract_list, error_msg=""):
        ''' Lists all contracts in a compact view and allows user to choose one to view '''
        self.ui_helper.clear()
        self.ui_helper.print_header()
        self.ui_helper.print_line("    Enter contract ID for more information")
        self.ui_helper.print_blank_line()
        contract_header = ["<< ID >>", "<< STATUS >>", "<< TOTAL PRICE >>", "<< TYPE >>", "<< VEHICLE >>", "<< NAME >>", "<< SSN >>", "<< START DATE >>", "<< RETURN DATE >>"]
        self.ui_helper.n_columns(contract_header)
        for contract in contract_list:
            self.compact_contract(contract)
        self.ui_helper.print_blank_line()
        self.ui_helper.print_footer()
        print(error_msg)
        user_choice = input("Input: ")
        if user_choice.lower() == self.ui_helper.BACK:
            return
        elif user_choice.lower() == self.ui_helper.QUIT:
            self.ui_helper.quit_prompt()
        else:
            the_contract = self.logic_api.find_contract(user_choice)
            if the_contract != None:
                self.single_contract_options(the_contract)      # This function is in view contract section

            else:
                error_msg = "Please enter a valid contract ID"
# End of view all contract functions

# Start of view contract by customer sections

    def view_contracts_by_customer(self, error_msg=""):
        ''' Asks for ssn and displays contracts for that customer, if any '''
        while True:
            customer, ssn = self.find_customer() # This function is in customer functions section
            if ssn == None:
                return

            if customer == None:
                self.customer_not_found()
                return

            else:
                contracts = self.logic_api.view_customer_contracts(customer.ssn) 

                if len(contracts) == 0:
                    self.contract_not_found()
                    return

                else:    
                    self.list_contracts(contracts)
                    return

# End of view contract by customer sections

# View contract functions // Functions that are used to print out contracts // Called in find contract and new contract sections

    def single_contract_options(self, a_contract, error_msg =""):
        ''' Shows a contract in a compacted view and allows user to choose options to change it '''
        change_start = "Change start date"
        change_end = "Change end date"
        change_vehicle = "Change vehicle"
        terminate = "t"
        printable = "p"

        if a_contract.status.lower() == "pending":
            contract_options_dict = {
                "1": change_start,
                "2": change_end,
                "3": change_vehicle,
            }
        elif a_contract.status.lower() == "active":
            contract_options_dict = {
                "2": change_end
            }

        else:
            contract_options_dict = {}


        contract_options_list = self.ui_helper.dict_to_list(contract_options_dict)
        options_string = "Please select an option"
        undo_list = []
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.view_full_display_contract(a_contract)
            self.ui_helper.print_options(contract_options_list, options_string)
            self.ui_helper.print_blank_line()
            
            if a_contract.status.lower() == "pending":                                                      #If contract has not started, we can terminate it
                self.ui_helper.print_line(f"    ({terminate.upper()})erminate: Terminate contract")
            else:
                self.ui_helper.print_blank_line()                                                           #Otherwise the customer must PAY

            self.ui_helper.print_line(f"    ({printable.upper()})rint: View contract in a printer friendly format")
            self.ui_helper.print_line(f"    ({self.ui_helper.SAVE.upper()})ave: Save changes")

            if undo_list == []:
                self.ui_helper.print_blank_line()
            else:
                self.ui_helper.print_line(f"    ({self.ui_helper.UNDO.upper()})ndo: Undo last change")

            self.ui_helper.print_footer()

            ### input decision making ###
            print(error_msg)
            error_msg =""
            user_choice = input("Input: ")
            if user_choice != None:

                if user_choice.lower() == self.ui_helper.QUIT:
                    self.ui_helper.quit_prompt()

                elif user_choice.lower() == self.ui_helper.BACK:
                    return

                elif user_choice.lower() == self.ui_helper.UNDO:
                    setattr(a_contract, undo_list[-1][0], undo_list[-1][1])

                elif user_choice.lower() == self.ui_helper.SAVE:
                    self.logic_api.change_contract(a_contract)
                    return

                elif user_choice.lower() == terminate and a_contract.status.lower() == "pending":
                        terminated = self.terminate_contract(a_contract)
                        if terminated:
                            return
                
                elif user_choice.lower() == printable:
                    self.print_contract(a_contract)

                elif user_choice.lower() in contract_options_dict:       #Actual options
                    if contract_options_dict[user_choice] == change_start:
                        undo_list.append(self.change_contract_start_date(a_contract))

                    elif contract_options_dict[user_choice] == change_end:
                        undo_list.append(self.change_contract_end_date(a_contract))

                    elif contract_options_dict[user_choice] == change_vehicle:
                        undo_list.append(self.change_contract_vehicle(a_contract))

                else:
                    error_msg = "Please select an option from the menu"
                        
                    
            else:
                error_msg = "Please select an option from the menu"

    def view_full_display_contract(self, a_contract):
        ''' Shows full display view of contract, for single contract menu '''
        a_customer = self.logic_api.find_customer(a_contract.customer_ssn)
        a_vehicle = self.logic_api.find_vehicle(a_contract.vehicle_id)
        a_employee = self.logic_api.find_employee(a_contract.employee_ssn)
        self.ui_helper.seperator()
        self.ui_helper.print_line(f"    << CONTRACT ID {a_contract.contract_id} INFORMATION >>")
        self.ui_helper.print_blank_line()
        self.ui_helper.left_aligned_columns([f"       START DATE: {a_contract.loan_date}", f"END DATE: {a_contract.end_date}", f"LOCATION: {a_vehicle.location}", f"STATUS: {a_contract.status}"])
        self.ui_helper.print_blank_line()
        self.ui_helper.left_aligned_columns([f"       RATE: {self.logic_api.get_types_rate(a_vehicle.type)}",f"BASE PRICE: {a_contract.base_price}", f"TOTAL PRICE: {a_contract.total}", f"REGISTRATION DATE: {a_contract.contract_created}"])
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



    def customer_change_view(self, customer):
        ''' Displays Attributes of a customer and indices to change each attribute '''
        self.ui_helper.print_line(f"        NAME:....................{customer.name}")
        self.ui_helper.print_line(f"        SOCIAL SECURITY NR:......{customer.ssn}")
        self.ui_helper.print_line(f"    1.  ADDRESS:.................{customer.address}")
        self.ui_helper.print_line(f"    2.  POSTAL CODE:.............{customer.postal_code}")
        self.ui_helper.print_line(f"    3.  PHONE NUMBER:...........{customer.phone}")
        self.ui_helper.print_line(f"    4.  EMAIL:...................{customer.email}")
        self.ui_helper.print_line(f"    5.  COUNTRY:.................{customer.country}")
        self.ui_helper.print_line(f"        LICENCES:................{customer.licenses}")
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
        self.ui_helper.print_line("    The renter is limited to use the rental vehicle only in the city in")
        self.ui_helper.print_line(f"    which it is rented, {the_vehicle.location}, {self.logic_api.find_destination(self.logic_api.city_to_iata(the_vehicle.location)).country}, and the general")
        self.ui_helper.print_line("    vicinity. The renter will not sublease or rent the rental vehicle")
        self.ui_helper.print_line("    to another person.")
        self.ui_helper.seperator()
        self.ui_helper.print_line("4. RENTAL FEES")
        self.ui_helper.print_line(f"    Rental vehicle is of class {the_vehicle.type}, which has a rental rate of:")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line(f"        RATE:      {self.logic_api.get_types_rate(the_vehicle.type)} {currency} per day")
        self.ui_helper.print_line(f"        PRICE:     {the_contract.base_price} {currency}")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line(f"    Failure to return the vehicle on time will result in an extra")
        self.ui_helper.print_line(f"    charge of 20% in addition to the rate, per day")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line(f"        LATE FEES: {self.logic_api.get_types_rate(the_vehicle.type) * 1.2} {currency} per late day")
        self.ui_helper.seperator()
        self.ui_helper.print_line("5. SIGNATURE")
        self.ui_helper.print_line(f"    This vehicle rental agreement constitutes the entire agreement")
        self.ui_helper.print_line(f"    between the Parties with respect to this rental arrangement")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line(f"        THIS CONTRACT WAS REGISTERED ON {the_contract.contract_created}")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_centered_line_dash("<< CUSTOMER >>")
        self.ui_helper.print_blank_line()
        self.ui_helper.left_aligned_columns([f"     NAME:  {the_customer.name}", f"ADDRESS:  {the_customer.address}"])
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line(f"  EMAIL: {the_customer.email}")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line(f"  PHONE:   {the_customer.phone}")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line("  SIGNATURE:___________________________     DATE:________________")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_centered_line_dash("<< EMPLOYEE >>")
        self.ui_helper.print_blank_line()
        self.ui_helper.left_aligned_columns([f"     NAME:  {the_employee.name}", f"WORK AREA:  {the_employee.work_area}"])
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line(f"  EMAIL: {the_employee.email}")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line(f"  PHONE:   {the_employee.mobile_phone}")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line("  SIGNATURE:___________________________     DATE:________________")
        self.ui_helper.seperator()

    def print_contract(self, the_contract, error_msg =""):
        while True:
            old_width = self.ui_helper.width
            self.ui_helper.width = 80                  #Sets ui window width to about A4 size
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.view_contract_details(the_contract)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            self.ui_helper.width = old_width            #Resets ui window width
            print(error_msg)
            user_choice = input("Input: ")

            if user_choice.lower() == self.ui_helper.BACK:
                return

            elif user_choice.lower() == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()

            else:
                error_msg = f"Enter {self.ui_helper.QUIT.upper()} to quit or {self.ui_helper.BACK.upper()} to go back"
    
    def compact_contract(self, a_contract):
        ''' Displays contract information in a compact format '''
        a_vehicle = self.logic_api.find_vehicle(a_contract.vehicle_id)
        a_customer = self.logic_api.find_customer(a_contract.customer_ssn)
        contract_column = [a_contract.contract_id, a_contract.status, a_contract.total, a_vehicle.type, f"{a_vehicle.manufacturer} {a_vehicle.model}", a_customer.name, a_customer.ssn, a_contract.loan_date, a_contract.end_date]
        self.ui_helper.n_columns(contract_column)  

# End of view contracts functions

# Customer functions that are used throughout contract sections

    def find_customer(self, error_msg=""):      # This function is called in line 67(def new_contract)
        ''' Searches for a customer, returning none if no customer exists with that ssn '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_blank_line()
            self.ui_helper.print_line("    Enter customer's social security number")
            self.ui_helper.print_line("    (DDMMYY-NNNN)")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            ssn = input("Input: ")

             #Check if the user wants to back or quit
            if ssn.lower() == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()
            elif ssn.lower() == self.ui_helper.BACK:
                return None, None

            ssn = self.logic_api.check_ssn(ssn)

            if ssn != None:
                return self.logic_api.find_customer(ssn), ssn

            else:
                error_msg = "Please provide a correctly formatted social security number, DDMMYY-NNNN"

    def confirm_customer(self, the_customer, error_msg=""):     # This function is called in line 77
        ''' Asks user if customer info is correct '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line("    Is this information correct? (y/n)")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_line("    (Y)es to continue")
            self.ui_helper.print_line("    (N)o to change information")
            self.ui_helper.print_blank_line()
            self.view_customer_details(the_customer)
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice =input("Input: ")
            if user_choice.lower() in [self.ui_helper.BACK, self.ui_helper.QUIT] or user_choice.lower() in self.ui_helper.YES or user_choice.lower() in self.ui_helper.NO:
                return user_choice
            else:
                error_msg = "Please select a valid option"

    def create_customer(self, ssn, error_msg =""):              # This function is called in line 72
        ''' Creates a new customer and passes it along to logic '''
        the_customer = Customer("", ssn, "", "", ".", "", "", "")
        attribute_list = ["name", "address", "postal code", "phone", "email", "country"]
        for attribute in attribute_list:
            while True:
                placeholder_text = f"<< Enter {attribute} >>"
                attr_key = attribute.replace(" ", "_")
                setattr(the_customer, attr_key, placeholder_text)
                self.ui_helper.clear()
                self.ui_helper.print_header()
                self.view_customer_details(the_customer)
                self.ui_helper.print_blank_line()
                self.ui_helper.print_footer()
                print()
                attr_value = input(f"Enter customer's {attribute}: ")
                if attr_value.lower() == self.ui_helper.BACK:
                    return

                elif attr_value.lower() == self.ui_helper.QUIT:
                    self.ui_helper.quit_prompt()
                    continue

                else:
                    attr_value = self.logic_api.check_attribute(attr_value, attr_key)
                    if attr_value != None:
                        setattr(the_customer, attr_key, attr_value)     #Sets attribute to input
                        break
                    
                    else:
                        error_msg = f"Please enter a valid {attribute}"
        
        licences = self.get_licences(the_customer)                 #Gets licence(s) for the customer
        setattr(the_customer, "licenses", licences) 

        self.logic_api.add_customer(the_customer)
        return the_customer
    
    def modify_customer(self, original_customer, error_msg=""): # This function is called in line 80
        ''' 
        shows all details of a customer, with indices and takes user choice in what to change, and changes it, 
        when user confirms, sends an instance of the employee down to logic 
        If an attribute has been changed, allows user to undo
        '''
        old_attr_list = []
        customer = original_customer
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line("Change customer information")
            self.ui_helper.print_line("Please select an option:")
            self.ui_helper.print_blank_line()
            self.customer_change_view(customer)
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
                    user_choice = self.unsaved_changes(customer)
                    if user_choice.lower() in self.ui_helper.YES:
                        return
                    else:
                        continue
                else:
                    return

            else:

                if user_choice == "1":
                    old_attr_list.append(self.ui_helper.get_old_attributes(customer, "address"))        #Stores old values before changing
                    setattr(customer, "address", f"<< ENTER NEW ADDRESS >>")
                    customer.address = self.change_customer_attribute(customer, "address")

                elif user_choice == "2":
                    old_attr_list.append(self.ui_helper.get_old_attributes(customer, "postal_code"))    #Stores old values before changing
                    setattr(customer, "postal_code", f"<< ENTER NEW POSTAL CODE >>")
                    customer.postal_code = self.change_customer_attribute(customer, "postal_code")

                elif user_choice == "3":
                    old_attr_list.append(self.ui_helper.get_old_attributes(customer, "phone"))   #Stores old values before changing
                    setattr(customer, "phone", f"<< ENTER NEW PHONE NR >>")
                    customer.phone = self.change_customer_attribute(customer, "phone")

                elif user_choice == "4":
                    old_attr_list.append(self.ui_helper.get_old_attributes(customer, "email"))     #Stores old values before changing
                    setattr(customer, "email", f"<< ENTER NEW EMAIL ADDRESS >>")
                    customer.email = self.change_customer_attribute(customer, "email")

                elif user_choice == "5":
                    old_attr_list.append(self.ui_helper.get_old_attributes(customer, "country"))          #Stores old values before changing
                    setattr(customer, "email", f"<< ENTER NEW COUNTRY >>")
                    customer.email = self.change_customer_attribute(customer, "country")

                elif user_choice.lower() == self.ui_helper.SAVE:
                    changed_customer = self.confirm_changes(customer)
                    if changed_customer != None:
                        return changed_customer
                    else:
                        return original_customer

                elif user_choice.lower() == self.ui_helper.UNDO and old_attr_list != []:
                    ''' Undo the last changes stored in the old attribute list, and removes the last item in the list '''
                    undo_key = old_attr_list[-1][0]
                    undo_value = old_attr_list[-1][1]
                    del old_attr_list[-1]
                    setattr(customer, undo_key, undo_value)
                    continue
    
    def change_customer_attribute(self, customer, attribute, error_msg = ""):   # This function is called multiple times in def modify_customer()
        ''' Changes and error checks a single attribute change, when modifying an employee '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line("Change customer information")
            self.ui_helper.print_line(f"Please enter a new {attribute}")
            self.ui_helper.print_blank_line()
            self.customer_change_view(customer)
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
    

    def customer_not_found(self):
        ''' Displays that no customer was found, returning after user presses enter, not saving input '''
        self.ui_helper.clear()
        self.ui_helper.print_header()
        self.ui_helper.print_line("No customer found")
        self.ui_helper.print_line("Press enter to continue")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_hash_line()
        print()
        _x = input("Input: ")
        return 

# End of customer functions

# Employee functions that are used throughout create contract section

    def employee_for_contract(self, error_msg=""): 
        ''' Gets employee for the contract '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_blank_line()
            self.ui_helper.print_line("    Enter employee's social security number")
            self.ui_helper.print_line("    (DDMMYY-NNNN)")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            ssn = input("Input: ")

            #Check if the user wants to back or quit
            if ssn.lower() == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()

            elif ssn.lower() == self.ui_helper.BACK:
                return None, None

            ssn = self.logic_api.check_ssn(ssn)

            if ssn != None:
                return self.logic_api.find_employee(ssn), ssn

            else:
                error_msg = "Please provide a correcly formatted social security number, DDMMYY-NNNN"
    
    def confirm_employee(self, the_employee, error_msg=""):     # This function calls the employeeUI class
        ''' Asks user if employee info is correct '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line("    Is this information correct? (y/n)")
            self.ui_helper.print_blank_line()
            self.employee_ui.view_employee_details(the_employee)
            self.ui_helper.print_footer()
            print(error_msg)
            return input("Input: ")

# End of employee functions

# Functions that are used to modify existing/new contract

    def change_contract_start_date(self, a_contract, error_msg=""):
        ''' Changes contract start date with input from user '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line("    Enter new start date (DD/MM/YYYY)")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            new_date = input("Input: ")
            if new_date.lower() == self.ui_helper.BACK:
                return

            elif new_date.lower() == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()

            else:
                new_date = self.logic_api.check_date(new_date)

                if new_date != None:
                    old_attr = ("loan_date", getattr(a_contract, "loan_date")) 
                    setattr(a_contract, "loan_date", new_date)
                    return old_attr

                else:
                    error_msg = "Please enter a valid date"


    def change_contract_end_date(self, a_contract, error_msg=""):
        ''' Changes contract end date with input from user '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line("    Enter new end date (DD/MM/YYYY)")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            new_date = input("Input: ")
            if new_date.lower() == self.ui_helper.BACK:
                return

            elif new_date.lower() == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()

            else:
                new_date = self.logic_api.check_date(new_date)

                if new_date != None:
                    old_attr = ("end_date", getattr(a_contract, "end_date"))
                    setattr(a_contract, "end_date", new_date)
                    return old_attr

                else:
                    error_msg = "Please enter a valid date"

    
    def change_contract_vehicle(self, a_contract, error_msg=""):
        ''' Changes contract vehicle with input from user '''
        while True:
            iata = self.logic_api.city_to_iata(self.logic_api.find_vehicle(a_contract.vehicle_id).location)
            location = self.logic_api.find_destination(iata)
            the_type = self.get_vehicle_type(a_contract.loan_date, a_contract.end_date, location)
            if the_type != None:

                while True:
                    new_vehicle_id = self.choose_vehicle(a_contract.customer_ssn, a_contract.loan_date, a_contract.end_date, location, the_type)

                    if new_vehicle_id != None:
                        old_attr = ("vehicle_id", getattr(a_contract, "vehicle_id"))
                        setattr(a_contract, "vehicle_id", new_vehicle_id)
                        return old_attr

                    else:               #Goes back to select type if back in vehicle selection
                        break

            else:
                return


    def terminate_contract(self, a_contract):
        ''' Asks user if they want to terminate a contract '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line(f"    Are you sure you want to terminate contract {a_contract.contract_id}? (y/n)")
            self.ui_helper.print_line("    This change cannot be undone")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_hash_line()
            print()
            user_choice = input("Input: ")
            if user_choice.lower() in self.ui_helper.YES:
                self.logic_api.change_contract_status(a_contract.contract_id, "terminated")
                return True

            else:
                return False
    

    def unsaved_changes(self, the_customer):   
        ''' Asks user if they want to go back without saving their changes '''
        self.ui_helper.clear()
        self.ui_helper.print_header()
        self.view_customer_details(the_customer)
        self.ui_helper.unsaved_prompt()
        self.ui_helper.print_blank_line()
        self.ui_helper.print_hash_line()
        print()
        return input("Input: ")

        
    def confirm_changes(self, customer):   
        ''' Ask user to confirm changes and modifies customer if yes '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.view_customer_details(customer)
            self.ui_helper.print_line("Are you sure you want to save these changes? (y/n)")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print()
            confirm_choice = input("Input: ")
            if confirm_choice.lower() in self.ui_helper.YES:
                self.logic_api.change_customer_info(customer)
                return customer
            else:
                return None

# End of functions that are used to modify existing/new contract


# Vehicles functions that are used for vehicles in contracts

    def no_vehicles_available(self, start_date, end_date, location):
        ''' '''
        self.ui_helper.clear()
        self.ui_helper.print_header()
        self.ui_helper.print_line(f"No vehicles available in {location} from {start_date} to {end_date}")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_hash_line()
        return input("Input: ")

    
    def get_vehicle_type(self, start_date, end_date, location,  error_msg=""):
        ''' Displays all vehicle types in a given location and allows user to choose '''
        vehicle_types = self.logic_api.filter_by_region(location.airport, start_date, end_date)
        if vehicle_types == []:
            self.no_vehicles_available(start_date, end_date, location)
            return

        vehicle_type_list = [ (str(ind + 1), line) for ind, line in enumerate(vehicle_types)]                                                                          
        vehicle_type_dict = dict(vehicle_type_list)
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line("Select vehicle type:")
            for line in vehicle_type_list:
                self.ui_helper.print_line(f"    {line[0]}. {line[1].name}")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()

            user_choice = self.ui_helper.get_user_menu_choice(vehicle_type_list)
            if user_choice != None:

                if user_choice.lower() == self.ui_helper.BACK:
                    return

                elif user_choice.lower() == self.ui_helper.QUIT:
                    self.ui_helper.quit_prompt()

                else:
                    return vehicle_type_dict[user_choice]
                
            else:
                error_msg = "Please select a vehicle type from the list"

    
    def choose_vehicle(self, cust_ssn, start_date, end_date, location, a_vehicle_type, error_msg=""):
        ''' Lists all vehicles that are available for given dates, in a given location of a given type '''
        vehicle_list = self.logic_api.get_filtered_vehicle(start_date, end_date, location, a_vehicle_type)
        id_list = [vehicle.id for vehicle in vehicle_list ]
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line("Enter vehicle ID to select")
            self.ui_helper.print_line("if nothing is chosen one will be selected automatically")
            self.ui_helper.print_blank_line()
            self.vehicle_ui.print_vehicle_list(vehicle_list)
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            id_choice = input("Input: ")
            if id_choice in id_list:
                if self.logic_api.match_licenses(cust_ssn, id_choice):  #If customer has right for this vehicle
                    return id_choice
                
                else:
                    self.license_required(cust_ssn, id_choice)

            elif id_choice == "":
                for veh_id in id_list:
                    if self.logic_api.match_licenses(cust_ssn, veh_id):
                        return veh_id
                
                self.license_required(cust_ssn, id_list[-1])


            elif id_choice.lower() == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()

            elif id_choice.lower() == self.ui_helper.BACK:
                return self.ui_helper.BACK

            else:
                error_msg = "Please select a vehicle id from the list"


    def license_required(self, customer_ssn, vehicle_id):
        ''' Informs user that the vehicle has license requirements that the customer does not meet, asks if user wants to confirm that customer has required license,
        if yes adds license to customer and regiers vehicle to contract '''
        the_vehicle = self.logic_api.find_vehicle(vehicle_id)
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line(f"The selected vehicle, ID {vehicle_id} has license requirements: {the_vehicle.license_type} license")
            self.ui_helper.print_line("Customer does not have the required license in their file")
            self.ui_helper.print_line("Please select another vehicle")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_hash_line()
            return input("Input: ")
    

    def pick_up_vehicle(self, error_msg=""):
        ''' Menu for when a customer is picking up a vehicle, asks for ssn and goes through the steps '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line("    Enter customer ssn:")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = input("Input: ")
            if user_choice.lower() == self.ui_helper.BACK:
                return

            elif user_choice.lower() == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()

            ssn = self.logic_api.check_ssn(user_choice)
            if ssn == None:
                error_msg = "Please enter a valid social security number (DDMMYY-NNNM)"
                continue
            
            else:
                the_customer = self.logic_api.find_customer(ssn)

                if the_customer != None:
                    conf_choice = self.confirm_customer(the_customer)
                    if conf_choice.lower() in self.ui_helper.YES:                   #If the customer is confirmed
                        
                        ### The contracts <3 ###
                        contract_list = self.logic_api.view_customer_contracts(ssn)
                        if contract_list == []:
                            pass
                            #No contract for this customer today

                        else:
                            returning_choice = self.customer_vehicle_selection(contract_list)   #To return to menu if user finished a task
                            if returning_choice == self.ui_helper.BACK:
                                return

                    else:
                        continue

                else:                       #If customer is not found
                    error_msg = "No customer with this ssn found!"
                    continue


    def customer_vehicle_selection(self, contract_list, error_msg=""):
        ''' Displays vehicles in a list and allows user to select (A)ll or one at a time to lend them out '''
        activate_list = []
        undo_list = []
        activate_all = "a"
        while True:
            vehicle_id_dict =  { contract.vehicle_id: contract for contract in contract_list }      #Contains vehicle id as key and contract as value, updates if user activates a contract
            self.ui_helper.clear()
            self.ui_helper.print_header()
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
                self.ui_helper.print_line(f"    ({self.ui_helper.SAVE.upper()})ave: Save changes")

            if undo_list != []:
                self.ui_helper.print_line(f"    ({self.ui_helper.UNDO.upper()})ndo: Undo last change")

            self.ui_helper.print_footer()
            print(error_msg)
            user_choice = input("Input: ")
            if user_choice.lower() == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()

            elif user_choice.lower() == self.ui_helper.BACK:
                return

            elif user_choice.lower() == self.ui_helper.UNDO:

                if isinstance(undo_list[-1], list):             #if the last item in undo list is a list
                    contract_list.extend(undo_list[-1])
                    for contract in undo_list[-1]:
                        activate_list.remove(contract)
                    undo_list.pop()

                else:                                           #if it is not
                    contract_list.append(undo_list[-1])
                    activate_list.remove(undo_list[-1])
                    undo_list.pop()
            
            elif user_choice.lower() == self.ui_helper.SAVE:                   #Saves changes through logic API
                for contract in activate_list:
                    self.logic_api.change_contract_status(contract.contract_id, "Active")
                self.contracts_activated()

                return self.ui_helper.BACK              #Makes user return to staff type menu if they finish the task

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
    
    def list_vehicle_and_contract_info(self, contract_list):
        ''' Lists info about vehicles and rates for pickup '''
        header_list = ["<< VEHICLE ID >>", "<< TYPE >>", "<< MAKE >>", "<< MODEL >>", "<< RETURN DATE >>", "<< RATE >>", "<< PRICE >>", "<< CONTRACT ID >>"]
        self.ui_helper.n_columns(header_list)
        for contract in contract_list:
            vehicle = self.logic_api.find_vehicle(contract.vehicle_id)
            self.logic_api.get_types_rate(vehicle.type)
            self.ui_helper.n_columns([vehicle.id, vehicle.type, vehicle.manufacturer, vehicle.model, contract.end_date, self.logic_api.get_types_rate(vehicle.type), contract.base_price, contract.contract_id])

    def vehicle_has_been_returned(self):
        ''' Displays that vehicle has been returned '''
        self.ui_helper.clear()
        self.ui_helper.print_header()
        self.ui_helper.print_line("Vehicle has been returned.")
        self.ui_helper.print_line("Press enter to continue")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_hash_line()
        print()
        _x = input("Input: ")
        return

# End of vehicles functions


# The rest are helper functions that are used throughout contract sections
    def get_user_input(self, prompt_str):
        ''' Asks user for input and returns it '''
        self.ui_helper.clear()
        self.ui_helper.print_header()
        self.ui_helper.print_line(prompt_str)
        self.ui_helper.print_blank_line()
        self.ui_helper.print_footer()
        print()
        return input("Input: ")
        
        
    def get_location(self, error_msg=""):
        ''' Gets a location from the user '''
        valid_locations = self.logic_api.destinations_option_list()
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line("Enter contract location")
            for iata, location in valid_locations:
                if iata != "ADM" and iata != "KEF":
                    self.ui_helper.print_line(f"    {iata}: {location}")
                else:
                    valid_locations.remove((iata, location))
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            user_input = self.ui_helper.get_user_menu_choice(valid_locations)
            if user_input.lower() == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()

            elif user_input.lower() == self.ui_helper.BACK:
                return

            location = self.logic_api.find_destination(user_input)
            if location != None:
                return location
            else:
                error_msg = "Please enter a valid location (IATA)"

    
    def get_date(self, date_type_str, error_msg=""):
        ''' gets a date from the user '''
        while True:
            self.ui_helper.clear()
            self.ui_helper.print_header()
            self.ui_helper.print_line(f"    Enter contract {date_type_str} date (DD/MM/YYYY)")
            self.ui_helper.print_blank_line()
            self.ui_helper.print_footer()
            print(error_msg)
            date_str = input("Input: ")
            if date_str.lower() == self.ui_helper.QUIT:
                self.ui_helper.quit_prompt()

            elif date_str.lower() == self.ui_helper.BACK:
                return

            date_str = self.logic_api.check_date(date_str)
            if date_str != None:
                return date_str
            else:
                error_msg = "Please enter a valid date (DD/MM/YYYY)"

              
    
    def contracts_activated(self):
        ''' Confirm screen to tell user contracts have been activated '''
        self.ui_helper.clear()
        self.ui_helper.print_header()
        self.ui_helper.print_line("Contract(s) have been activated")
        self.ui_helper.print_line("Press enter to return")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_footer()
        print()
        return input("Input: ")

    
    def contract_not_found(self):
        ''' Displays that no contract was found, returning after user presses enter, not saving input '''
        self.ui_helper.clear()
        self.ui_helper.print_header()
        self.ui_helper.print_line("No contract found")
        self.ui_helper.print_line("Press enter to continue")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_hash_line()
        print()
        _x = input("Input: ")
        return 


