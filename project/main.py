import sys
sys.path.append(sys.path[0] + "/..")
from project.ui.ui_main import UI_Main

a = UI_Main()
col = "work_area"
attribute = "Admin"
attribute_list = [(col, attribute)]
a.start()
<<<<<<< HEAD
a.get_administrators()
a.new_employee()
=======
a.get_filtered_employees(attribute_list)
>>>>>>> efe91c53425670bc46a9fba2179c86439ef175bc
