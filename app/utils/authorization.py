from app.models.user import User
from app.exceptions.user_exceptions import UserForbidden

def ownership(current:int,owner_id:int):
    if current != owner_id:
        raise UserForbidden(current)
    