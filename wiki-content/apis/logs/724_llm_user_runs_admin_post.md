# LLM User Runs Admin POST API

## Overview
The LLM User Runs Admin POST API is responsible for creating and managing records of user runs in a language model processing system. It handles user input, validates it, interacts with an external LLM API for processing, and tracks the status of the processing job.

## Details
- **HTTP Method**: POST
- **URL**: `/llm_user_runs_admin`
- **Request Shape**:
  - Input fields:
    - `text`: User input text (required)
    - `prior_run_uuid`: UUID of a previous run (optional)
    - `phrase_clients_id`: ID of the phrase client (optional)
    - `source_lang`: Source language code (required)
    - `target_lang`: Target language code (required)
    - `style_guide`: Style guide reference (optional)
    - `reference_file_ids`: IDs of reference files (optional)
- **Response Shape**: Streamed updates on the status of the job.
- **Authentication**: Requires user authentication via `users` group.

## How it works
1. **Input Validation**: The API first checks the length of the input text to ensure it does not exceed 1500 characters.
2. **User Profile Retrieval**: It fetches the user's profile to obtain the organization ID.
3. **Organization Details**: Using the organization ID, it retrieves relevant organization details, including the phrase client ID.
4. **API Request to LLM**: It sends a POST request to an external LLM API with the user input and other parameters.
5. **Job Status Tracking**: It continuously polls the LLM API for the status of the job until it is marked as finished.
6. **Database Updates**: Throughout the process, it updates the database with the job status, results, and any relevant metrics.
7. **Real-time Streaming**: The API streams updates to the client regarding the status of the job.

## Notes
- The API enforces a character limit of 1500 for the input text.
- The external LLM API endpoint is hardcoded and may need updates if the service changes.
- The API uses a UUID generation function to uniquely identify each job.
- Error handling is implemented to manage API response errors and input validation issues.
- The API streams real-time updates, which may require a suitable client-side implementation to handle the streamed data.
- [TODO]: Additional dependencies or environment variables required for the API to function properly.