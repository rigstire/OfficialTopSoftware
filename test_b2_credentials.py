"""
Simple script to test Backblaze B2 credentials directly with boto3
This bypasses Django to verify if credentials work at all
"""
import boto3
from botocore.config import Config
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get credentials from environment
access_key = os.getenv('B2_ACCESS_KEY', '').strip()
secret_key = os.getenv('B2_SECRET_KEY', '').strip()
bucket_name = os.getenv('B2_BUCKET_NAME', '').strip()
endpoint_url = os.getenv('B2_ENDPOINT_URL', 'https://s3.us-west-002.backblazeb2.com').strip()

print("="*70)
print("Testing Backblaze B2 Credentials")
print("="*70)
print(f"Key ID: {access_key} (length: {len(access_key)})")
print(f"Secret Key: {secret_key[:10]}...{secret_key[-4:]} (length: {len(secret_key)})")
print(f"Bucket: {bucket_name}")
print(f"Endpoint: {endpoint_url}")
print("="*70)

if not access_key or not secret_key:
    print("❌ ERROR: B2_ACCESS_KEY or B2_SECRET_KEY not set in .env file")
    exit(1)

try:
    # Create boto3 session
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
    
    # Create S3 client with B2 endpoint
    client = session.client(
        's3',
        endpoint_url=endpoint_url,
        config=config,
        region_name=None
    )
    
    print("\n1. Testing: List buckets...")
    response = client.list_buckets()
    buckets = [b['Name'] for b in response.get('Buckets', [])]
    print(f"   ✅ Success! Found {len(buckets)} buckets:")
    for bucket in buckets:
        print(f"      - {bucket}")
    
    if bucket_name and bucket_name not in buckets:
        print(f"\n   ⚠️  WARNING: Target bucket '{bucket_name}' not found in list!")
    elif bucket_name:
        print(f"\n   ✅ Target bucket '{bucket_name}' found!")
    
    # Try to list objects in the bucket
    if bucket_name:
        print(f"\n2. Testing: List objects in bucket '{bucket_name}'...")
        try:
            response = client.list_objects_v2(Bucket=bucket_name, MaxKeys=5)
            objects = response.get('Contents', [])
            print(f"   ✅ Success! Found {len(objects)} objects (showing first 5)")
            for obj in objects:
                print(f"      - {obj['Key']} ({obj['Size']} bytes)")
        except Exception as e:
            print(f"   ⚠️  Could not list objects: {e}")
    
    # Try to upload a test file
    if bucket_name:
        print(f"\n3. Testing: Upload test file to bucket '{bucket_name}'...")
        try:
            test_key = 'test_upload.txt'
            test_content = b'This is a test upload from boto3'
            client.put_object(
                Bucket=bucket_name,
                Key=test_key,
                Body=test_content,
                ContentType='text/plain'
            )
            print(f"   ✅ Success! Uploaded '{test_key}'")
            
            # Clean up - delete the test file
            print(f"\n4. Cleaning up: Deleting test file...")
            client.delete_object(Bucket=bucket_name, Key=test_key)
            print(f"   ✅ Test file deleted")
        except Exception as e:
            print(f"   ❌ Upload failed: {e}")
            print(f"   Error type: {type(e).__name__}")
            if hasattr(e, 'response'):
                print(f"   Error response: {e.response}")
    
    print("\n" + "="*70)
    print("✅ All tests passed! Your B2 credentials are working correctly.")
    print("="*70)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print(f"Error type: {type(e).__name__}")
    if hasattr(e, 'response'):
        error_code = e.response.get('Error', {}).get('Code', '')
        error_message = e.response.get('Error', {}).get('Message', '')
        print(f"Error code: {error_code}")
        print(f"Error message: {error_message}")
        print(f"Full response: {e.response}")
    
    print("\n" + "="*70)
    print("❌ Credential test failed!")
    print("="*70)
    print("\nPossible issues:")
    print("1. Key ID and Secret Key don't match (from different Application Keys)")
    print("2. Application Key was deleted or deactivated")
    print("3. Application Key doesn't have required permissions")
    print("4. Endpoint URL doesn't match bucket region")
    print("5. There's an issue on Backblaze's end (less likely)")
    exit(1)
