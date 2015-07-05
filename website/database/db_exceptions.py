class NoInternetAccess(Exception):
    """Raised when the service cannot connect to the internet"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value

class NoDatabaseAccess(Exception):
    """Raised when the service cannot connect to the database"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value
