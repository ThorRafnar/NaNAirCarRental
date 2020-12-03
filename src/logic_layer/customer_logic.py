
class CustomerLogic():
    def __init__(self, data_api):
        self.data_api = data_api


    def get_customers(self):
        return self.data_api.get_customers()

    def change_customer_info(self, attribute_list):
        return self.data_api.change_customer_info(attribute_list)

    def add_customer(self, cust):
        return self.data_api.add_customer(cust)
