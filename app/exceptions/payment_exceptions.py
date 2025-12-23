from app.exceptions.base import PaymentException
from app.utils.error_codes import ErrorCodes

class TxnNotFoundException(PaymentException):
    def __init__(self,id:int):
        super().__init__(
            code=ErrorCodes.TRANSACTION_NOT_FOUND, 
            msg=F"Transaction was not found with id: {id}", status_code=404
        )