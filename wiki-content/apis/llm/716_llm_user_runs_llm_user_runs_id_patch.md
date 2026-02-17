# Edit LLM User Runs Record

## Overview
This API endpoint allows users to update records in the "LLM User Runs" database. It supports various modifications, including changing the title, updating user feedback, and sharing settings, making it a flexible tool for managing user run data.

## Details
- **HTTP Method**: PATCH
- **URL**: `llm_user_runs/{llm_user_runs_id}`
- **Authentication**: Required (user-based)
- **Request Shape**:
  - **Input Fields**:
    - `llm_user_runs_uuid` (string, required): The UUID of the user run to be edited.
    - `new_title` (string, optional): A new title for the user run.
    - `user_feedback` (enum, optional): User feedback, which can be "thumbs_up" or "thumbs_down".
    - `shared` (boolean, optional): Indicates if the user run should be sharable.
- **Response Shape**: Returns a boolean indicating success.

## How it works
1. The API receives a PATCH request with the specified `llm_user_runs_id`.
2. It retrieves the raw input data in JSON format.
3. The API checks which fields are provided in the input:
   - If `new_title` is present, it updates the title for the corresponding user run.
   - If `user_feedback` is provided, it updates the feedback metrics.
   - If `shared` is set to true, it updates the shareability status.
   - If none of the above fields are provided, it performs a generic patch update using the remaining input data.
4. The changes are applied to the "LLM User Runs" database.

## Notes
- The following fields are hidden and cannot be modified through this API:
  - `meta`, `input`, `job_id`, `status`, `metrics`, `source_lang`, `style_guide`, `target_lang`, `shunyaku_output`, `reference_file_ids`, `termbase_terms_used`, `from_translation_memory`.
- Ensure that the UUID provided in `llm_user_runs_uuid` is valid and exists in the database.
- [TODO] Consideration for error handling and response messages is not specified in the code.