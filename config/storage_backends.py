"""
Custom storage backends for Backblaze B2
"""
from storages.backends.s3boto3 import S3Boto3Storage
from botocore.exceptions import ClientError
from django.conf import settings
import logging
import boto3
from botocore.config import Config

logger = logging.getLogger(__name__)


def clean_credential_for_boto3(value):
    """Clean credential value specifically for boto3 (removes quotes, newlines, but keeps spaces)"""
    if not value:
        return ''
    # Convert to string
    value = str(value)
    # Remove surrounding quotes
    value = value.strip().strip('"').strip("'")
    # Remove newlines, tabs, but keep spaces (some keys might have spaces)
    value = value.replace('\n', '').replace('\r', '').replace('\t', '')
    # Remove any non-printable characters
    value = ''.join(c for c in value if c.isprintable())
    # Final strip to remove leading/trailing spaces
    value = value.strip()
    return value


class B2Storage(S3Boto3Storage):
    """
    Custom storage backend for Backblaze B2 that handles B2-specific requirements.
    This backend works around B2's differences from S3, particularly around
    file existence checks that can cause 403 errors.
    """
    
    # Disable file overwrite check to prevent HeadObject calls
    # B2 will handle overwrites automatically
    file_overwrite = True
    
    def __init__(self, *args, **kwargs):
        """
        Initialize B2 storage with proper configuration.
        """
        # Clear any cached connection to ensure we use our clean credentials
        if hasattr(self, '_connection'):
            delattr(self, '_connection')
        super().__init__(*args, **kwargs)
        # Clear connection again after parent init to ensure our override is used
        if hasattr(self, '_connection'):
            delattr(self, '_connection')
    
    @property
    def connection(self):
        """
        Override connection property to ensure clean credentials are used.
        This is critical because boto3 is very sensitive to credential format.
        """
        if not hasattr(self, '_connection') or self._connection is None:
            # Get credentials from settings and clean them aggressively
            raw_access_key = getattr(settings, 'AWS_ACCESS_KEY_ID', '')
            raw_secret_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', '')
            
            # Clean credentials - but don't remove spaces from secret key (it might be valid)
            # Only remove newlines, tabs, and quotes
            access_key = clean_credential_for_boto3(raw_access_key)
            # For secret key, be more careful - only remove newlines, tabs, and quotes, but keep spaces
            secret_key = str(raw_secret_key) if raw_secret_key else ''
            secret_key = secret_key.strip().strip('"').strip("'")
            secret_key = secret_key.replace('\n', '').replace('\r', '').replace('\t', '')
            secret_key = ''.join(c for c in secret_key if c.isprintable())
            
            endpoint_url = getattr(settings, 'AWS_S3_ENDPOINT_URL', '')
            bucket_name = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', '')
            
            # Validate credentials
            if not access_key or not secret_key:
                raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set")
            
            # Log credential info (partial for security) - show raw vs cleaned
            logger.info(f"B2 Storage connecting with Key ID: {access_key[:10]}...{access_key[-4:] if len(access_key) > 14 else ''}")
            logger.debug(f"Raw Key ID length: {len(raw_access_key)}, Cleaned length: {len(access_key)}")
            logger.debug(f"Raw Secret length: {len(raw_secret_key)}, Cleaned length: {len(secret_key)}")
            
            # Check for common issues
            if len(access_key) != 24:
                logger.warning(f"B2 Key ID length is {len(access_key)}, expected 24. This might cause issues.")
            if len(secret_key) < 30:
                logger.warning(f"B2 Secret Key length is {len(secret_key)}, seems short. Expected ~40 characters.")
            
            # Create boto3 session with explicit credentials
            session = boto3.Session(
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
            )
            
            # Create S3 client with B2 endpoint
            config = Config(
                signature_version='s3v4',
                s3={
                    'addressing_style': 'path'
                }
            )
            
            self._connection = session.resource(
                's3',
                endpoint_url=endpoint_url,
                config=config
            )
            
        return self._connection
    
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
        Override save to ensure B2-compatible upload with clean credentials.
        Uses our own boto3 client directly to bypass any credential issues.
        """
        # Ensure content is at the beginning
        if hasattr(content, 'seek'):
            content.seek(0)
        
        # Get clean credentials directly
        raw_access_key = getattr(settings, 'AWS_ACCESS_KEY_ID', '')
        raw_secret_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', '')
        endpoint_url = getattr(settings, 'AWS_S3_ENDPOINT_URL', '')
        bucket_name = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', '')
        
        # Clean credentials aggressively
        access_key = clean_credential_for_boto3(raw_access_key)
        secret_key = str(raw_secret_key) if raw_secret_key else ''
        secret_key = secret_key.strip().strip('"').strip("'")
        secret_key = secret_key.replace('\n', '').replace('\r', '').replace('\t', '')
        secret_key = ''.join(c for c in secret_key if c.isprintable()).strip()
        
        # Validate credentials BEFORE attempting upload
        if not access_key or not secret_key:
            raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set")
        
        # Validate credential format - B2 Key IDs are 24-25 chars and start with numbers
        if access_key.startswith('K'):
            error_msg = (
                f"❌ CRITICAL ERROR: Your B2_ACCESS_KEY appears to be a Secret Key!\n"
                f"   Current value: {access_key[:10]}...{access_key[-4:]} (length: {len(access_key)})\n"
                f"   B2 Key IDs should be 24-25 characters and start with NUMBERS (e.g., 0046d1240f581bd0000000006)\n"
                f"   B2 Secret Keys are ~40 characters and start with 'K'\n"
                f"   Please check your .env file and ensure:\n"
                f"   - B2_ACCESS_KEY=0046d1240f581bd0000000006 (24-25 chars, starts with numbers)\n"
                f"   - B2_SECRET_KEY=K004XwT3RzjZB5pGNWHe1uEqtGETCLU (~40 chars, starts with K)"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        if len(access_key) < 24 or len(access_key) > 25:
            error_msg = (
                f"❌ CRITICAL ERROR: B2_ACCESS_KEY has wrong length!\n"
                f"   Current length: {len(access_key)} (expected: 24-25)\n"
                f"   Current value: {access_key[:10]}...{access_key[-4:]}\n"
                f"   Please check your .env file - B2_ACCESS_KEY should be 24-25 characters"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        if len(secret_key) < 25:
            error_msg = (
                f"❌ CRITICAL ERROR: B2_SECRET_KEY has wrong length!\n"
                f"   Current length: {len(secret_key)} (expected: 25-50)\n"
                f"   Current value: {secret_key[:10]}...{secret_key[-4:]}\n"
                f"   Please check your .env file - B2_SECRET_KEY should be 25-50 characters and start with 'K'"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Log for debugging
        logger.debug(f"B2 _save: Using Key ID length {len(access_key)}, Secret length {len(secret_key)}")
        
        # Prepare the file name
        normalized_name = self._normalize_name(name)
        normalized_name = normalized_name.replace('\\', '/')
        
        # Get content type
        content_type = getattr(content, 'content_type', None)
        if not content_type:
            if normalized_name.lower().endswith('.pdf'):
                content_type = 'application/pdf'
            else:
                content_type = 'application/octet-stream'
        
        # Read content
        if hasattr(content, 'read'):
            file_content = content.read()
        else:
            file_content = content
        
        # Create boto3 client directly with clean credentials
        try:
            # Create boto3 session - don't set region_name here to avoid AWS region conflicts
            session = boto3.Session(
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
            )
            
            config = Config(
                signature_version='s3v4',
                s3={
                    'addressing_style': 'path'
                }
            )
            
            # Create client with B2 endpoint - explicitly set region_name to None
            # This prevents boto3 from trying to use AWS regions
            client = session.client(
                's3',
                endpoint_url=endpoint_url,
                config=config,
                region_name=None  # B2 doesn't use AWS regions, use endpoint URL instead
            )
            
            # Log what we're about to do - detailed for debugging
            logger.info(f"="*60)
            logger.info(f"B2 Upload Configuration:")
            logger.info(f"  Bucket: {bucket_name}")
            logger.info(f"  Key: {normalized_name}")
            logger.info(f"  Endpoint: {endpoint_url}")
            logger.info(f"  Key ID: {access_key} (length: {len(access_key)})")
            logger.info(f"  Secret Key starts with: {secret_key[:5]}... (length: {len(secret_key)})")
            logger.info(f"  Secret Key ends with: ...{secret_key[-5:]}")
            logger.info(f"="*60)
            # Don't log full secret key for security
            
            # Test credentials by listing buckets first (this will fail fast if credentials are wrong)
            try:
                logger.info("Testing credentials by listing buckets...")
                response = client.list_buckets()
                logger.info(f"✅ Credentials verified - can list buckets")
                logger.debug(f"Found {len(response.get('Buckets', []))} buckets")
                # Log bucket names to verify we can see the target bucket
                bucket_names = [b['Name'] for b in response.get('Buckets', [])]
                logger.info(f"Available buckets: {bucket_names}")
                if bucket_name not in bucket_names:
                    logger.warning(f"⚠️  Target bucket '{bucket_name}' not found in list. Available: {bucket_names}")
            except ClientError as test_error:
                error_code = test_error.response.get('Error', {}).get('Code', '')
                error_msg = str(test_error)
                logger.error(f"❌ Credential test failed with {error_code}: {test_error}")
                
                if 'InvalidAccessKeyId' in error_msg or error_code == 'InvalidAccessKeyId':
                    # Try to get more details
                    logger.error(f"Full error response: {test_error.response}")
                    raise ValueError(
                        f"❌ Invalid Access Key ID Error\n\n"
                        f"The Key ID '{access_key}' is being rejected by Backblaze B2.\n\n"
                        f"Possible causes:\n"
                        f"1. Key ID and Secret Key don't match (from different Application Keys)\n"
                        f"2. Application Key was deleted or deactivated\n"
                        f"3. Endpoint URL doesn't match bucket region\n"
                        f"4. There's a delay after creating the Application Key (try waiting 1-2 minutes)\n\n"
                        f"Current configuration:\n"
                        f"  Key ID: {access_key}\n"
                        f"  Secret Key: {secret_key[:10]}...{secret_key[-4:]} (length: {len(secret_key)})\n"
                        f"  Bucket: {bucket_name}\n"
                        f"  Endpoint: {endpoint_url}\n\n"
                        f"Troubleshooting steps:\n"
                        f"1. In Backblaze B2, verify the Application Key with ID '{access_key}' still exists\n"
                        f"2. Check that the Secret Key matches exactly (copy it again from Backblaze)\n"
                        f"3. Verify the bucket '{bucket_name}' exists and is in the same region as the endpoint\n"
                        f"4. Try creating a NEW Application Key and updating your .env file\n"
                        f"5. Wait 1-2 minutes if you just created the Application Key"
                    )
                # If it's a different error (like permission), that's okay, continue with upload
                logger.warning(f"Credential test returned: {test_error} (may be permission issue, continuing)")
            
            # Upload directly
            client.put_object(
                Bucket=bucket_name,
                Key=normalized_name,
                Body=file_content,
                ContentType=content_type,
            )
            
            logger.info(f"Successfully uploaded {normalized_name} to B2")
            return normalized_name
            
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            error_message = str(e)
            
            # Handle InvalidAccessKeyId - means Key ID doesn't match Secret Key or doesn't exist
            if 'InvalidAccessKeyId' in str(e) or error_code == 'InvalidAccessKeyId':
                error_msg = (
                    f"❌ CRITICAL ERROR: Invalid Access Key ID!\n"
                    f"   The Key ID '{access_key}' is not valid or doesn't match the Secret Key.\n"
                    f"   This usually means:\n"
                    f"   1. The Key ID and Secret Key don't match (from different Application Keys)\n"
                    f"   2. The Application Key was deleted or doesn't exist\n"
                    f"   3. The Application Key doesn't have permissions for bucket '{bucket_name}'\n\n"
                    f"   Current credentials being used:\n"
                    f"   - Key ID: {access_key[:10]}...{access_key[-4:]} (length: {len(access_key)})\n"
                    f"   - Secret Key: {secret_key[:10]}...{secret_key[-4:]} (length: {len(secret_key)})\n"
                    f"   - Bucket: {bucket_name}\n"
                    f"   - Endpoint: {endpoint_url}\n\n"
                    f"   📋 HOW TO FIX:\n"
                    f"   1. Go to Backblaze B2 dashboard → App Keys\n"
                    f"   2. Find the Application Key with Key ID: {access_key}\n"
                    f"   3. Verify the Secret Key matches: {secret_key[:10]}...{secret_key[-4:]}\n"
                    f"   4. Check that the Application Key has these capabilities:\n"
                    f"      - listBuckets\n"
                    f"      - readFiles\n"
                    f"      - writeFiles\n"
                    f"      - deleteFiles (optional)\n"
                    f"   5. Verify the Application Key is allowed for bucket: {bucket_name}\n"
                    f"   6. If the Key ID and Secret Key don't match, create a new Application Key\n"
                    f"      and update your .env file with BOTH the new Key ID and Secret Key"
                )
                logger.error(error_msg)
                raise ValueError(error_msg)
            
            # Handle malformed credential errors with more detail
            if 'InvalidRequest' in str(e) or 'malformed' in str(e).lower():
                logger.error(f"B2 credential error: {e}")
                logger.error(f"Access Key (first 10, last 4): {access_key[:10]}...{access_key[-4:] if len(access_key) > 14 else ''}")
                logger.error(f"Access Key length: {len(access_key)} (expected 24-25)")
                logger.error(f"Secret Key length: {len(secret_key)} (expected 25-50)")
                logger.error(f"Raw Access Key length: {len(raw_access_key)}")
                logger.error(f"Raw Secret Key length: {len(raw_secret_key)}")
                logger.error("Check your .env file - ensure no quotes, newlines, or extra spaces")
                raise ValueError(f"B2 credentials are malformed. Access Key length: {len(access_key)}, Secret length: {len(secret_key)}. Error: {e}")
            
            # Re-raise other errors
            logger.error(f"B2 upload error: {error_code} - {e}")
            raise
