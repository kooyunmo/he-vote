class ServiceError(Exception):
    default_code = "service"
    default_detail = "Service Error"
    http_code = 409

    def __init__(self, detail=None, code=None):
        self.code = code or self.default_code
        self.detail = detail or self.default_detail

    def __str__(self):
        return f"Error {self.code} {self.detail}"


class InternalServiceError(ServiceError):
    default_code = "service_interal"
    default_detail = "Internal Service Error"
    http_code = 500


class UserServiceError(ServiceError):
    default_code = "service_runtime"
    default_detail = "Service Runtime Error"
    http_code = 409


class ParseError(UserServiceError):
    default_code = "bad_request"
    default_detail = "Bad request"
    http_code = 400


# Exception raised When not authenticated
class NotAuthenticatedError(UserServiceError):
    default_code = "not_authenticated"
    default_detail = "Not Authenticated"
    http_code = 401


# Exception raised when authenticated but operation not permitted for user
class PermissionDeniedError(UserServiceError):
    default_code = "permission_denied"
    default_detail = "Permission Denied"
    http_code = 403


class InvalidCredentialError(UserServiceError):
    default_code = "invalid_credential"
    default_detail = "Credential is invalid or deleted"
    http_code = 404


class InvalidAttachmentError(UserServiceError):
    default_code = "invalid_attachment"
    default_detail = "Attachment is invalid"
    http_code = 400


class NotFoundError(UserServiceError):
    default_code = "not_found"
    default_detail = "Resource you have requested is not found"
    http_code = 404


class ServiceTimeoutError(UserServiceError, TimeoutError):
    default_code = "service_timeout_error"
    default_detail = "Timed out"
    http_code = 409
