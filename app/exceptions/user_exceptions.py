from app.exceptions.base import PaymentException
from app.utils.error_codes import ErrorCodes

class UserNotFoundException(PaymentException):
    def __init__(self, user_id: int):
        super().__init__(
            code=ErrorCodes.USER_NOT_FOUND,
            msg=f"User not found with id: {user_id}",
            status_code=404
        )
class EmailnotFOundException(PaymentException):
    def __init__(self, user_email:str):
        super().__init__(   
            code=ErrorCodes.USER_NOT_FOUND   ,
            msg=f"User not found with email: {user_email}"   , 
            status_code =404
        ) 
class MobilenotFOundException(PaymentException):
    def __init__(self, user_mobile:str):
        super().__init__(   
            code=ErrorCodes.USER_NOT_FOUND   ,
            msg=f"User not found with email: {user_mobile}"   , 
            status_code =404
        )     
        

class UnauthorizedException(PaymentException):
    def __init__(self, user_id: int):
        super().__init__(
            code=ErrorCodes.UNAUTHORIZED,
            msg=f"No authorization for user with id: {user_id}",
            status_code=401
        )
class InvalidCredException(PaymentException):
    def __init__(self):
        super().__init__(
            code=ErrorCodes.UNAUTHORIZED,
            msg=f"invalid username or password",
            status_code=401
        )

class UserForbidden(PaymentException):
    def __init__(self, user_id: int):
        super().__init__(
            code=ErrorCodes.USER_FORBIDDEN,
            msg=f"No access for user with id: {user_id}",
            status_code=403
        )

class InvalidUserException(PaymentException):
    def __init__(self, user_id: int):
        super().__init__(
            code=ErrorCodes.INVALID_USER,
            msg=f"Invalid user with id: {user_id}",
            status_code=400
        )
