from enum import Enum

class PurchaseType(Enum):
    API_PURCHASE = "API Purchase"
    MANUAL_PURCHASE = "Manual Purchase"
    ONLY_STOCK = "Only Stock"