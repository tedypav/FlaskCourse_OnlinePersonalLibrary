from enum import Enum


class ResourceStatus(Enum):
    read = "Read"
    pending = "To Read"
    dropped = "Dropped"

class UserRole(Enum):
    user = "user"
    admin = "admin"
