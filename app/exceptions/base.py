class PaymentException(Exception):
    def __init__(self,code:str,msg:str,status_code:int=400):
        self.code=code
        self.msg=msg
        self.status_code=status_code
        super().__init__(msg)