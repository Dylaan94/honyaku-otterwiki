# Get Shunyaku Runs by User ID

## Overview
This API endpoint retrieves all shunyaku runs associated with a specific user ID from the `docling_test` table. It allows users to filter results based on a search term, providing a way to access relevant data efficiently.

## Details
- **HTTP Method**: GET
- **URL**: `/apis/llm/shunyaku_runs_by_user_id`
- **Authentication**: Requires user authentication.
- **Request Parameters**:
  - `text? search?`: An optional search term to filter results.
- **Response Shape**: Returns a list of shunyaku runs with the following fields:
  - `id`
  - `created_at`
  - `uuid`
  - `user_id`
  - `project_id`
  - `Client`
  - `user_prompt`
  - `organization_id`
  - `file_name`
  - `shunyaku_n8n_s3_key`
  - `Source_lang`
  - `Target_lang`
  - `segments`
  - `termbase_usage`
  - `tm_matches`
  - `processing_stats`

## How it works
1. The API receives a GET request with an optional search parameter.
2. It authenticates the user to ensure they have access to the data.
3. A database query is executed against the `docling_test` table:
   - Filters results where the `user_id` matches the authenticated user's ID.
   - Checks if the `file_name` or `user_prompt` includes the search term (if provided).
   - Ensures that the record is not marked as deleted (`delete == false`).
4. The results are sorted by the creation date in descending order.
5. The relevant fields are selected and returned in the response.

## Notes
- Ensure that the user is authenticated before making a request to this endpoint.
- The search functionality is case-insensitive and looks for partial matches in `file_name` and `user_prompt`.
- [TODO] Consider any additional error handling or edge cases that may arise from database queries or user inputs.