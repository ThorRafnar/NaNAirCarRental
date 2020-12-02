class VehicleLogic():

    def __init__(self, data_api):
        self.data_api = data_api

    def register_new_vehicle(self, new_vehicle):
        """ sends new vecicle to database to register """
        return self.data_api.register_new_vehicle(new_vehicle)

    def change_vehicle_condition(self, vehicle):
        return self.data_api.change_vehicle_condition(vehicle_id, status)
