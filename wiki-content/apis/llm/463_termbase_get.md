# Termbase API - GET Endpoint

## Overview
The Termbase API provides a way to retrieve a list of terms from a specified organization. This endpoint allows users to paginate through the results, making it easier to manage large datasets.

## Details
- **HTTP Method**: GET
- **URL**: `/api/llm/termbase`
- **Request Parameters**:
  - `page` (int, optional): The page number to retrieve.
  - `per_page` (int, optional): The number of results per page.
  - `offset` (int, optional): The number of results to skip before starting to collect the result set.
  - `organization` (text, optional): The organization to filter results by.
- **Response Shape**: Returns a list of terms that match the specified organization, along with pagination information.
- **Authentication**: Required.

## How it works
1. The API receives a GET request with optional parameters for pagination and organization filtering.
2. It queries the database for terms associated with the specified organization.
3. The query includes pagination details (page number, results per page, and offset).
4. The results are returned as a list, ensuring that the terms are distinct.
5. The response is cached for 24 hours (86400 seconds) to improve performance.

## Notes
- The query filters results based on the `organization` parameter, which must match the client's organization.
- Caching settings include:
  - `ttl`: 86400 seconds (1 day)
  - `input`: true (cache based on input parameters)
  - `auth`: true (cache is authenticated)
  - `datasource`: true (cache is datasource-specific)
  - `ip`: false (does not cache based on IP)
- Ensure that the database connection and the `termbase` table are properly configured.
- [TODO] Confirm any additional dependencies or environment variables required for this API.