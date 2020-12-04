from logic_layer.logic_api import LogicAPI
from model_layer.employee import Employee
from model_layer.vehicle import Vehicle

r = LogicAPI()
#emp = Employee('Jón Jónsson','Melagerð 99','200','300279-1289','+356 5815432','+354 6890012','jj@nan.is','KEF')
veh = Vehicle('Yedoo','Trexx','Light road','OK','2020','Orange',None,'KUS',None)
dest = r.find_vehicle('1')
print(dest)