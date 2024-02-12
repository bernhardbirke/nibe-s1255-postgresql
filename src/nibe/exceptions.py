# /exceptions.py


class WrongData(Exception):
    """Raised when wrong data."""


class DataCollectionError(Exception):
    """Raised when an Error at Data Collection Occurs"""


class UnknownRegisterTypeError(Exception):
    """Raised when the Registertype is unknown"""


class NoConnectionError(Exception):
    """Raised when no connection is established. Check nibe_ip and nibe_port."""
