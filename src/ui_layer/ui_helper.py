import os

class UIHelper():

    QUIT = "9"
    BACK = "0"

    def __init__(self, width):
        self.width = width
        self.half_a = width // 2
        self.half_b = self.half_a
        if self.width % 2 == 1:
            self.half_b += 1

    def clear(self):
        """ helper function to clear screen """
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
    
    def print_line(self, a_str):
        """ Prints a line with | on either side, with one string, left aligned 3 spaces, 4 including the |. """
        a_str = "|   " + a_str
        print(a_str + " " * (self.width - len(a_str) - 1) + "|")


    def print_blank_line(self):
        print("|" + " " * (self.width - 2) + "|")


    def print_hash_line(self):
        print("#" * self.width)

    def print_line_2_strings(self, a_str, b_str):
        """ Prints a line of length width, takes two strings and aligns them on either side, 3 spaces from the edge, | """
        a_str = "|   " + a_str
        b_str = b_str + "   |"     
        print("{: <{width}}".format(a_str, width = self.half_a), end="")
        print("{: >{width}}".format(b_str, width = self.half_b))


    def print_header(self, a_str):
        """ prints header of width width, takes a string as parameter for a display message """
        employee_type = "<< " + a_str + " >>"
        comp_str = "Nan Air Rentals"
        version = "Vol 1.0"
        self.print_hash_line()
        self.print_line_2_strings(comp_str, version)
        self.print_line(employee_type)
        self.print_hash_line()
        self.print_blank_line()


    def print_options(self, options_list, opt_str):
        """ 
        Takes a list of tuples as parameter with an option code (required input)
        and option description and prints it 
        """
        opt_str = (f"|   {opt_str}")
        print(opt_str + " " * (self.width - len(opt_str) - 1) + "|")
        for option in options_list:
            choice_str = f"    {option[0]}: {option[1]}"
            self.print_line(choice_str)

        self.print_blank_line()


    def print_start_footer(self):
        """
        Prints the footer with a quit option 
        """
        quit_str = (f"    {self.QUIT}: Quit")
        self.print_line(quit_str)
        self.print_blank_line()
        self.print_hash_line()
        

    def print_footer(self):
        """
        Prints the footer with a quit and back option 
        """
        quit_str = (f"    {self.QUIT}: Quit")
        self.print_line(quit_str)
        back_str = (f"    {self.BACK}: Back")
        self.print_line(back_str)
        self.print_blank_line()
        self.print_hash_line()

    def get_user_menu_choice(self, options_list):
        """
        Gets a choice from the user
        """
        user_choice = input("Input: ")
        for option in options_list:
            if option[0].lower() == user_choice.lower().strip():
                return option[0]
        if user_choice == self.QUIT or user_choice == self.BACK:
            return user_choice
        else:
            return None