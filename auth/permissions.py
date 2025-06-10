from fastapi import HTTPException
from starlette import status


from .auth import CurrUser


class RoleChecker:
    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles

    def __call__(self, user: CurrUser):
        if user.role in self.allowed_roles:
            return True
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="У вас недостаточно прав"
        )
