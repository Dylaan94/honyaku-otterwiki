# Check Termbase API

## Overview
The Check Termbase API is designed to query a termbase database to retrieve specific translation data based on the provided organization and search terms. This API is useful for applications that need to verify or fetch translation entries from a centralized termbase.

## Details
- **HTTP Method**: POST
- **URL**: `/api/llm/check_tb`
- **Request Shape**:
  - **Input Parameters**:
    - `organization` (optional, string): The organization to filter the termbase entries.
    - `search` (optional, string): The search term to look for in the termbase.
- **Response Shape**:
  - Returns a single translation entry:
    - `en` (string or null): The English translation.
    - `en_us` (string or null): The American English translation.
- **Authentication**: [TODO] (details about authentication are not provided in the code)

## How it works
1. The API receives a POST request with optional `organization` and `search` parameters.
2. It queries the database to find entries in the termbase where:
   - The client matches the provided organization.
   - The Japanese term (`ja`) matches the search term.
3. The query returns distinct results, specifically the English (`en`) and American English (`en_us`) translations.
4. If no results are found, the response will indicate that the translation is `null`.
5. If results are found, it checks if the `en` translation is available:
   - If `en` is not available, it uses the `en_us` translation.
   - If `en` is available, it uses that value for the response.
6. The final response is sent back to the requester.

## Notes
- The API is part of the "LLM" API group.
- The database query uses specific filters to ensure that only relevant entries are retrieved.
- The implementation includes a debug stop to inspect the results during development.
- Ensure that the database connection and schema are properly configured to support the query structure.
- [TODO] - Additional dependencies or environment variables required for this API are not specified in the code.