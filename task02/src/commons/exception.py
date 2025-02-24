class ApplicationException(Exception):
    def __init__(self, statusCode, message):
        super().__init__(message)
        self.statusCode = statusCode
        self.message = message
