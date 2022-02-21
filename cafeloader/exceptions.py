class NaverCafeError(Exception):
    """
    Base Exception for this script.
    :note: This exception should not be raised directly
    """
class GetIframeContentError(NaverCafeError):
    pass