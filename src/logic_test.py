from logic_layer.logic_api import LogicAPI
from model_layer.employee import Employee
from model_layer.vehicle import Vehicle
from model_layer.contract import Contract
from model_layer.destination import Destination
from model_layer.vehicle_type import VehicleType
from model_layer.profit import Profit



r = LogicAPI()
#emp = Employee('Jón Jónsson','Melagerð 99','200','300279-1289','+356 5815432','+354 6890012','jj@nan.is','KEF')
# veh = Vehicle('Yedoo','Trexx','Light road','OK','2020','Orange',None,'KUS',None)
# dest = r.find_vehicle('1')
# print(dest)
# con = Contract(None,'320866-9910','250645-9999','2','01/12/2020','05/12/2020')
# amm = r.create_new_contract(con)
#blah = r.change_contract_status('5','paid')
# ty = r.get_types_rate('Medium off-road')
# print(ty)
# loc = Destination('Greenland','Kulusuk','+299 999 200','10:30 - 15:30','KUS')
# veh = VehicleType('Medium road','All','1100')


#r.change_contract_status('3', 'returned')

# r.get_filtered_vehicle('28/11/2020', '01/12/2020',loc,veh)
#r.change_contract_dates('4','02/12/2020','10/12/2020')

# hey = Contract("1",'320866-9910','250645-9999','2','01/12/2020','05/12/2020',"sadf","sadf","sadfafsd","sadf","sadf","sadfafsd" )
# r.get_utilization_for_location('Thorshavn')
# # r.change_contract(hey)

# hey = Contract("2",'320866-9910','250645-9999','2','01/12/2020','05/12/2020',"sadf","sadf","sadfafsd","sadf","sadf","sadfafsd" )

# r.get_paid_and_unpaid_contracts("320866-9910", "01/12/2010", "01/12/2021")
hey = r.get_vehicle_by_location("Kulusuk")
print(hey)

for i in hey:
    print(i.location)
