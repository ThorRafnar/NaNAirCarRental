# Main File for testing
# Do not change this shit
from vehicle_data import VehicleData

a = VehicleData()
a = a.all_vehicles_to_list()
for vehicle in a:
    print(vehicle)