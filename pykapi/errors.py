class APIException(Exception):
    def __init__(self, response):

        response_content = response.json()

        self.status_code = response.status_code
        self.response_code = response_content["response_code"]
        self.error_message = response_content["error_message"]
        self.error_time = response_content["server_time"]

    def __repr__(self):
        return f"<{self.__class__.__name__} status_code={self.status_code} response_code={self.response_code}>"

    def __str__(self):
        return f"{self.error_time} : HTTP Status : {self.status_code} response code : {self.response_code} :: {self.error_message}"

class BadRegion(APIException):
    def __init__(self, response):
        super().__init__(response)

class InvalidParameter(APIException):
    def __init__(self, response):
        super().__init__(response)

class Unauthorized(APIException):
    def __init__(self, response):
        super().__init__(response)

class LoginFailure(APIException):
    def __init__(self, response):
        super().__init__(response)

class NotFound(APIException):
    def __init__(self, response):
        super().__init__(response)

class NotPurchased(APIException):
    def __init__(self, response):
        super().__init__(response)

class BadRequest(APIException):
    def __init__(self, response):
        super().__init__(response)


