class VehicleLogic():

    def __init__(self, data_api):
        self.data_api = data_api

    def all_vehicles_to_list(self):
        ''' Gets vehicle list from data and sends it to UI '''
        return self.data_api.get_all_vehicles()

    def find_vehicle(self, veh_id):
        ''' Gets vehicle id from UI, looks for vehicle in database and returns an instance of Vehicle class if found, else returns None back to UI '''
        vehicle_list = self.all_vehicles_to_list()
        is_vehicle = None
        for vehicle in vehicle_list:
            if vehicle.id == veh_id:
                is_vehicle = vehicle
        return is_vehicle

    def register_new_vehicle(self, new_vehicle):
        """ sends new vecicle to database to register """
        new_id = self.add_id_to_vehicle(new_vehicle)
        new_vehicle.id = new_id
        airport = self.iata_to_airport(new_vehicle)
        new_vehicle.location = airport
        self.data_api.register_new_vehicle(new_vehicle)
    
    def add_id_to_vehicle(self, new_vehicle):
        ''' Checks what is the last id in database and adds + 1 to add to new vehicle '''
        vehicle_list = self.all_vehicles_to_list()
        last_id = vehicle_list[-1].id
        new_id = int(last_id) + 1
        return new_id
    
    def iata_to_airport(self,new_vehicle):
        ''' Converts iata code to airport location in Vehicle.location '''
        dest_list = self.data_api.get_destinations()
        airport = ''
        for dest in dest_list:
            if dest.iata.lower() == new_vehicle.location.lower():
                airport = dest.airport
        return airport

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
