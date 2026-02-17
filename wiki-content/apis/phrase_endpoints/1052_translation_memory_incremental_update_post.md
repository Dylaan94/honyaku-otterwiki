# Translation Memory Incremental Update

## Overview
This endpoint handles webhooks from Phrase for job updates (specifically `JOB_UPDATED` and `JOB_TARGET_UPDATED` events) to incrementally update a translation memory table. It fetches segments from the Phrase API and upserts them into the translation memory table `translation_memory_dylan_test`.

## Details
- **HTTP Method**: POST
- **URL**: [Not explicitly defined; it is a webhook handler]
- **Request Shape**: Expects a JSON payload from Phrase containing event metadata and job details.
- **Response Shape**: Returns a JSON object indicating success, event type, project UID, total segments upserted, and details for each job processed.
- **Authentication**: Uses API token authentication to access the Phrase API.

## How it works
1. **Input Handling**: The code retrieves the raw webhook payload and extracts the event type, project UID, and job details.
2. **Event Validation**: Checks if the event type is valid (`JOB_UPDATED` or `JOB_TARGET_UPDATED`) and ensures the project UID is present.
3. **Job UID Extraction**: Depending on the event type, it extracts job UIDs from the webhook payload.
4. **Phrase API Authentication**: Logs into the Phrase API to obtain an authentication token.
5. **Segment Fetching and Upserting**:
   - For each job UID, it fetches segments in batches from the Phrase API.
   - Each segment is checked for valid source and translation text before being upserted into the translation memory table.
6. **Response Construction**: After processing all job UIDs, it builds a response summarizing the operation's success and details.

## Notes
- **Edge Cases**:
  - If no job UIDs are found in the payload, an error is returned.
  - If the fetched segments are empty, pagination stops.
- **Dependencies**: 
  - Requires access to the Phrase API.
  - Database table `translation_memory_dylan_test` must exist and be properly configured.
- **Environment Variables**: 
  - The API username and password are hardcoded (`team@honyaku.org` and `boysbesso1989`), which should be managed securely.
- **Error Handling**: Errors during segment fetching are logged, and pagination stops for that job.
- **[TODO]**: Confirm if the API credentials should be managed differently (e.g., through environment variables).