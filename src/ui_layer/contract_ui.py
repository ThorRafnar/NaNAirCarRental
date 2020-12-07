from model_layer.contract import Contract

class ContractUI():
    CREATE = "Create new contract"
    FIND = "Find a contract"



    def __init__(self, ui_helper, logic_api):
        self.ui_helper = ui_helper
        self.logic_api = logic_api
        self.options_dict = {
            "1": self.CREATE, 
            "2": self.FIND, 
        }