# Get Shunyaku Runs for Admin/Manager Views

## Overview
This API endpoint retrieves shunyaku runs, allowing for optional filtering based on organization ID, user ID, or search terms. It is primarily designed for administrative and managerial use, enabling users to view all runs or filter them according to specific criteria.

## Details
- **HTTP Method**: GET
- **URL**: `/apis/llm/shunyaku_runs_admin`
- **Authentication**: Required (user authentication)
- **Input Parameters**:
  - `search` (optional, string): Filters results by `file_name` or `user_prompt`.
  - `page` (optional, integer): The page number for pagination.
  - `per_page` (optional, integer): Number of results per page (default is 25).
  - `users_id` (optional, integer): Filters runs for a specific user.
  - `organizations_id` (optional, integer): Filters runs for a specific organization.
- **Response Shape**:
  - Returns a paginated list of shunyaku runs with various fields including IDs, timestamps, user details, and organization details.

## How it works
1. The API receives input parameters for filtering runs.
2. It constructs a database query to fetch runs from the `docling_test` table:
   - Filters out deleted runs.
   - Applies filters based on `organizations_id`, `users_id`, and `search` criteria.
3. The results are sorted in descending order by `id`.
4. The response includes pagination details and a list of relevant fields.
5. Additional data about organizations and users is fetched and included in the response.

## Notes
- The default pagination settings return the first page with 25 results if no specific values are provided.
- The API is designed to handle cases where no filters are applied, returning all runs.
- The `search` parameter can be empty or null, in which case it will not filter by `file_name` or `user_prompt`.
- [TODO]: Confirm the exact URL path for the API endpoint.