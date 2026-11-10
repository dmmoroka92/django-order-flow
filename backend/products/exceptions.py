from rest_framework.exceptions import APIException


class InsufficientStockAPIError(APIException):
    status_code = 409
    default_detail = "Insufficient stock"
    default_code = "insufficient_stock"
