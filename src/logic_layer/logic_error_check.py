import string

class LogicErrorCheck():
    def __init__(self, data_api, destination_logic):
        self.data_api = data_api
        self.destination_logic = destination_logic

    def check_name(self,a_str):
        new_str = ""
        a_str = a_str.strip()
        for char in a_str:
            if char.isalpha():
                if (new_str == "") or (new_str[-1].isspace()):
                    new_str += char.upper()
                else:
                    new_str += char.lower()
            elif char.isspace():
                new_str += char
            
            else:
                return None
        return new_str

    def check_phone(self, a_str):
        # US and UK number length are the same or 11 in length but some areas
        # in UK have number length of 10.
        if len(a_str) < 6:
            return None
        elif len(a_str) > 18:
            return None
        else:
            for char in a_str:
                if char.isnumeric() == False and char.isspace() == False and char != "+":
                    return None
        
        return a_str


    def check_iata(self,a_str):
        ''' Checks that a string is a valid iata code that does not exist already, returning None if invalid and "1" if it already exists, otherwise returns the string in uppercase '''
        valid_dest = self.data_api.get_destinations()
        valid_work_areas = [getattr(dest,"iata") for dest in valid_dest]
        for work_area in valid_work_areas:
            if a_str.lower() == work_area.lower():
                return "1"      # To know area exists

        if len(a_str) != 3:    
            return None

        else:
            for char in a_str:
                if char.isalpha() == False:
                    return None
            
            return a_str.upper()

    
    def check_hours(self, hours):
        ''' Checks if supplied hours are in avalid fomrat, returning none if not '''
        hours_list = hours.split(" - ")
        for time in hours_list:
            if len(time) != 5:
                return None
            else:
                hour = time[:2]
                minutes = time[3:]
                if int(hour) > 24:
                    return None
                
                if int(minutes) > 60:
                    return None
                
                if time[2] != ":":
                    return None
        
        return hours


    def ssn_formatter(self, ssn):
        ''' Returns a ssn in the correct format, NNNNNN-NNNN. '''
        if len(ssn) == 10:
            for num in ssn:
                if num.isnumeric() == False:
                    return None

            ssn = ssn[:6] + "-" + ssn[6:]

        elif len(ssn) == 11 and (ssn[6].isspace() or ssn[6] == "-"):
            for ind, num in enumerate(ssn):
                if num.isnumeric() == False and ind != 6:
                    return None

            ssn = ssn[:6] + "-" + ssn[7:]

        else:
            ssn = None
        
        return ssn


    def check_email(self, email_address):
        ''' 
        Checks if email address is valid, that it contains:
        exactly one @
        no consec dots
        exactly one dot after @
        '''
        email_address 
        if email_address[0] == ".":
            return None

        if email_address.count("@") != 1:
            return None

        for i in range(len(email_address ) - 1):
            if email_address[i] == "." and email_address[i + 1] == "@":
                return None
            if email_address[i] == "." and email_address[i + 1] == ".":
                return None

            if email_address[i] == "@":
                if email_address[i:].count(".") != 1:
                    return None
                if "." not in email_address[i:]:
                    return None
                    
        if email_address[-1] == "@":
            return None
        if "@" in email_address[0]:
            return None

        return email_address

    
    #This function can be used whenever a string has to be only numbers with no spaces
    def check_if_number(self, a_str):
        try:
            _num = int(a_str)
            return a_str
        except ValueError:
            return None
    
    def check_valid_vehicle_type(self, a_str):
        all_vehicle_types = self.data_api.get_all_vehicle_types()
        valid_types = [getattr(name, "name") for name in all_vehicle_types]
        for vehicle_type in valid_types:
            if str(vehicle_type.lower()) == a_str.lower():
                return a_str

        return None
    
    def check_location(self, a_str):
        all_airports = self.data_api.get_destinations()
        valid_airports = [getattr(airport, "airport") for airport in all_airports]
        for airport in valid_airports:
            if str(airport.lower()) == a_str.lower():
                return a_str
        return None
    
    def check_color(self, a_str):
        ''' error check cancelled, go home '''
        return a_str


    def check_date(self, date_str):
        ''' checks if a date is correctly formatted and returns none if it is not '''
        length = len(date_str)
        shorter_months = [4, 6, 9, 11]
        day = date_str[0:2]
        if length == 8:
            month = date_str[2:4]
            year = date_str[4:]
        else:
            month = date_str[3:5]
            year = date_str[6:]

        try:
        
            if int(month) > 12:
                return None

            if int(month) == 2 and int(day) > 29:   #Leap years are a lie
                return None

            if int(month) in shorter_months and int(day) > 30:
                return None
            
            if int(day) > 31:
                return None

        except ValueError:
            return None

        return f"{day}/{month}/{year}"
    
    def check_address(self, address):
        address = address.strip()
        for char in address:
            if char in string.punctuation:
                return None
        return address.capitalize()

    def check_work_area(self, a_str):
        ''' Checks if a given string matches an existing work area '''
        valid_areas = self.destination_logic.get_destinations()
        for dest in valid_areas:
            if dest.iata.lower() == a_str.lower():
                return dest.iata

        return None


    def decide_what_error(self, a_str, attribute):
        ''' Takes in a string then decides what error check needs to be done 
        on that particular string. '''
   
    # Phone
        if attribute.lower() == "phone" or attribute.lower() == "mobile_phone" or attribute.lower() == "home_phone":
            return self.check_phone(a_str)
    # NAME
        elif attribute.lower() == "name":
            return self.check_name(a_str)
    # ADDRESS
        elif attribute.lower() == "address":
            return self.check_address(a_str)
    # EMAIL
        elif attribute.lower() == "email":
            return self.check_email(a_str)
    # POSTAL CODE
        elif attribute.lower() == "postal_code":
            return self.check_if_number(a_str)
    # SSN
        elif attribute.lower() == "ssn":
            return self.ssn_formatter(a_str)
    # COUNTRY
        elif attribute.lower() == "country":
            return a_str.capitalize()
    # WORK AREA
        elif attribute.lower() == "work_area":
            return self.check_work_area(a_str)
    # Vehicle type
        elif attribute.lower() == "type":
            return self.check_valid_vehicle_type(a_str)
    # Year
        elif attribute.lower() == "year":
            return self.check_if_number(a_str)
    # COLOR
        elif attribute.lower() == "color":
            return self.check_color(a_str)
    # If attribute is undefined then we do nothing.    
        else:
            return a_str

        



    
