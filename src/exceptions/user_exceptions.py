class UserAlreadyExistsError(Exception):
    def __init__(self, message: str = "User already exists"):
        self.message = message
        super().__init__(self.message)


class UserDoesNotExistsError(Exception):
    def __init__(self, message: str = "User does not exists"):
        self.message = message
        super().__init__(self.message)
