# Check Translation Memory API

## Overview
The Check Translation Memory API is designed to query a translation memory database to retrieve English translations based on a given search term and optional organization filter. This API helps in determining if a translation exists for a specific input, enhancing the efficiency of translation processes.

## Details
- **HTTP Method**: POST
- **URL**: `/api/llm/check_tm`
- **Request Shape**:
  - **Input Parameters**:
    - `text` (optional): The organization name to filter results.
    - `text` (optional): The search term for which translations are sought.
- **Response Shape**:
  - Returns the English translation or `null` if no translation is found.
- **Authentication**: [TODO]

## How it works
1. The API receives a POST request with optional parameters for `organization` and `search`.
2. It queries the `translation_memory` database to find entries that match the provided organization and search term.
3. If results are found:
   - It checks if the primary English translation (`en`) exists; if not, it falls back to the U.S. English translation (`en_us`).
   - Sets a flag indicating that results exist and prepares an empty list for terms (though this list is not populated).
4. If no results are found, it sets the existence flag to false.
5. The response returns the determined English translation or `null`.

## Notes
- The API currently does not handle authentication; this should be implemented as needed.
- The `terms` variable is initialized but not populated, indicating potential future use or a missing implementation.
- The API uses a debug stop mechanism to output intermediate values, which may be useful for development but should be removed or disabled in production.
- Ensure that the database schema matches the expected fields for the query to function correctly.