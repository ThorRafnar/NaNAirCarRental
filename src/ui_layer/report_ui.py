class ReportUI():

    def __init__(self, ui_helper, logic_api):
        PROFIT_REPORTS = "Profits"
        UTIL_REPORTS = "Utilization Reports"
        BILLS = "Bills"
        self.ui_helper = ui_helper
        self.logic_api = logic_api
        self.options_dict = {
            "1": self.PROFIT_REPORTS,
            "2": self.UTIL_REPORTS,
            "3": self.BILLS,
        }
    
    def reports_menu(self, header_str):
        user_choice = ReportUI.show_options(header_str)
        while True:
            if self.options_dict[user_choice].lower() == self.ui_helper.QUIT.lower():
                self.ui_helper.quit_prompt(header_str)
            elif self.options_dict[user_choice].lower() == self.ui_helper.BACK.lower():
                return
            else:
                if self.options_dict[user_choice] == self.PROFIT_REPORTS:
                    # Call a function wich deals with profit reports
                elif self.options_dict[user_choice] == self.UTIL_REPORST:
                    # Call a function wich deals with utilizitation reports
                elif self.options_dict[user_choice] == self.BILLS:
                    # Call a function wich deals with bills.

    
    def show_options(self, header_str, error_msg=""):
        options_list = self.ui_helper.list_to_dict(self.options_dict)
        self.ui_helper.clear()
        self.ui_helper.print_header(header_str)
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line("    Tasks:")
        self.ui_helper.print_blank_line()
        for option in options_list:
            print(option)
        self.ui_helper.print_blank_line()
        self.ui_helper.print_footer()
        return input("Input: ")
    

    def show_profit_reports(self, header_str):
        self.ui_helper.clear()
        self.ui_helper.print_header(header_str)
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line("    Profit Reports:")
        ReportUI.ask_end_and_start_date(header_str)
        # How do they look? O.o

    def ask_end_and_start_date(self, header_str):
        self.ui_helper.clear()
        self.ui_helper.print_header(header_str)
        self.ui_helper.print_blank_line()
        self.ui_helper.print_line("    Enter start date: (dd/mm/yy)")
        self.ui_helper.print_line("    Enter end date: (dd/mm/yy)")
        self.ui_helper.print_blank_line()
        self.ui_helper.print_footer()
        start_date = input("Input: ")
        end_date = input("Input: ")
        return start_date, end_date
    
    def show_utilization_report(self, header_str, start_date, end_date):
        pass
    

