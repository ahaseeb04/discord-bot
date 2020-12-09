import abc

class CustomError(abc.ABC, Exception):
    def __init__(self, user=None):
        self.user = user

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