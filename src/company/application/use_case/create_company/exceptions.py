class CompanyCreationError(Exception):
    """Exception raised when there is an error creating a company."""
    pass

class InvalidCompanyDataError(Exception):
    """Exception raised when company data is invalid."""
    pass

class UnauthorizedCompanyCreationError(Exception):
    """Exception raised when an unauthorized user attempts to create a company."""
    pass

class DuplicateCompanyError(Exception):
    """Exception raised when attempting to create a company that already exists."""
    pass

class AdminUserNotFoundError(Exception):
    """Exception raised when the specified admin user is not found."""
    pass

