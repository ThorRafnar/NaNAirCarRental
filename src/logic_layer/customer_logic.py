
class CustomerLogic():
    def __init__(self, data_api):
        self.data_api = data_api


    def get_customers(self):
        ''' Returns a list of customers as instances of Customer class from data layer '''
        return self.data_api.get_customers()

    def change_customer_info(self, attribute_list):
        ''' Sends a list of attributes to data layer to change given attribute for given employee '''
        return self.data_api.change_customer_info(attribute_list)

    def add_customer(self, cust):
        ''' Sends an instance of Customer class for new customer to data layer to write to database '''
        return self.data_api.add_customer(cust)
