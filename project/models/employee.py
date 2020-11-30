from person import Person

class Employee(Person):

    def __init__(self, name, address, postal_code, social_security_number, home_phone, mobile_phone, email, work_area):
        super().__init__(name, address, postal_code, social_security_number, home_phone, mobile_phone, email)
        self.location = work_area