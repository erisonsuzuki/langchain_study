# core/exceptions.py
class ServiceExecutionError(Exception):
    """Custom exception for errors that occur during a service's execution."""
    def __init__(self, message: str, original_exception: Exception = None):
        self.message = message
        self.original_exception = original_exception
        super().__init__(self.message)
