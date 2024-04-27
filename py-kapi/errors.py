class APIException(Exception):
    pass

class BadRegion(APIException):
    pass

class InvalidParameter(APIException):
    pass

class Unauthorized(APIException):
    pass

class LoginFailure(APIException):
    pass

class NotFound(APIException):
    pass

class NotPurchased(APIException):
    pass

class BadRequest(APIException):
    pass

