# LLM User Runs Query API

## Overview
This API endpoint retrieves all records of LLM User Runs associated with a specific user. It allows users to access their own runs or, if they have admin privileges, the runs of all users. This functionality is essential for monitoring and managing user interactions with the LLM system.

## Details
- **HTTP Method**: GET
- **URL**: `/apis/llm/714_llm_user_runs`
- **Authentication**: Requires user authentication; only authenticated users can access their own runs, while admins can access all runs.
- **Request Shape**: No input parameters are required for the request.
- **Response Shape**: Returns a list of LLM User Runs records, including associated organization details.

### Response Structure
The response includes:
- A list of LLM User Runs, filtered by user ID or admin role.
- Organization details for each run, including:
  - `id`
  - `name`
  - `name_ja`
  - `logo` (with properties: `access`, `path`, `name`, `type`, `size`, `mime`, `meta`, `url`)

## How it works
1. The API is triggered by a GET request.
2. It authenticates the user to retrieve their ID.
3. It queries the database for LLM User Runs:
   - Filters results based on the user's ID or checks if the user has an admin role.
   - Ensures that only non-deleted records are returned.
4. For each LLM User Run, it fetches associated organization details.
5. The final response is constructed and sent back to the user.

## Notes
- The query checks if the user is an admin to allow broader access to records.
- The `delete` flag ensures that only active records are returned.
- [TODO] Additional error handling or edge cases are not specified in the provided code.