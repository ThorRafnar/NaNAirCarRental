'''from data_layer.contract_data import ContractData
from model_layer.contract import ContractLogic

a = ContractLogic("aaa","aaa","aaa","aaa"
,"aaa","aaa","aaa","aaa","aaa","aaa",
"aaa","aaa","aaa","aaa","aaa","aaa","aaa")

ContractData.new_contract(self,a)'''

from logic_layer.logic_api import LogicAPI

r = LogicAPI()

the_dates = ["29/02/20", "32/12/19", "13/01/15", "010120"]

for the_date in the_dates:
    print(r.check_date(the_date))