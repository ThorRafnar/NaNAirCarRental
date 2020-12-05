import string

class LogicErrorCheck():
    def __init__(self, data_api):
        self.data_api = data_api

    def check_name(self,a_str):
        new_str = ""
        a_str = a_str.strip()
        for index, char in enumerate(a_str):
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
        IS_number_length = 7
        US_number_length = 11
        UK_number_length = 10
        DK_number_length = 8
        FI_number_length = 6    # Faroe islands
        counter = 0
        for char in a_str:
            if char.isspace():
                pass
            else:
                counter += 1
        if counter != IS_number_length and counter != US_number_length and counter !=  UK_number_length and counter != DK_number_length and counter != FI_number_length:
            return None
        
        return a_str

    def check_work_area(self,a_str):
        valid_dest = self.data_api.get_destinations()
        valid_work_areas = [getattr(dest,"iata") for dest in valid_dest]
        valid_work_areas.append("Admin")
        for work_area in valid_work_areas:
            if a_str.lower() == work_area.lower():
                return work_area
            
        return None


    def check_email(self, a_str):
        # Maybe add valid email domains in future?
        if "@" not in a_str:
            return None
        
        return a_str
    
    #This function can be used whenever a string has to be only numbers with no spaces
    def check_if_number(self, a_str):
        try:
            numb = int(a_str)
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
        # These are the valid colors for the system
        valid_colors = ["blue","green","purple","grey","black","white","orange","yellow","pink","brown"]
        if a_str.lower() in valid_colors:
            return a_str.lower()
        else:
            return None
    
    def check_ssn_inpunt(self, a_str):
        ''' Takes in a string that is supposed to be social security number 
        and checks if it is valid or not.'''
        new_str = ""
        final_str = ""
        for char in a_str:
            if char.isspace():
                pass
            new_str += char
        
        if len(new_str) > 10:
            return None
        
        try:
            numb = int(new_str)
        except ValueError:
            return None
        
        birtday = new_str[0:6]
        if (int(new_str[0:2]) > 31) or (int(new_str[2:4]) > 12):
            return None
        
        counter = 0
        for char in new_str:
            counter += 1
            final_str += char
            if counter == 6:
                final_str += "-"
        
        return final_str

    
