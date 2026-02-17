# Get Potential Terms for Shunyaku Run

## Overview
This API endpoint retrieves potential terms associated with a specific shunyaku run, formatted for use in a WeWeb component. It ensures that the user has the necessary permissions to access the data and returns a structured list of terms based on the provided shunyaku ID.

## Details
- **HTTP Method**: GET
- **URL**: `/apis/shunyaku/potential_terms`
- **Authentication**: Requires user authentication.
- **Input**:
  - `shunyaku_id` (int): The ID of the shunyaku run for which potential terms are requested.
- **Response**: A list of potential terms, each containing:
  - `term`: The source term.
  - `en_suggestion`: The target suggestion.
  - `en_suggestion_type`: Type of suggestion (e.g., "ai_suggested").
  - `term_type`: The type of term.
  - `count`: The source count of the term.
  - `segment_uuid`: The UUID of the segment.
  - `reason_tag`: The reason tag associated with the term.

## How it works
1. **User Verification**:
   - The API first checks if the user has access to the specified shunyaku run by querying the database with the provided `shunyaku_id`.
   - If the shunyaku run is not found, it returns a "notfound" error.
   - If the user does not match the owner of the shunyaku run, it returns an "Access denied" error.

2. **Fetching Potential Terms**:
   - If access is granted, the API queries the database for potential terms linked to the `shunyaku_id`.

3. **Flattening Results**:
   - The results are processed to ensure that each term is represented in a flattened structure, where each segment UUID is associated with its respective term.
   - Terms without segment UUIDs are skipped.

4. **Response Construction**:
   - The final structured list of terms is prepared and returned as the response.

## Notes
- The API relies on the existence of a database with the relevant collections (`docling_test` and `potential_terms`).
- Ensure that the user is authenticated before making a request to this endpoint.
- [TODO]: Additional error handling or edge cases may need to be documented based on further requirements or testing.