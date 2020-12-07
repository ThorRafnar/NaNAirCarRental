from logic_layer.logic_api import LogicAPI
from model_layer.employee import Employee
from model_layer.vehicle import Vehicle
from model_layer.contract import Contract


r = LogicAPI()
#emp = Employee('Jón Jónsson','Melagerð 99','200','300279-1289','+356 5815432','+354 6890012','jj@nan.is','KEF')
# veh = Vehicle('Yedoo','Trexx','Light road','OK','2020','Orange',None,'KUS',None)
# dest = r.find_vehicle('1')
# print(dest)
# con = Contract(None,'320866-9910','250645-9999','11','01/12/2020','03/12/2020')
# amm = r.create_new_contract(con)
blah = r.change_contract_status('4','paid')
# ty = r.get_types_rate('Medium off-road')
# print(ty)