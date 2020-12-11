class VehicleTypeLogic():
    def __init__(self, data_api, vehicle_logic):
        self.data_api = data_api
        self.vehicle_logic = vehicle_logic
    
    def get_vehicle_types(self):
        ''' Returns a list of all vehicle types '''
        return self.data_api.get_all_vehicle_types()
    
    def create_new_type(self, vehicle_type):
        ''' Creates a new vehicle type in database '''
        self.data_api.new_vehicle_type(vehicle_type)

    def change_types_rate(self, type_name, new_rate):
        ''' finds a given vehicle type and changes its rate from given parameters '''
        self.data_api.change_vehicle_rate(new_rate, type_name)
    
    def get_types_rate(self, selected_type):
        ''' Searches for a vehicle type and returns it rate '''
        types_list = self.data_api.get_all_vehicle_types()
        rate = 0
        for t in types_list:
            if t.name.lower() == selected_type.lower():
                rate = int(t.rate)
                break
        return rate

    def filter_by_region(self, reg, start_date, end_date):
        ''' returns a list of vehicle types available from given region '''
        type_list = self.get_vehicle_types()
        vehicle_list = self.data_api.get_all_vehicles()
        availble_types = self.get_types_for_vehicles_location(reg, vehicle_list, start_date, end_date)
        availble_list = []
        for veh_type in type_list:
            if veh_type.name in availble_types:
                availble_list.append(veh_type)
                
        return availble_list
    
    def get_types_for_vehicles_location(self, location, a_list, start_date, end_date):
        ''' returns a list with all vehicle types with in certain location '''
        types_available = []
        for vehicle in a_list:
            if vehicle.location == location:
                is_available = self.vehicle_logic.check_vehicle_availability(vehicle.id, start_date, end_date)
                if is_available:
                    if vehicle.type not in types_available:
                        types_available.append(vehicle.type)
        return types_available

