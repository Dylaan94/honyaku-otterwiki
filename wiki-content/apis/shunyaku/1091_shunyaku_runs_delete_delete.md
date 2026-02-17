# Delete Shunyaku Run Record

## Overview
This endpoint allows users to delete a Shunyaku run record from the database by marking it as deleted. It is part of the Shunyaku API group and requires user authentication. The deletion is performed logically by updating the record rather than physically removing it from the database.

## Details
- **HTTP Method**: DELETE
- **URL**: `/shunyaku_runs/delete`
- **Authentication**: Requires user authentication.
- **Request Shape**:
  - **Input**:
    - `id` (int): The identifier of the Shunyaku run record to be deleted.
- **Response Shape**:
  - **Success Response**:
    - `success` (boolean): Indicates if the operation was successful.
    - `id` (int): The ID of the deleted record.
    - `message` (string): Confirmation message.

## How it works
1. The endpoint receives a DELETE request with the `id` of the record to be deleted.
2. It uses the `db.edit` function to mark the record as deleted by setting the `delete` field to `true` in the `docling_test` database.
3. Upon successful execution, it constructs a response indicating the success of the operation along with the ID of the deleted record and a confirmation message.

## Notes
- The deletion is logical; the record remains in the database but is marked as deleted.
- Ensure that the user is authenticated before accessing this endpoint.
- [TODO]: Additional error handling or edge cases that may need to be considered.