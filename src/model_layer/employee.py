class Employee():

    def __init__(self, name, address, postal_code, social_security_number, home_phone, mobile_phone, email, work_area):
        self.name = name
        self.address = address
        self.postal_code = postal_code
        self.ssn = social_security_number
        self.home_phone = home_phone
        self.mobile_phone = mobile_phone
        self.email = email
        self.work_area = work_area



    def __str__(self):
        return f"Name: {self.name}, Work Location: {self.work_area}"