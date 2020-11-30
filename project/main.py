import sys
sys.path.append(sys.path[0] + "/..")
from project.ui.ui_main import UI_Main

a = UI_Main()
col = "ssn"
attribute = "250645-9999"
attribute_list = [(col, attribute)]
a.start()
a.get_filtered_employees(attribute_list)
print("hello, world!")