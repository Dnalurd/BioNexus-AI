"""Custom exception classes for the application."""


class BioNexusException(Exception):
    """Base exception for BioNexus AI application."""

    def __init__(self, message: str, code: str = "INTERNAL_ERROR", status_code: int = 500):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)


class AuthenticationException(BioNexusException):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, "AUTHENTICATION_ERROR", 401)


class AuthorizationException(BioNexusException):
    """Raised when user lacks required permissions."""

    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, "AUTHORIZATION_ERROR", 403)


class ResourceNotFoundException(BioNexusException):
    """Raised when a resource is not found."""

    def __init__(self, resource: str, resource_id: str | int):
        message = f"{resource} with id {resource_id} not found"
        super().__init__(message, "RESOURCE_NOT_FOUND", 404)


class ValidationException(BioNexusException):
    """Raised when validation fails."""

    def __init__(self, message: str, field: str = None):
        super().__init__(message, "VALIDATION_ERROR", 422)
        self.field = field


class ConflictException(BioNexusException):
    """Raised when resource already exists."""

    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, "CONFLICT_ERROR", 409)


class RateLimitException(BioNexusException):
    """Raised when rate limit is exceeded."""

    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, "RATE_LIMIT_ERROR", 429)


class ExternalServiceException(BioNexusException):
    """Raised when external service fails."""

    def __init__(self, service: str, message: str):
        full_message = f"External service {service} error: {message}"
        super().__init__(full_message, "EXTERNAL_SERVICE_ERROR", 502)


class DatabaseException(BioNexusException):
    """Raised when database operation fails."""

    def __init__(self, message: str = "Database operation failed"):
        super().__init__(message, "DATABASE_ERROR", 500)


class InvalidRequestException(BioNexusException):
    """Raised when request is invalid."""

    def __init__(self, message: str = "Invalid request"):
        super().__init__(message, "INVALID_REQUEST", 400)
