class ReportUI():

    def __init__(self, ui_helper, logic_api):
        self.ui_helper = ui_helper
        self.logic_api = logic_api
        # self.options_dict = {
        #     "1": self.PROFIT_REPORTS,
        #     "2": self.UTIL_REPORTS,
        #     "3": self.BILLS,
        # }
    
    def show_options(self, header_str, error_msg=""):
        options_list = self.ui_helper.list_to_dict(self.options_dict)
        pass
        

