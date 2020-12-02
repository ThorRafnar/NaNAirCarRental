class VehicleLogic():

    def __init__(self, data_api):
        self.data_api = data_api

    def all_vehicles_to_list(self):
        ''' Gets vehicle list from data and sends it to UI '''
        return self.data_api.all_vehicles_to_list()

    def register_new_vehicle(self, new_vehicle):
        """ sends new vecicle to database to register """
        self.data_api.register_new_vehicle(new_vehicle)

    def change_vehicle_condition(self, vehicle_id, status):
        ''' Sends vehicle id and condition status to data layer '''
        self.data_api.change_vehicle_condition(vehicle_id, status)
    
    def list_vehicles_by_status(self, status):
        ''' Gets status to filter by from UI and finds vehicles by status in vehicle list '''
        vehicle_list = self.all_vehicles_to_list()
        status_list = []
        for vehicle in vehicle_list:
            if vehicle.status == status:
                status_list.append(vehicle)
        
        return status_list
