from logic_layer.logic_api import LogicAPI
from model_layer.employee import Employee

r = LogicAPI()

r.find_employee(Employee('Jón Jónsson','Melagerð 99','200','300279-1289','+356 5815432','+354 6890012','jj@nan.is','KEF'))