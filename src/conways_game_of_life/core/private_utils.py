from functools import wraps


def property_setter_error_handle(func):
    """
    Decorator that emits the 'property_setter_error_signal' Signal
    If the error occurred in the property setter method.
    """

    @wraps(func)
    def wrapper(self, value):
        try:
            func(self, value)  # Call the original setter function
        except (ValueError, TypeError, AttributeError) as e:
            error_message = str(e)
            func_name = func.__name__
            self.property_setter_error_signal.emit(func_name, error_message)

    return wrapper
