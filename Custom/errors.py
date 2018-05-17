
class ContentTypeError(Exception):
    """to be used when the content-type of the request is not supported. content_type should be a kwarg."""
    pass

class InvalidCredentialsError(Exception):
    "to be used when the entered user credentials are incorrect."
    pass

class InvalidPermissionsError(Exception):
    "to be used when the entered user's permissions are insufficient."
    pass
