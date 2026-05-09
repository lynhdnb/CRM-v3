from enum import Enum


class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    ORGANIZATION_ADMIN = "organization_admin"
    TEACHER = "teacher"
    STUDENT = "student"
    PARENT = "parent"
    ACCOUNTANT = "accountant"


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"
