from ui_layer.ui_api import UIAPI
from ui_layer.ui_start_menu import UIStartMenu
import os  
# Get the size 
# of the terminal 
size = os.get_terminal_size() 
width = size.columns - 1 
height = size.lines
print(height)

f = UIStartMenu(width)
f.choose_location()