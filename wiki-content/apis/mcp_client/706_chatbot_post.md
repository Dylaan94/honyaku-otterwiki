# MCP Client Chatbot API

## Overview
The MCP Client Chatbot API is designed to facilitate interactions with OpenAI models by processing user queries and integrating with MCP tools. It allows for the submission of user messages, optional system prompts, and existing conversation history to generate appropriate responses from the AI.

## Details
- **HTTP Method**: POST
- **Endpoint**: `/chatbot`
- **Request Shape**:
  - `user_query`: (string) The current message from the user (required).
  - `system_prompt`: (string, optional) An optional system message to replace the existing one.
  - `conversation`: (json, optional) The existing conversation formatted for OpenAI.
  
- **Response Shape**: The response will contain instructions for tool usage and the AI's response based on the provided inputs.
- **Authentication**: Requires a bearer token specified in the environment variable `$request_auth_token`.

## How it works
1. **Input Processing**: The API accepts a user query, an optional system prompt, and an optional conversation history.
2. **MCP Tools Retrieval**: It makes a request to an MCP server to retrieve available tools, converting them into a format compatible with OpenAI's API.
3. **Tool Transformation**: The retrieved tools are transformed into a JSON schema that OpenAI can understand, including descriptions and parameter specifications.
4. **ChatGPT Interaction**: The API constructs a message array, including the system prompt (if provided) and the conversation history, and sends this to the ChatGPT model for processing.
5. **Response Handling**: The API receives the response from ChatGPT, which includes instructions for tool usage and the AI's generated content.

## Notes
- **Dependencies**: Requires access to the MCP server at `https://xkqd-rhqz-zkri.t7.xano.io/x2/mcp/ZLRkdYcY/mcp/sse`.
- **Environment Variables**: The API relies on the `$request_auth_token` environment variable for authentication.
- **Error Handling**: Ensure that the input data is properly formatted to avoid errors during processing.
- **Edge Cases**: If the system prompt is empty, the existing system message will be used if available. If no conversation history is provided, the API will still function, but the context may be limited.