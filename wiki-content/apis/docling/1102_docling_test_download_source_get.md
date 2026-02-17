# Docling Test Download Source API

## Overview
The Docling Test Download Source API provides a mechanism to retrieve a specific file associated with a Docling test from an AWS S3 bucket. This endpoint allows users to download files by specifying the test ID, facilitating easy access to test resources.

## Details
- **HTTP Method**: GET
- **URL**: `/docling_test/download_source`
- **Request Shape**:
  - **Input**: 
    - `id` (integer): The unique identifier for the Docling test.
- **Response Shape**: The response contains the file data retrieved from S3.
- **Authentication**: Uses AWS credentials stored in environment variables.

## How it works
1. The API receives a GET request with a test ID.
2. It retrieves the corresponding Docling test record from the database using the provided ID.
3. The API then accesses the specified file in an S3 bucket using the file key stored in the retrieved test record.
4. It sets the appropriate headers for the response:
   - `Content-Disposition`: Specifies the filename for the download.
   - `Content-Type`: Sets the MIME type of the file.
5. Finally, it returns the file data as the response.

## Notes
- The S3 bucket used is `honyaku-os`, located in the `ap-northeast-1` region.
- The API requires the following environment variables for AWS access:
  - `s3_access_key`
  - `s3_secret_access_key`
- The filename in the `Content-Disposition` header is URL-encoded to ensure proper handling of special characters.
- Debugging information can be accessed through the `!debug.stop` statement, which outputs the retrieved Docling test record.
- [TODO] Additional error handling and edge cases should be documented.