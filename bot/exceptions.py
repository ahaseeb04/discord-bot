import abc

class CustomError(abc.ABC, Exception):
    def __init__(self, user=None, message=None):
        self.user = user
        self.message = message

class IllegalFormatError(CustomError):
    pass

class NotApprovedError(CustomError):
    pass

class DataNotFoundError(CustomError):
    pass

class WrongChannelError(CustomError):
    pass

class ShouldBeBannedError(CustomError):
    pass