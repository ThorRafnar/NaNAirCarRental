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