class ChiftException(Exception):
    def __init__(self, message, error_code=None, detail=None):
        super().__init__(message)

        self.message = message
        self.error_code = error_code or ""
        self.detail = detail or ""

    def __str__(self):
        return f"Chift Exception: {self.error_code} {self.message} {self.detail}"


class ChiftProcessControlledException(ChiftException):
    """Exception for handle controlled errors in process execution"""
    def __init__(self, message, error_status_code, error_code=None, detail=None):
        super().__init__(message, error_code, detail)
        self.error_status_code = error_status_code

    def __str__(self):
        return (f"Chift Exception: {self.error_code} {self.message} {self.detail}. "
                f"Error Process status code - {self.error_status_code}")
