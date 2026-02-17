# Process Docling Test API

## Overview
The `process_docling_test` API endpoint retrieves and processes data related to a specific document test from the database. It formats the data for display in the WeWeb platform, grouping segments, terms, and translation memory matches for easier consumption.

## Details
- **HTTP Method**: GET
- **URL**: `/apis/llm/process_docling_test`
- **Authentication**: Requires user authentication.
- **Request Shape**:
  - Input: 
    - `id` (integer): The identifier for the document test to retrieve.
- **Response Shape**: 
  - Returns an object containing:
    - `docTitle`: Title of the document.
    - `sourceLang`: Source language of the document.
    - `targetLang`: Target language of the document.
    - `segments`: Array of processed segments.
    - `terms`: Array of associated terms.
    - `tm_matches`: Array of translation memory matches.

## How it works
1. **Input Handling**: The API receives an integer `id` as input.
2. **Database Query**: It queries the `docling_test` database for the record matching the provided `id`.
3. **Data Processing**:
   - **Segments**: It processes the segments from the retrieved record, grouping them by their `chunk_index` (adjusted to be 1-based).
   - **Terms**: It filters and collects terms associated with each segment.
   - **Translation Memory Matches**: It filters and collects translation memory matches for each segment, formatting dates appropriately.
4. **Response Construction**: The processed data is structured into a response object that includes the document title, languages, segments, terms, and matches.

## Notes
- The API has a timeout limit of 10 seconds for processing.
- The segments are grouped by `chunk_index`, which is adjusted to be 1-based for user-friendly display.
- There is a typo in the code where "segments" is misspelled as "segements"; this is preserved to match the existing configuration.
- The function `formatDate` ensures dates are formatted to `YYYY-MM-DD`, returning the original value if the date is invalid.
- [TODO]: Additional dependencies or environment variables required for this API are not specified in the code.