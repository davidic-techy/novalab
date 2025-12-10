from django.conf import settings
from django.core.files.storage import default_storage
from .constants import SystemConfig

class StorageService:
    """
    Wrapper around Django's storage backend.
    """
    
    @staticmethod
    def upload_file(file_obj, destination_path):
        """
        Saves a file to the configured storage (GCS or Local).
        Returns the relative path.
        """
        try:
            # default_storage handles the logic based on settings.py
            path = default_storage.save(destination_path, file_obj)
            return path
        except Exception as e:
            print(f"File Upload Error: {e}")
            return None

    @staticmethod
    def get_public_url(file_path):
        """
        Returns the publicly accessible URL.
        """
        if not file_path:
            return None
        return default_storage.url(file_path)

    @staticmethod
    def get_signed_url(file_path, expiration=SystemConfig.SIGNED_URL_EXPIRY):
        """
        Generates a temporary signed URL for private files on GCS.
        Falls back to standard URL in local dev.
        """
        if not file_path:
            return None

        # Check if we are using GCS
        if hasattr(default_storage, 'bucket'):
            try:
                blob = default_storage.bucket.blob(file_path)
                return blob.generate_signed_url(expiration=expiration)
            except Exception as e:
                print(f"GCS Signing Error: {e}")
                return None
        
        # Local Development fallback
        return default_storage.url(file_path)