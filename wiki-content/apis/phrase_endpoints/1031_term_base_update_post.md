# Phrase Term Base Update API

## Overview
The Phrase Term Base Update API handles webhooks from Phrase to create or update term and concept records in the database based on specific event types. This API is essential for maintaining the integrity and accuracy of terms and concepts used in translation and localization processes.

## Details
- **HTTP Method**: POST
- **Endpoint**: `/term_base_update`
- **Request Shape**:
  - **Input**: A JSON payload containing webhook data from Phrase.
  - **Example Payload**:
    ```json
    {
      "event": "TERM_BASE_TERM_UPDATED",
      "term": {
        "conceptId": "12345",
        "lang": "en",
        "data": "Updated term data"
      }
    }
    ```
- **Response Shape**: 
  - Success: 
    ```json
    {
      "success": true,
      "action": "term_updated",
      "concept_id": "12345",
      "language": "en",
      "record_id": "67890"
    }
    ```
  - Failure:
    ```json
    {
      "success": false,
      "action": "not_found",
      "concept_id": "12345",
      "message": "No record found with conceptId: 12345"
    }
    ```
- **Authentication**: [TODO]

## How it works
1. **Input Handling**: The API receives a JSON payload from Phrase containing the event type and relevant term or concept data.
2. **Event Validation**: It checks if the event type is one of the valid types:
   - `TERM_BASE_TERM_UPDATED`
   - `TERM_BASE_TERM_CREATED`
   - `TERM_BASE_TERM_DELETED`
   - `TERM_BASE_CONCEPT_UPDATED`
   - `TERM_BASE_CONCEPT_DELETED`
3. **Processing Events**:
   - For `TERM_BASE_TERM_UPDATED`: It updates an existing term record based on the `conceptId`.
   - For `TERM_BASE_TERM_CREATED`: It creates a new term record if it does not exist.
   - For `TERM_BASE_CONCEPT_UPDATED`: It updates the concept fields in the database.
   - For `TERM_BASE_TERM_DELETED`: It deletes the term from the relevant language fields in the database.

## Notes
- **Error Handling**: The API includes preconditions to validate required fields such as `conceptId` and `lang`. If these are missing, it returns an error message.
- **Database Operations**: The API interacts with the "Dylan TB Update Test Table" for querying, updating, and adding records.
- **Language Handling**: When deleting a term, the API checks across multiple language fields to identify which language's term needs to be cleared.
- **Dependencies**: The API relies on the `phrase/update_term_by_language` function to handle term updates and creations.
- **Environment Variables**: [TODO]