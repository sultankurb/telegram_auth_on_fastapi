class ApplicationException(Exception):
    def __init__(self, message: str = "Fatal error in business logic"):
        self.message = message
        super().__init__(self.message)


class NotFoundException(ApplicationException):
    def __init__(self, message: str = "Entity not found"):
        super().__init__(message)


class ForbiddenException(ApplicationException):
    def __init__(self, message: str = "You are not allowed to to this action"):
        super().__init__(message)
