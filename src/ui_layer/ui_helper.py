import os

class UIHelper():

    QUIT = "q"
    BACK = "b"
    SAVE = "s"
    UNDO = "u"
    YES = ["y", "yes"]
    NO = ["n", "no"]

    def __init__(self, width, header_str):
        self.width = width
        self.header_string = header_str


    def clear(self):
        """ helper function to clear screen """
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    
    def seperator(self):
        print("|   " + "_" * (self.width - 8) + "   |")


    def left_aligned_columns(self, string_list):
        ''' prints columns left aligned '''
        width = self.width - 2
        remainder = width % len(string_list)
        print("|", end="")
        for a_string in string_list:
            col_width = width // len(string_list)
            if remainder > 0:
                col_width += 1
                remainder -= 1
            print("{: <{width}}".format(a_string, width = col_width), end="")
            
        print("|")

    
    def print_line(self, a_str):
        """ Prints a line with | on either side, with one string, left aligned 3 spaces, 4 including the |. """
        a_str = "|   " + a_str
        print(a_str + " " * (self.width - len(a_str) - 1) + "|")


    def print_blank_line(self):
        ''' ‾|_(ツ)_/‾ '''
        print("|" + " " * (self.width - 2) + "|")


    def print_hash_line(self):
        print("#" * self.width)

    def print_line_2_strings(self, a_str, b_str):
        """ Prints a line of length width, takes two strings and aligns them on either side, 3 spaces from the edge, | """
        half_a = self.width // 2
        half_b = half_a
        if self.width % 2 == 1:
            half_b += 1
        a_str = "|   " + a_str
        b_str = b_str + "   |"     
        print("{: <{width}}".format(a_str, width = half_a), end="")
        print("{: >{width}}".format(b_str, width = half_b))


    def print_header(self):
        """ prints header of width width, takes a string as parameter for a display message """
        employee_type = f"<< {self.header_string} >>"
        comp_str = "Nan Air Rentals"
        version = "Vol 1.0"
        self.print_hash_line()
        self.print_line_2_strings(comp_str, version)
        self.print_line(employee_type)
        self.print_hash_line()
        self.print_blank_line()



    def print_options(self, options_list, opt_str=""):
        """ 
        Takes a list of tuples as parameter with an option code (required input)
        and option description and prints it 
        """
        self.print_line(opt_str)
        for option in options_list:
            choice_str = f"    {option[0]}: {option[1]}"
            self.print_line(choice_str)

        self.print_blank_line()


    def print_start_footer(self):
        """
        Prints the footer with a quit option 
        """
        quit_str = (f"    ({self.QUIT.upper()})uit")
        self.print_line(quit_str)
        self.print_blank_line()
        self.print_hash_line()
        

    def print_footer(self):
        """
        Prints the footer with a quit and back option 
        """
        quit_str = (f"    ({self.QUIT.upper()})uit")
        self.print_line(quit_str)
        back_str = (f"    ({self.BACK.upper()})ack")
        self.print_line(back_str)
        self.print_blank_line()
        self.print_hash_line()

    def get_user_menu_choice(self, options_list=None):
        """
        Gets a choice from the user
        """
        if options_list == None:
            options_list = []
        user_choice = input("Input: ")
        for option in options_list:
            if option[0].lower() == user_choice.lower().strip():
                return option[0]
        if user_choice.lower() == self.QUIT.lower() or user_choice.lower() == self.BACK.lower():
            return user_choice
        else:
            return None

    def n_columns(self, string_list):
        '''
        Takes a list of items to print and divides into columns of roughly equal size
        '''
        width = self.width - 2
        remainder = width % len(string_list)
        print("|", end="")
        for a_string in string_list:
            col_width = width // len(string_list)
            if remainder > 0:
                col_width += 1
                remainder -= 1
            print("{: ^{width}}".format(a_string, width = col_width), end="")
            
        print("|")

    def print_centered_line(self, a_str):
        ''' prints a string centered on the screen '''
        print("|{: ^{width}}|".format(a_str, width = self.width - 2))

    
    def print_centered_line_dash(self, a_str):
        ''' prints a string centered , padded with dashes on the screen '''
        print("|   {:-^{width}}   |".format(a_str, width = self.width - 8))


    def quit_prompt(self):
        ''' 
        Asks the user if they really want to quit, 
        and quits if they do, else returns to previous screen 
        '''
        self.clear()
        self.print_header()
        self.print_blank_line()
        self.print_centered_line("Are you sure you want to quit ? (y/n)")
        self.print_centered_line("Any unsaved changes will be lost!")
        self.print_blank_line()
        self.print_hash_line()
        user_choice = input("Enter choice: ")
        if user_choice.lower() in self.YES:
            self.clear()
            quit()
        else:
            return


    def get_old_attributes(self, a_class_instance, attr_key):
        ''' gets an attribute from a class instance and returns a tuple with the old attribute key and value '''
        old_attr_value = getattr(a_class_instance, attr_key)
        return (attr_key, old_attr_value)

    
    def unsaved_prompt(self):
        ''' Informs user of unsaved changes, takes no input and returns nothing '''
        self.print_line("    You have unsaved changes!")
        self.print_line("    Are you sure you want to go back? (y/n)")
        self.print_line("    Your unsaved changes will be lost")


    def dict_to_list(self, options_dict):
        ''' converts a dictionary to a list and returns it '''
        return [(k, v) for k, v in options_dict.items()]

    def n_columns_width(self, columns, wid):
        ''' Formats n columns in a given width, returns a string'''
        remainder = wid % len(columns)
        ret_str = ""
        for a_string in columns:
            col_width = wid // len(columns)
            if remainder > 0:
                col_width += 1
                remainder -= 1
            ret_str += "{: ^{width}}".format(a_string, width = col_width)
            
        return ret_str

"""
Roses are red
Violets are blue
Expected indented block
in line 32
"""
