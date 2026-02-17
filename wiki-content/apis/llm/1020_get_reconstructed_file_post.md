# Get Reconstructed File API

## Overview
The `get_reconstructed_file` API endpoint allows users to retrieve a reconstructed file after translation based on a given record UUID. This functionality is essential for accessing processed files stored in an S3 bucket, enabling further actions or downloads.

## Details
- **HTTP Method**: POST
- **URL**: `/api/llm/get_reconstructed_file`
- **Request Shape**:
  - **Input**:
    - `record_uuid`: A unique identifier for the record (string).
- **Response Shape**:
  - `reconstructed_file_url`: URL to the reconstructed file.
  - `shunyaku_json`: JSON data associated with the shunyaku process.
  - `shunyaku_json_url`: URL to the shunyaku JSON file.
- **Authentication**: Requires AWS S3 credentials stored in environment variables.

## How it works
1. The API receives a `record_uuid` as input.
2. It initializes a timeout mechanism allowing up to 700 seconds for the process.
3. A loop checks the database for a record matching the provided UUID:
   - If the `reconstructed_s3_key` is found, it breaks the loop.
   - If not found, it waits for 2 seconds before checking again.
4. Once the record is found, it retrieves the S3 keys for both the reconstructed file and the shunyaku process.
5. It generates signed URLs for both files using AWS S3 credentials.
6. Finally, it constructs and returns a response containing the URLs and associated JSON data.

## Notes
- The API will keep checking for the reconstructed file for a maximum of 700 seconds.
- The sleep interval between checks is set to 2 seconds.
- Ensure that the following environment variables are set for AWS S3 access:
  - `s3_access_key`
  - `s3_secret_access_key`
- The S3 bucket used is `honyaku-os` located in the `ap-northeast-1` region.
- [TODO] Additional error handling and edge cases should be considered, such as what happens if the UUID does not exist or if the S3 URL generation fails.