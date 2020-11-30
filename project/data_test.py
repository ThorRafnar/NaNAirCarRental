import sys
sys.path.append(sys.path[0] + "/..")
from project.data.data_main import DataMain


d = DataMain()
emp_list = d.get_employees()
for emp in emp_list:
    print(emp)