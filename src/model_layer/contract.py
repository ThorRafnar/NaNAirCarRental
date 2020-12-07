class Contract:
    def __init__(self, contract_id, customer_ssn, employee_ssn, vehicle_id, loan_date, end_date, base_price=None, contract_created=None, return_date=None, extensions=0, total=None, status='pending'):
        self.contract_id = contract_id
        self.customer_ssn = customer_ssn
        self.employee_ssn = employee_ssn
        self.vehicle_id = vehicle_id
        self.loan_date = loan_date
        self.end_date = end_date
        self.base_price = base_price
        self.contract_created = contract_created
        self.return_date = return_date
        self.extensions = extensions
        self.total = total
        self.status = status

        