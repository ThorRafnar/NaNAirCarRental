class DestinationLogic():
    def __init__(self, data_api):
        self.data_api = data_api

    def get_destinations(self):
        ''' Sends a list of destinations as instances of Destination class to UI '''
        return self.data_api.get_destinations()

    def find_destination(self, iata):
        ''' Gets iata code from UI and checks if destination exists in database, returns an instance of Destination class for give destination if found, else returns None '''
        dest_list = self.get_destinations()
        dest_inst = None
        for dest in dest_list:
            if dest.iata == iata:
                dest_inst = dest
                break
        return dest_inst

    def create_destination(self, destination):
        ''' Gets an instance of Destination class from UI and sends it to data layer '''
        self.data_api.create_destination(destination)

    def destinations_option_list(self):
        ''' Returns destinations attributes for use in UI start screen '''
        dest_list = self.get_destinations()
        options_list = []
        admin = ('ADM', 'Administrator')
        for dest in dest_list:
            option_tuple = (dest.iata, dest.airport, dest.country)
            options_list.append(option_tuple)
        # Adds admin to the back of the list
        options_list.append(admin)
        return options_list