"""
Custom storage backends for Backblaze B2
"""
from storages.backends.s3boto3 import S3Boto3Storage
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)


class B2Storage(S3Boto3Storage):
    """
    Custom storage backend for Backblaze B2 that handles B2-specific requirements.
    This backend works around B2's differences from S3, particularly around
    file existence checks that can cause 403 errors.
    """
    
    # Disable file overwrite check to prevent HeadObject calls
    # B2 will handle overwrites automatically
    file_overwrite = True
    
    def exists(self, name):
        """
        Override exists check to handle B2's HeadObject limitations.
        For B2, we'll skip the existence check to avoid 403 errors.
        The file will be uploaded regardless of whether it exists.
        """
        # Skip existence check for B2 to avoid 403 Forbidden errors
        # B2 handles file overwrites differently than S3
        # Always return False to allow upload to proceed
        return False
    
    def _save(self, name, content):
        """
        Override save to ensure B2-compatible upload.
        Handles file uploads without checking existence first.
        """
        # Ensure content is at the beginning
        if hasattr(content, 'seek'):
            content.seek(0)
        
        try:
            # Directly upload without checking existence
            # This bypasses any HeadObject calls that might cause 403 errors
            cleaned_name = self._normalize_name(self._clean_name(name))
            name = self._location + cleaned_name
            
            # Get the S3 connection
            connection = self.connection
            
            # Upload the file directly
            content_type = getattr(content, 'content_type', None) or 'application/pdf'
            
            # Use put_object directly to avoid existence checks
            connection.meta.client.put_object(
                Bucket=self.bucket_name,
                Key=name,
                Body=content,
                ContentType=content_type,
            )
            
            return cleaned_name
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            logger.error(f"B2 upload error: {error_code} - {e}")
            # Re-raise to let Django handle it
            raise
