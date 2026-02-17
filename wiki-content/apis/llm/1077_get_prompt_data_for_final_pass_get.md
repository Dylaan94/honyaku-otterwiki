# Get Prompt Data for Final Pass

## Overview
The `get_prompt_data_for_final_pass` API endpoint retrieves specific data related to prompt processing for a final pass in the LLM (Large Language Model) framework. It consolidates information from multiple database queries to provide a comprehensive response that includes rules, style devices, and potential term bases.

## Details
- **HTTP Method**: GET
- **URL**: `/api/llm/get_prompt_data_for_final_pass`
- **Request Shape**:
  - **Input**:
    - `record_uuid` (optional): A unique identifier for the record.
- **Response Shape**:
  - Returns a JSON object containing:
    - `mqm_rules`: List of rules from the `dqf_mqm_framework_devices` query.
    - `style_devices`: List of style devices filtered by tier.
    - `potential_tb`: List of potential term bases from the `docling_test` query.
- **Authentication**: [TODO]

## How it works
1. The API receives an optional `record_uuid` as input.
2. It executes three database queries:
   - **`dqf_mqm_framework_devices`**: Retrieves a list of rules categorized as "do" and "dont".
   - **`style_devices`**: Fetches style devices where the tier equals 1, returning "trigger" and "instruction".
   - **`docling_test`**: Looks up the potential term base associated with the provided `record_uuid`.
3. The results from these queries are compiled into a single response object.

## Notes
- Ensure that the `record_uuid` is provided if specific term base data is required.
- The queries depend on the existence of the respective tables in the database.
- [TODO] for any specific authentication requirements or headers that may be needed for this API.