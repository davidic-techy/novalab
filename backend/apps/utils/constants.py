class FileTypes:
    ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'webp']
    ALLOWED_DOC_EXTENSIONS = ['pdf', 'docx', 'txt']
    MAX_UPLOAD_SIZE_MB = 10

class ErrorMessages:
    GENERIC = "Something went wrong. Please try again later."
    PERMISSION_DENIED = "You do not have permission to perform this action."
    NOT_FOUND = "The requested resource was not found."
    FILE_TOO_LARGE = f"File size exceeds the limit of {FileTypes.MAX_UPLOAD_SIZE_MB}MB."

class RegexPatterns:
    # Basic check for alphanumeric + hyphens (for slugs)
    SLUG = r'^[a-z0-9]+(?:-[a-z0-9]+)*$'
    # Basic phone number validation
    PHONE = r'^\+?1?\d{9,15}$'

class SystemConfig:
    # How long a signed URL for a private file remains valid (in seconds)
    SIGNED_URL_EXPIRY = 3600  # 1 hour