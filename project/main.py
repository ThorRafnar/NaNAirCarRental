import sys
sys.path.append(sys.path[0] + "/..")
from project.ui.ui_main import UI_Main

a = UI_Main()
col = "work_area"
attribute = "Admin"
attribute_list = [(col, attribute)]
a.start()
a.new_employee()
# laga eitthvað