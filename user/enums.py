from django_enumfield import enum


class RoleTypeEnum(enum.Enum):
    ADMIN = 1
    MANAGER = 2
    USER = 3

    labels = {
        ADMIN: "Admin",
        MANAGER: "Manager",
        USER: "User",
    }
