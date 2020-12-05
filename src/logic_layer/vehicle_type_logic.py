class VehicleTypeLogic():
    def __init__(self, data_api):
        self.data_api = data_api
    
    def get_vehicle_types(self):
        return self.data_api.get_all_vehicle_types()
    
    def create_new_type(self, vehicle_type):
        self.data_api.new_vehicle_type(vehicle_type)

    def change_types_rate(self, type_name, new_rate):
        self.data_api.change_vehicle_rate(new_rate, type_name)

    def filter_by_region(self, reg):
        types_list = self.data_api.get_all_vehicle_types()
        region_list = [t for t in types_list if t.region == reg]
        return region_list

