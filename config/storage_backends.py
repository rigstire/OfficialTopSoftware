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
        Catches any HeadObject 403 errors and retries without existence check.
        """
        # Ensure content is at the beginning
        if hasattr(content, 'seek'):
            content.seek(0)
        
        try:
            # Use parent's _save method
            # Since we override exists() to return False, it shouldn't check for file existence
            return super()._save(name, content)
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            error_message = str(e)
            
            # If it's a HeadObject 403 error, the parent might still be checking
            # In this case, we need to upload directly without any checks
            if error_code in ('403', 'Forbidden') and 'HeadObject' in error_message:
                logger.warning(f"B2 HeadObject 403 detected, uploading directly: {name}")
                
                # Reset content
                if hasattr(content, 'seek'):
                    content.seek(0)
                
                # Prepare the file name using parent's method
                normalized_name = self._normalize_name(name)
                normalized_name = normalized_name.replace('\\', '/')
                
                # Get content type
                content_type = getattr(content, 'content_type', 'application/pdf')
                if not content_type and normalized_name.lower().endswith('.pdf'):
                    content_type = 'application/pdf'
                
                # Use the boto3 client directly to upload
                # This bypasses all existence checks
                client = self.connection.meta.client
                
                # Read content
                if hasattr(content, 'read'):
                    file_content = content.read()
                else:
                    file_content = content
                
                # Upload directly
                client.put_object(
                    Bucket=self.bucket_name,
                    Key=normalized_name,
                    Body=file_content,
                    ContentType=content_type,
                )
                
                return normalized_name
            else:
                # Re-raise other errors
                logger.error(f"B2 upload error: {error_code} - {e}")
                raise
