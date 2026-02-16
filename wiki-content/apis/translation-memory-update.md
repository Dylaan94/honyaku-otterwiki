# POST /translation_memory_update

## Overview

Handles Phrase TMS webhook events (`JOB_UPDATED` and `JOB_TARGET_UPDATED`) to incrementally update the translation memory. When Phrase fires a webhook, this endpoint fetches all segments from the affected jobs and upserts them into the translation memory database table (`translation_memory_dylan_test`, table 178).

**API Group:** Phrase Endpoints

## Request

| Field | Value |
|-------|-------|
| **Method** | `POST` |
| **Content-Type** | `application/json` |
| **Body** | Raw Phrase webhook payload (passed through automatically) |

### Webhook Payload Structure

The endpoint expects a standard Phrase TMS webhook payload. The key fields it reads:

| Field | Type | Description |
|-------|------|-------------|
| `event` | string | Must be `JOB_UPDATED` or `JOB_TARGET_UPDATED` |
| `metadata.project.uid` | string | Phrase project UID |
| `metadata.project.name` | string | Project name (stored in TM) |
| `metadata.project.client.name` | string | Client name (stored in TM) |
| `metadata.project.client.uid` | string | Client UID (stored in TM) |
| `jobParts` | array | *(JOB_UPDATED only)* Array of job part objects with `uid` |
| `jobPart` | object | *(JOB_TARGET_UPDATED only)* Single job part object with `uid` |

## How It Works

1. **Receive webhook** - Reads the raw JSON payload from the incoming request.
2. **Validate event type** - Rejects any event that isn't `JOB_UPDATED` or `JOB_TARGET_UPDATED`.
3. **Extract metadata** - Pulls the project UID, project name, client name, and client UID from the webhook payload.
4. **Extract job UIDs** - Handles both event types:
   - `JOB_UPDATED`: maps over the `jobParts` array to collect all job UIDs.
   - `JOB_TARGET_UPDATED`: reads the single `jobPart.uid`.
5. **Authenticate with Phrase API** - Logs in via `POST /auth/login` to get an API token.
6. **Fetch segments** - For each job UID, paginates through the Phrase "Get Segments" API in batches of 500:
   - `GET /projects/{projectUid}/jobs/{jobUid}/segments?beginIndex=X&endIndex=Y`
7. **Upsert into TM** - For each segment that has both a source and non-empty translation:
   - Creates a unique `phrase_ID` from `{jobUid}_{segmentId}`.
   - Upserts a record into `translation_memory_dylan_test` with fields: `phrase_ID`, `ja` (source), `en` (translation), `project`, `client`, `clientUid`, `changedate`.
8. **Return results** - Responds with a summary including success status, event type, project UID, total upserted count, and per-job breakdown.

## Response

```json
{
  "success": true,
  "event": "JOB_UPDATED",
  "project_uid": "abc123",
  "total_upserted": 1250,
  "jobs": [
    { "job_uid": "xyz789", "segments_upserted": 1250 }
  ]
}
```

## Dependencies

| Dependency | Detail |
|------------|--------|
| **Phrase TMS API** | `cloud.memsource.com/web/api2/v1` |
| **Auth credentials** | Hardcoded: `team@honyaku.org` / password in source [TODO: move to env vars] |
| **Database table** | `translation_memory_dylan_test` (table 178) |
| **TM field mapping** | `ja` = source language, `en` = translation |

## Notes

- **Pagination**: Segments are fetched in batches of 500. If a batch returns fewer than 500, pagination stops for that job.
- **Error handling**: If a segment fetch fails for a job, the error is logged and that job's pagination stops, but other jobs continue processing.
- **Idempotency**: Uses `db.add_or_edit` with `phrase_ID` as the unique key, so re-processing the same webhook is safe — it will update existing records rather than create duplicates.
- **[TODO]**: Phrase API credentials are hardcoded in the source. These should be moved to environment variables or a secrets manager.
