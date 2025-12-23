from app.utils.error_codes import ErrorCodes
from app.exceptions.base import PaymentException

class WalletNotFoundException(PaymentException):
    def __init__(self,wallet_id:int):
        super().__init__(
            code=ErrorCodes.WALLET_NOT_FOUND,
            msg=f"Wallet not found with id: {wallet_id}",
            status_code=404
        )
class InsufficientBalanceException(PaymentException):
    def __init__(self, wallet_id: int, amount: float,balance:float):
        super().__init__(
            code=ErrorCodes.INSUFFICIENT_BALANCE,
            msg=f"Wallet {wallet_id} has insufficient balance. "
                f"Attempted: {amount} and available balance :{balance}",
            status_code=400
        )
class InactiveWalletException(PaymentException):
        def __init__(self, wallet_id: int):
            super().__init__(
                code=ErrorCodes.INSUFFICIENT_BALANCE,
                msg=f"Wallet with id: {wallet_id} was inactive. active wallet first ",
                status_code=400
            )
class WalletException(PaymentException):
     def __init__(self,sender_id:int,rec_id:int):
          super().__init__(
               code=ErrorCodes.SAME_WALLET,
               msg=f"sender id: {sender_id} and reciver id: {rec_id} must be different", status_code=400
            )
          
class NegativeBalException(PaymentException):
     def __init__(self,sender_id:int,amount:float):
          super().__init__(
               code=ErrorCodes.TRANSACTION_FAILED,
               msg=f"sending amount should not be negative or zero.{amount} should be more than zero", status_code=400
            )