# Download File API

## Overview
The Download File API allows users to retrieve files from a database based on a specified record ID and file type. It supports two types of files: source and target. This API is essential for applications that need to access and download files stored in a cloud storage solution.

## Details
- **HTTP Method**: GET
- **URL**: `/download_file`
- **Authentication**: Required (user authentication)
- **Input Parameters**:
  - `record_id` (int): The ID of the record to retrieve.
  - `type` (text): The type of file to download, either 'source' or 'target'.
- **Response Shape**:
  - On success:
    - For source type:
      ```json
      {
        "error": false,
        "type": "source",
        "s3_key": "<s3_key>",
        "filename": "<file_name>",
        "file": null
      }
      ```
    - For target type:
      ```json
      {
        "error": false,
        "type": "target",
        "s3_key": null,
        "filename": "<translated_filename>",
        "file": "<translated_file>"
      }
      ```
  - On error:
    - Record not found:
      ```json
      {
        "error": true,
        "message": "Record not found",
        "status": 404
      }
      ```
    - Invalid type:
      ```json
      {
        "error": true,
        "message": "Invalid type. Must be 'source' or 'target'",
        "status": 400
      }
      ```

## How it works
1. **Get the Record**: The API queries the database to fetch the record using the provided `record_id`. It retrieves the fields: `id`, `file_name`, `file_s3_key`, and `translated_file`.
2. **Generate Translated Filename**: A lambda function generates a translated filename based on the original file name. If no extension is found, it appends '_translated' to the name; otherwise, it retains the extension.
3. **Build Response**: Another lambda function constructs the response based on the `type` parameter:
   - If the record is not found, it returns a 404 error.
   - If the type is 'source', it returns the S3 key and original filename.
   - If the type is 'target', it returns the translated filename and the translated file.
   - If the type is invalid, it returns a 400 error.

## Notes
- Ensure the user is authenticated to access this API.
- The API currently supports only 'source' and 'target' types; any other input will result in an error.
- The maximum timeout for the lambda functions is set to 5 seconds.
- [TODO] Additional dependencies or environment variables required for database access or file storage are not specified in the code.