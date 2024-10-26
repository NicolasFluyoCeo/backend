class UserNotFoundException(Exception):
    pass


class TokenNotFoundException(Exception):
    pass


class TokenRevokedException(Exception):
    pass


class TokenExpiredException(Exception):
    pass


class InvalidTokenException(Exception):
    pass
