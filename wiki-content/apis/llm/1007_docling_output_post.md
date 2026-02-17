# docling_output POST API

## Overview
The `docling_output` API endpoint is designed to process documents by uploading them to an AWS S3 bucket and triggering a translation service. It handles various inputs, including file URLs and user prompts, and returns a record of the operation along with a unique identifier.

## Details
- **HTTP Method**: POST
- **URL**: `/docling_output`
- **Request Shape**:
  - **Input Parameters**:
    - `file_url` (optional): URL of the file to be processed.
    - `file_name` (optional): Name of the file.
    - `client_id` (optional): Identifier for the client.
    - `source_lang` (optional): Source language of the document.
    - `target_lang` (optional): Target language for translation.
    - `user_prompt` (optional): User's prompt for processing.
    - `users_id` (optional): User ID from the `users` table.
    - `organizations_id` (optional): Organization ID from the `organizations` table.
    - `choice` (optional): Choice parameter for processing.
- **Response Shape**:
  - `result1`: Status message (e.g., "200 ok").
  - `file_record`: Record of the uploaded file.
  - `record_uuid`: Unique identifier for the operation.
- **Authentication**: Requires a Bearer token for the external API call.

## How it works
1. **File Upload**: The API first uploads the file specified by `file_url` to an S3 bucket.
2. **UUID Generation**: A unique identifier (UUID) is created for tracking the request.
3. **Organization Query**: Depending on whether `client_id` is provided, it queries the database for organization details.
4. **File Metadata Handling**: The file is uploaded to S3 with the appropriate metadata.
5. **Database Entry**: A new record is created in the `docling_test` table with details about the upload and processing request.
6. **Trigger Processing**: An asynchronous function is triggered to handle further processing of the document.
7. **External API Call**: A request is sent to an external API for processing the document.
8. **Response Handling**: The API checks the response and retrieves additional data if the processing was successful, or throws an error if it failed.

## Notes
- **Edge Cases**: If `client_id` is not provided, the API defaults to querying based on `organizations_id`.
- **Dependencies**: Requires access to AWS S3 and a valid token for the external API.
- **Environment Variables**:
  - `s3_access_key`: AWS S3 access key.
  - `s3_secret_access_key`: AWS S3 secret access key.
  - `RUNPOD_API_TOKEN`: Token for authenticating with the external API.
- **Error Handling**: If the external API call fails, an exception is thrown with the error message.