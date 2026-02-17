# axon_add_docling POST API

## Overview
The `axon_add_docling` API endpoint allows users to upload a document (referred to as a "docling") to an S3 bucket and update the corresponding database entry. This functionality is essential for managing document storage and ensuring that metadata related to the documents is correctly maintained in the database.

## Details
- **HTTP Method**: POST
- **URL**: `/api/llm/axon_add_docling`
- **Request Shape**:
  - **Input Parameters**:
    - `id` (optional): The unique identifier for the docling.
    - `docling_s3_key` (optional): The S3 key for the uploaded docling.
    - `extracted_termbase` (optional): A JSON object containing extracted termbase data.
- **Response Shape**: The API returns the updated docling information, including:
  - `id`
  - `created_at`
  - `uuid`
  - `user_id`
  - `organization_id`
  - `file_name`
  - `docling_s3_key`
  - `potential_termbase`
- **Authentication**: [TODO] - Specify authentication requirements if applicable.

## How it works
1. The API receives input parameters including `id`, `docling_s3_key`, and `extracted_termbase`.
2. It queries the database to retrieve the document details associated with the provided `id`.
3. The API uploads the corresponding JSON file to an S3 bucket using AWS credentials stored in environment variables.
4. After the file upload, the API updates the database entry for the docling with the new S3 key and extracted termbase.
5. Finally, it returns the updated docling information as the response.

## Notes
- **Edge Cases**: Ensure that the `id` provided corresponds to an existing entry in the database; otherwise, the upload and update will fail.
- **Dependencies**:
  - AWS S3 for file storage.
  - Database access for querying and updating docling entries.
- **Environment Variables**:
  - `s3_acess_key`: AWS access key for S3.
  - `s3_secret_acess_key`: AWS secret access key for S3.
- **File Naming Convention**: The uploaded file is named using the format `docling_data/{file_name}_docling.json`.
- **[TODO]**: Clarify the authentication method required for accessing this API.