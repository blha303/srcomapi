

class APIRequestException(Exception):
    def __init__(self, message, data):
        super(APIRequestException, self).__init__(message)
        self.data = data

class APINotProvidedException(Exception):
    pass
