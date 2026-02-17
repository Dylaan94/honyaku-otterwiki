# Add LLM User Runs Record

## Overview
This code defines an API endpoint for adding records of user runs in a Language Learning Model (LLM) system. It handles the submission of user input, validates it, and interacts with external APIs to process the input, while also managing user and organization data.

## Details
- **HTTP Method**: POST
- **URL**: `/llm_user_runs`
- **Request Shape**:
  - Input fields:
    - `input_text`: The text to be processed.
    - `prior_run_uuid` (optional): UUID of a previous run for reruns.
    - `end_client_id` (optional): ID for setting the organization.
- **Response Shape**: JSON response containing the status of the request and other relevant data.
- **Authentication**: Requires user authentication.

## How it works
1. **Input Validation**: The input text length is checked to ensure it does not exceed 1500 characters.
2. **User Profile Retrieval**: The user's profile is fetched to obtain the organization ID.
3. **Organization Data Fetching**: Depending on whether `end_client_id` is provided, the organization details are retrieved.
4. **API Request to LLM**: A POST request is made to an external LLM API with the user input and organization details.
5. **Job Status Monitoring**: The job status is monitored in a loop until it is finished, updating the database and streaming status updates as necessary.
6. **Response Processing**: The response from the LLM API is processed to extract relevant data, including memory flags and term pairs.

## Notes
- **Character Limit**: Input text is limited to 1500 characters. Exceeding this limit will trigger an error.
- **Deployment URLs**: The code includes multiple base URLs for different deployments (Europe, Tokyo, etc.).
- **Error Handling**: The code includes error handling for API failures and input validation.
- **Database Operations**: Records are added to the "LLM User Runs" table with relevant metadata.
- **Real-time Updates**: The system streams updates regarding the job status to a specified channel.
- **[TODO]**: Further details on the external LLM API response structure and specific error messages.