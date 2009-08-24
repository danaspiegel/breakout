
class InactiveSessionException(Exception):
    """
    Raised when a session is inactive, and must be active to perform the action
    """
    pass

class InvalidSessionCheckoutException(Exception):
    """ Raised when a session is in the wrong status or user has already checked out """
    pass
