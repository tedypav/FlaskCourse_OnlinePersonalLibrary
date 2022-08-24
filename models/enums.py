from enum import Enum


class ResourceStatus(Enum):
    """
    A simple Enum class for the possible resource statuses.
    """

    read = "Read"
    pending = "To Read"
    dropped = "Dropped"


class UserRole(Enum):
    """
    A simple Enum class for the possible user roles. This is a preparation for future application features.
    """

    user = "user"
    admin = "admin"
