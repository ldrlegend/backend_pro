from enum import Enum

class Status(Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    LOW_STOCK = "Low Stock"
    B2B_ONLY = "B2B Only"
    TEMPORARY = "Temporary"
    PREPARING = "Preparing"
    DELETED = "Deleted"
    ECOM_ONLY = "Ecom-Only"