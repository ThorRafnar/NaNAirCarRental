from datetime import datetime,date

class UtilizationLogic():
    def __init__(self, data_api):
        self.data_api = data_api
    
    def get_utilization_logs(self):
        ''' Returns a list of all utilization logs '''
        return self.data_api.get_utilization()
    
    def get_utilization_for_location(self, location):
        ''' Find and returns a list of all utilization logs for given location '''
        util_list = self.get_utilization_logs()
        location_list = [log for log in util_list if log.location == location]
        type_dict = self.util_by_vehicle_type_dict(location_list)
        
        return type_dict
    
    def util_by_vehicle_type_dict(self, a_list):
        ''' Returns a dictionary of utilization log from list with vehicle type as key and value as list of dictionaries with vehicle name as key '''
        type_dict = {}
        vehicle_dict = self.create_vehicle_utilization_dict(a_list)
        for key,value in vehicle_dict.items():
            util = self.calc_vehicle_utilization(value[1],value[2],value[3])
            vehicle_list = [key,value[0],value[1],value[2],util]
            if value[4] not in type_dict:
                type_dict[value[4]] = [vehicle_list]
            else:
                type_dict[value[4]].append(vehicle_list)
        return type_dict
                
    
    def create_vehicle_utilization_dict(self, a_list):
        ''' Creates a dictionary of utilization logs for each vehicle with vehicle ID as key and value as list of vehicla name, first usage date, last usage date and percentage of vehicle usage over that period '''
        vehicle_dict = {}
        for vehicle in a_list:
            d,m,y = int(vehicle.pick_up[:2]),int(vehicle.pick_up[3:5]),int(vehicle.pick_up[6:])
            e_d,e_m,e_y = int(vehicle.return_date[:2]),int(vehicle.return_date[3:5]),int(vehicle.return_date[6:])
            pic_date = date(y, m, d)
            ret_date = date(e_y, e_m, e_d)
            delta = ret_date - pic_date
            vehicle_name = f'{vehicle.manufacturer} {vehicle.model}'
            if vehicle.ID not in vehicle_dict:
                vehicle_dict[vehicle.ID] = [vehicle_name, pic_date, ret_date,delta.days,vehicle.vehicle_type]
            else:
                if vehicle_dict[vehicle.ID][1] > pic_date:
                    vehicle_dict[vehicle.ID][1] = pic_date
                if vehicle_dict[vehicle.ID][2] < ret_date:
                    vehicle_dict[vehicle.ID][2] = ret_date
                vehicle_dict[vehicle.ID][3] += delta.days
        return vehicle_dict
    
    def calc_vehicle_utilization(self,start_date,end_date,loan_time):
        ''' Calculates and returns a percentage of utilization over given period '''
        delta = end_date - start_date
        period = delta.days
        # Changes loan time or period to 1 day if loan_time or period is 0 because if vehicle is returned on the same day it is rented it calculates usage as 0 but should be 1 because if customer rents a vehcile than he pays for a days usage not hours usage
        if loan_time == 0: 
            loan_time = 1
        if period == 0:
            period = 1
        if loan_time == 1 and period == 1: # Returns a 100% usage if both loan_time and period is 1
            return 100
        else:
            util_rate = (loan_time/period) * 100
            return round(util_rate)
