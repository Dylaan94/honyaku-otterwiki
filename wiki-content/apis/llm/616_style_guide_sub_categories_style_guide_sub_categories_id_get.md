# Get Style Guide Sub Categories by ID

## Overview
This API endpoint retrieves a specific record from the `style_guide_sub_categories` table based on the provided `style_guide_sub_categories_id`. It ensures that the requested sub-category exists and returns the corresponding data, or an error if not found.

## Details
- **HTTP Method**: GET
- **URL**: `/style_guide_sub_categories/{style_guide_sub_categories_id}`
- **Request Parameters**:
  - `style_guide_sub_categories_id` (integer, optional): The ID of the style guide sub-category to retrieve. Must be greater than or equal to 1.
- **Response Shape**: Returns the style guide sub-category record if found; otherwise, returns a "Not Found" error.
- **Authentication**: [TODO]

## How it works
1. The API accepts a `style_guide_sub_categories_id` as input.
2. It queries the database for a record in the `style_guide_sub_categories` table where the `id` matches the provided `style_guide_sub_categories_id`.
3. If the record is found, it is returned as the response.
4. If the record is not found, an error of type "notfound" is generated with the message "Not Found."

### Code Snippet
```xs
db.get style_guide_sub_categories {
  field_name = "id"
  field_value = $input.style_guide_sub_categories_id
} as $style_guide_sub_categories
```

## Notes
- The `style_guide_sub_categories_id` must be a positive integer (minimum value of 1).
- If the ID does not correspond to an existing record, a "Not Found" error will be returned.
- Ensure that the database connection is properly configured to access the `style_guide_sub_categories` table.
- [TODO] - Include any authentication requirements or additional headers if applicable.