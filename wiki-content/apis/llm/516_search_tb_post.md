# Search Termbase API

## Overview
The Search Termbase API allows users to search for terms in a database based on specified criteria, such as organization and search text. This API is designed to facilitate the retrieval of multilingual term data, enhancing the efficiency of language processing tasks.

## Details
- **HTTP Method**: POST
- **URL**: `/api/llm/search_tb`
- **Request Shape**:
  - **Input Parameters**:
    - `text` (optional): The text to search for.
    - `organization` (optional): The organization to filter results.
    - `search` (optional): The search term to look for.
- **Response Shape**: Returns a list of results containing English, Japanese, and US English translations.
- **Authentication**: [TODO]

## How it works
1. The API receives a POST request with optional input parameters: `text`, `organization`, and `search`.
2. It queries the database to find entries in the termbase that match the organization and search criteria:
   - It checks if the organization is included in the termbase and if the search term is found in either Japanese or English fields.
   - It also checks the translation memory for matches.
3. The results are returned as a list containing the fields: `en`, `ja`, and `en_us`.
4. If no results are found, the response will indicate that the English field is null.
5. If results are found, the API checks for the presence of the English translation and returns it; if not, it defaults to the US English translation.

## Notes
- The API uses a conditional structure to handle the presence or absence of results effectively.
- The `debug.stop` statement is included for debugging purposes to halt execution and inspect the `$results`.
- Ensure that the database connection and schema are properly configured to support the queries made by this API.
- [TODO] - Additional dependencies or environment variables required for this API are not specified.