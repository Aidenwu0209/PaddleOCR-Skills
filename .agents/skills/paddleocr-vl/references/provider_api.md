# Provider API Reference: PaddleOCR-VL

This document describes the external provider API contract that this skill depends on.

## Endpoint

**POST** `<PADDLEOCR_VL_API_URL>`

Where the URL is obtained from [Paddle AI Studio](https://paddleocr.com) (select VL model).

Example: `https://xxxxx.aistudio-app.com/layout-parsing`

## Authentication

**Header:**
```
Authorization: token <ACCESS_TOKEN>
```

Where `<ACCESS_TOKEN>` is the API token obtained from Paddle AI Studio.

## Request Body

### URL-based Input

```json
{
  "file_url": "https://example.com/document.pdf",
  "parse_all": true,
  "include_layout": true,
  "include_all_elements": true
}
```

### Base64-encoded Input

```json
{
  "file": "<base64_encoded_content>",
  "fileType": 0,
  "parse_all": true,
  "include_layout": true,
  "include_all_elements": true
}
```

### Key Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `file_url` | string | URL to document (PDF or image) |
| `file` | string | Base64-encoded file content |
| `fileType` | number | `0` = PDF, `1` = Image |
| `parse_all` | boolean | Parse all document elements |
| `include_layout` | boolean | Include layout analysis |
| `include_all_elements` | boolean | Include all element types |

## Response Structure

### Success Response

```json
{
  "result": {
    "layout": {
      "regions": [...],
      "reading_order": [...]
    },
    "full_text": "...",
    "elements": [...]
  }
}
```

### Error Response

HTTP status codes indicate errors:

| HTTP Status | Meaning | Mapped Error Code |
|-------------|---------|-------------------|
| 200 | Success | - |
| 401 | Authentication failed | `PROVIDER_AUTH_ERROR` |
| 403 | Access forbidden | `PROVIDER_AUTH_ERROR` |
| 429 | Quota/rate limit exceeded | `PROVIDER_QUOTA_EXCEEDED` |
| 503 | Service overloaded | `PROVIDER_OVERLOADED` |
| 504 | Gateway timeout | `PROVIDER_TIMEOUT` |
| Other | Unknown error | `PROVIDER_ERROR` |

## Supported File Formats

| Format | Extension | fileType |
|--------|-----------|----------|
| PDF | .pdf | 0 |
| PNG | .png | 1 |
| JPEG | .jpg, .jpeg | 1 |
| BMP | .bmp | 1 |
| TIFF | .tiff, .tif | 1 |
| WebP | .webp | 1 |

## Limitations

- **Maximum file size**: 20MB per request (configurable via `PADDLEOCR_VL_MAX_FILE_SIZE_MB`)
- **Maximum pages**: 10 pages per request
- **Timeout**: 30 seconds default (configurable via `PADDLEOCR_VL_TIMEOUT_MS`)

## Best Practices

1. **Use URL for large files**: Prefer `file_url` over base64 for files >5MB
2. **Handle timeouts**: VL processing can take 3-10 seconds per page
3. **Retry on 503/504**: Use exponential backoff (up to 2 retries)
4. **Never log tokens**: Keep credentials secure
5. **Cache responses**: Results can be cached for 10 minutes

## Request Example

```bash
curl -X POST "https://xxxxx.aistudio-app.com/layout-parsing" \
  -H "Authorization: token YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "file_url": "https://example.com/document.pdf",
    "parse_all": true,
    "include_layout": true,
    "include_all_elements": true
  }'
```
