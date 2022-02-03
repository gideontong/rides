class person:
    def __init__(self, data: dict):
        self.fname = data['fname']
        self.lname = data['lname']
        self.phone = data['phone']
        self.carrier = data['carrier']
        self.address = data['address']

    def start(self):
        pass
