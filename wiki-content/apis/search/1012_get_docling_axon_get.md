# Get Docling Axon API

## Overview
The Get Docling Axon API is designed to retrieve document data from the `docling_test` database table based on a specified unique identifier (Uid). This API is part of the Search API group and allows users to filter and retrieve relevant document information efficiently.

## Details
- **HTTP Method**: GET
- **URL**: `/api/search/get_docling_axon`
- **Request Shape**:
  - **Input**:
    - `Uid` (optional): A unique identifier for the document.
- **Response Shape**:
  - Returns a list of documents that match the given Uid, containing:
    - `id`: The identifier of the document.
    - `docling_data`: The associated data for the document.
- **Authentication**: [TODO] (Specify if authentication is required)

## How it works
1. The API receives a GET request with an optional `Uid` parameter.
2. It queries the `docling_test` table in the database where the `uuid` matches the provided `Uid`.
3. The query returns a list of documents, specifically the `id` and `docling_data` fields.
4. The response is structured to return the results of the database query.

## Notes
- The `Uid` parameter is optional; if not provided, the API may return all documents or an empty list based on the implementation.
- The `filters=trim` indicates that any whitespace around the Uid will be removed before processing.
- Ensure that the database connection is properly configured to access the `docling_test` table.
- [TODO] - Additional dependencies or environment variables that may be required for this API.