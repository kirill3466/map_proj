from enum import StrEnum

# from pydantic import conint, constr


class Roles(StrEnum):
    admin = "admin"
    owner = "owner"
    user = "user"


# PrimaryKey = conint(gt=0, lt=2147483647)
# NameStr = constr(pattern=r"^(?!\s*$).+", strip_whitespace=True, min_length=3)
