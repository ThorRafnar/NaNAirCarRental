from datetime import datetime, date

class VehicleLogic():

    def __init__(self, data_api, customer_logic):
        self.data_api = data_api
        self.customer_logic = customer_logic

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
        self.data_api.change_vehicle_condition(status, vehicle_id)
    
    def list_vehicles_by_status(self, status):
        ''' Gets status to filter by from UI and finds vehicles by status in vehicle list '''
        vehicle_list = self.all_vehicles_to_list()
        status_list = []
        for vehicle in vehicle_list:
            if vehicle.status == status:
                status_list.append(vehicle)
        
        return status_list
    
    def get_filtered_vehicle(self,start_date,end_date,location,vehicle_type):
        ''' Filters vehicles to find if vehicle is available for rent '''
        vehicle_list = self.all_vehicles_to_list()
        filtered_list = []
        for vehicle in vehicle_list:
            if vehicle.location.lower() == location.airport.lower() and vehicle.type.lower() == vehicle_type.name.lower():
                is_available = self.check_vehicle_availability(vehicle.id,start_date,end_date)
                if is_available:
                    filtered_list.append(vehicle)
        return filtered_list
    
    def check_vehicle_availability(self,veh_id,start_date,end_date):
        ''' Check vehicle availability from status first, then potential loan dates '''
        s_date = datetime.strptime(start_date, '%d/%m/%Y')
        e_date = datetime.strptime(end_date, '%d/%m/%Y')
        is_vehicle = self.find_vehicle(veh_id)
        is_available = False

        contract_list = self.data_api.list_all_contracts()
        veh_contracts = []
        print(is_vehicle.status)
        if is_vehicle.status.lower() != 'workshop':
            for cont in contract_list:
                if cont.vehicle_id == veh_id:
                    veh_contracts.append(cont)

            if not veh_contracts:
                is_available = True
            else:
                for veh_cont in veh_contracts:
                    veh_start_date = datetime.strptime(veh_cont.loan_date, '%d/%m/%Y')
                    veh_end_date = datetime.strptime(veh_cont.end_date, '%d/%m/%Y')

                    if s_date > veh_end_date or e_date < veh_start_date:
                        is_available = True
                    else:
                        is_available = False
                        break

        return is_available

    def match_licenses(self, customer_ssn, vehicle_id):
        cust = self.customer_logic.find_customer(customer_ssn)
        vehicle = self.find_vehicle(vehicle_id)
        customer_licenses = cust.licenses.split('-')
        vehicle_license = vehicle.license_type
        does_match = False
        if vehicle_license.lower() == 'none':
            does_match = True
        else:
            for c_license in customer_licenses:
                if c_license.lower() == vehicle_license.lower():
                    does_match = True
        
        return does_match

    def licenses_options_list(self):
        vehicles_list = self.all_vehicles_to_list()
        licenses_list = []
        for vehicle in vehicles_list:
            if vehicle.license_type not in licenses_list and vehicle.license_type.lower() != 'none':
                licenses_list.append(vehicle.license_type)
        return licenses_list

    def get_vehicle_by_location(self, location):
        '''returns a list with instances of all vehicles in set location'''
        ret_list = []
        vehicles = self.all_vehicles_to_list()
        for vehicle in vehicles:
            if vehicle.location == location:
                ret_list.append(vehicle)
        return ret_list
        

        





    
            
        
        

