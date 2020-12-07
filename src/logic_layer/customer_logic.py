
class CustomerLogic():
    def __init__(self, data_api):
        self.data_api = data_api


    def get_customers(self):
        ''' Returns a list of customers as instances of Customer class from data layer '''
        return self.data_api.get_customers()
    
    def find_customer(self, new_ssn):
        ''' Takes an instance of Customer class for customer from UI and checks if he exist in database, returns an instance of that Customer back if found, else returns None '''
        cust_list = self.get_customers()
        cust_inst = None
        for cust in cust_list:
            if cust.ssn == new_ssn:
                cust_inst = cust
                break
        return cust_inst 

    def change_customer_info(self, attribute_list):
        ''' Sends a list of attributes to data layer to change given attribute for given employee '''
        return self.data_api.change_customer_info(attribute_list)

    def add_customer(self, cust):
        ''' Sends an instance of Customer class for new customer to data layer to write to database '''
        return self.data_api.add_customer(cust)
