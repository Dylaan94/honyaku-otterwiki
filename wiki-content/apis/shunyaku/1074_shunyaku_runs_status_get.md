# Shunyaku Runs Status API

## Overview
The Shunyaku Runs Status API provides a way to retrieve the status of specific runs associated with a user. It allows users to query their run statuses using a list of identifiers, returning relevant details about each run.

## Details
- **HTTP Method:** GET
- **URL:** `/shunyaku_runs/status`
- **Authentication:** Required (user-based authentication)
- **Request Shape:**
  - Input: JSON object containing an array of `ids`
    ```json
    {
      "ids": ["id1", "id2", ...]
    }
    ```
- **Response Shape:**
  - Returns a list of runs with the following fields:
    - `id`
    - `user_id`
    - `organization_id`
    - `file_s3_key`
    - `shunyaku_n8n_s3_key`
    - `reconstructed_s3_key`
    - `Source_lang`
    - `Target_lang`
    - `segments`
    - `termbase_usage`
    - `tm_matches`
    - `processing_stats`
    - `delete`

## How it works
1. The API receives a GET request with a JSON payload containing an array of `ids`.
2. It authenticates the user making the request.
3. A database query is executed against the `docling_test` table:
   - It filters records where the `id` is in the provided `ids` and the `user_id` matches the authenticated user's ID.
4. The query returns a list of runs with specified fields.
5. The response is sent back to the user containing the queried run details.

## Notes
- Ensure that the user is authenticated before making a request to this endpoint.
- The API is designed to return only the runs that belong to the authenticated user.
- [TODO] Additional error handling and edge cases are not specified in the code.