class Contract:
    def __init__(self, name, ssn, phone, address, email, date_from, date_to, vehicle_id, location,
    vehicle_status, employee_id, loan_date, return_date, total, loan_status,contract_id, contract_status):
        self.name = name
        self.ssn = ssn
        self.phone = phone
        self.address = address
        self.email = email
        self.date_from = date_from
        self.date_to = date_to
        self.vehicle_id = vehicle_id
        self.location = location
        self.vehicle_status = vehicle_status
        self.employee_id = employee_id
        self.loan_date = loan_date
        self.return_date = return_date
        self.loan_status = loan_status
        self.total = total
        self.contract_id = contract_id
        self.contract_status = contract_status