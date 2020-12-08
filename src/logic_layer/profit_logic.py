from datetime import date

class ProfitLogic():

    def __init__(self, data_api):
        self.data_api = data_api

    def add_profits(self, profits):
        self.data_api.add_profits(profits)


    def get_profits(self):
        return self.data_api.get_profits()

    def calculate_profits(self,start_date,end_date):
        ''' Returns total profits of given time '''
        profits = self.get_profits()
        total = 0
        d,m,y = int(start_date[:2]),int(start_date[3:5]),int(start_date[6:])
        e_d,e_m,e_y = int(end_date[:2]),int(end_date[3:5]),int(end_date[6:])
        s_date = date(y, m, d)
        e_date = date(e_y, e_m, e_d)

        for profit in profits:
            c_y, c_m, c_d = int(profit.date[0:4]), int(profit.date[5:7]), int(profit.date[8:])
            check_date = date(c_y, c_m, c_d)
            if s_date <= check_date <= e_date:
                total += int(profit.total)

        vehicle_profits = self.calculate_profits_by_vehicle(start_date, end_date)
        location_profits = self.calculate_profits_by_locataion(start_date, end_date)
        print(vehicle_profits, location_profits)
        return total, vehicle_profits, location_profits


    def calculate_profits_by_locataion(self, start_date, end_date):
        ''' ^ puts profits of each locations as a keys and values in dictonary '''
        location_profits = {}
        profits = self.get_profits()
        d,m,y = int(start_date[:2]),int(start_date[3:5]),int(start_date[6:])
        e_d,e_m,e_y = int(end_date[:2]),int(end_date[3:5]),int(end_date[6:])
        s_date = date(y, m, d)
        e_date = date(e_y, e_m, e_d)

        for profit in profits:
            c_y, c_m, c_d = int(profit.date[0:4]), int(profit.date[5:7]), int(profit.date[8:])
            check_date = date(c_y, c_m, c_d)
            if s_date <= check_date <= e_date:
                if profit.location not in location_profits:
                    location_profits[profit.location] = int(profit.total)
                else:
                    location_profits[profit.location] += int(profit.total)
        return location_profits


    def calculate_profits_by_vehicle(self, start_date, end_date):
        ''' '''
        vehicle_profits = {}
        profits = self.get_profits()
        d,m,y = int(start_date[:2]),int(start_date[3:5]),int(start_date[6:])
        e_d,e_m,e_y = int(end_date[:2]),int(end_date[3:5]),int(end_date[6:])
        s_date = date(y, m, d)
        e_date = date(e_y, e_m, e_d)

        for profit in profits:
            print(profit.vehicle_type)
            c_y, c_m, c_d = int(profit.date[0:4]), int(profit.date[5:7]), int(profit.date[8:])
            check_date = date(c_y, c_m, c_d)
            if s_date <= check_date <= e_date:
                print(profit.vehicle_type)
                if profit.vehicle_type not in vehicle_profits:
                    vehicle_profits[profit.vehicle_type] = int(profit.total)
                else:
                    vehicle_profits[profit.vehicle_type] += int(profit.total)
            print(vehicle_profits)
            return vehicle_profits






