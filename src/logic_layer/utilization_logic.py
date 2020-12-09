from datetime import datetime,date

class UtilizationLogic():
    def __init__(self, data_api):
        self.data_api = data_api
    
    def get_utilization_logs(self):
        return self.data_api.get_utilization()
    
    def get_utilization_for_location(self, location):
        util_list = self.get_utilization_logs()
        location_list = [log for log in util_list if log.location == location]
        type_dict = self.util_by_vehicle_type_dict(location_list)
    
    def util_by_vehicle_type_dict(self, a_list):
        type_dict = {}
        vehicle_dict = self.create_vehicle_utilization_dict(a_list)
        for key,value in vehicle_dict.items():
            util = self.calc_vehicle_utilization(value[0],value[1],value[2])
            vehicle_list = [key,value[0],value[1],util]
            if value[3] not in type_dict:
                type_dict[value[3]] = [vehicle_list]
            else:
                type_dict[value[3]].append(vehicle_list)
        print(type_dict)
                
    
    def create_vehicle_utilization_dict(self, a_list):
        vehicle_dict = {}
        for vehicle in a_list:
            # pic_date = datetime.strptime(vehicle.pick_up, '%d/%m/%Y')
            # ret_date = datetime.strptime(vehicle.return_date, '%d/%m/%Y')
            d,m,y = int(vehicle.pick_up[:2]),int(vehicle.pick_up[3:5]),int(vehicle.pick_up[6:])
            e_d,e_m,e_y = int(vehicle.return_date[:2]),int(vehicle.return_date[3:5]),int(vehicle.return_date[6:])
            pic_date = date(y, m, d)
            ret_date = date(e_y, e_m, e_d)
            delta = ret_date - pic_date
            vehicle_name = f'{vehicle.manufacturer} {vehicle.model}'
            if vehicle_name not in vehicle_dict:
                vehicle_dict[vehicle_name] = [pic_date, ret_date,delta.days,vehicle.vehicle_type]
            else:
                if vehicle_dict[vehicle_name][0] > pic_date:
                    vehicle_dict[vehicle_name][0] = pic_date
                if vehicle_dict[vehicle_name][1] < ret_date:
                    vehicle_dict[vehicle_name][1] = ret_date
                vehicle_dict[vehicle_name][2] += delta.days
        return vehicle_dict
    
    def calc_vehicle_utilization(self,start_date,end_date,loan_time):
        delta = end_date - start_date
        period = delta.days
        util_rate = (loan_time/period) * 100
        return round(util_rate)
