# Provider API Reference: Paddle AI Studio PP-OCRv5

This document describes the external provider API contract that this skill depends on.

## Endpoint

**POST** `<PADDLEOCR_OCR_API_URL>`

Where the URL is obtained from [Paddle AI Studio](https://paddleocr.com) (e.g.: `https://your-subdomain.aistudio-app.com/ocr`).

## Authentication

**Header:**
```
Authorization: token <ACCESS_TOKEN>
```

Where `<ACCESS_TOKEN>` is the API token obtained by the user from Paddle AI Studio.

## Request Body

```jsonc
{
  "file": "https://example.com/image.png",  // URL or base64 (without data: prefix)
  "fileType": 1,                            // 0=PDF, 1=Image
  "visualize": false,                       // Default false (avoid large responses)

  // Text detection options
  "textDetLimitSideLen": 736,               // Maximum side length for detection
  "textDetLimitType": "max",                // "min" or "max"
  "textDetThresh": 0.3,                     // Detection threshold
  "textDetBoxThresh": 0.6,                  // Box threshold
  "textDetUnclipRatio": 1.5,                // Unclip ratio

  // Text recognition options
  "textRecScoreThresh": 0.0,                // Recognition score threshold

  // Document preprocessing options
  "useDocOrientationClassify": false,       // Enable orientation correction
  "useDocUnwarping": false,                 // Enable unwarping/skew correction
  "useTextlineOrientation": false           // Enable textline orientation
}
```

### Key Parameters

- **file**: URL or base64 string of image/PDF (without `data:` URI prefix)
- **fileType**:
  - `0` = PDF
  - `1` = Image
- **visualize**: If `true`, returns visualization image (increases response size)
- **useDocOrientationClassify**: Correct page orientation (0°/90°/180°/270°)
- **useDocUnwarping**: Correct perspective distortion and skew
- **useTextlineOrientation**: Correct individual text line angles

## Response Structure

### Success Response (errorCode == 0)

```jsonc
{
  "errorCode": 0,
  "errorMsg": "",
  "logId": "unique-log-id",
  "result": {
    "ocrResults": [
      {
        "prunedResult": {
          "rec_texts": ["Invoice", "Amount", "123.45"],  // Recognized text
          "rec_scores": [0.98, 0.95, 0.92],              // Confidence scores (may be missing)
          "rec_boxes": [                                  // Bounding boxes (may be missing)
            [10, 20, 100, 50],
            [10, 60, 150, 90],
            [200, 60, 300, 90]
          ],
          "rec_polys": [...]                              // Polygons (alternative to boxes)
        }
      }
    ]
  }
}
```

### Error Response (errorCode != 0)

```jsonc
{
  "errorCode": 500,
  "errorMsg": "Invalid parameter",
  "logId": "unique-log-id"
}
```

## Error Codes

| HTTP Status | errorCode | Meaning | Mapped Error Code |
|-------------|-----------|---------|-------------------|
| 403 | N/A | Authentication failed | `PROVIDER_AUTH_ERROR` |
| 429 | N/A | Quota/rate limit exceeded | `PROVIDER_QUOTA_EXCEEDED` |
| 500 | 500 | Invalid parameters | `PROVIDER_BAD_REQUEST` |
| 503 | N/A | Service overloaded | `PROVIDER_OVERLOADED` |
| 504 | N/A | Gateway timeout | `PROVIDER_TIMEOUT` |
| Other | Other | Unknown error | `PROVIDER_ERROR` |

## Field Compatibility Notes

- **rec_scores**: May be missing or empty. Default to 0.5 if needed.
- **rec_boxes**: May be missing. Use `rec_polys` as fallback.
- **rec_polys**: May be missing. Bounding box information may not be available.
- **visualize result**: Only returned when `visualize: true` (increases response size).

## Best Practices

1. **Always set visualize to false** unless explicitly requested by user (reduces response size and latency)
2. **Handle missing fields gracefully** (rec_scores, rec_boxes, rec_polys may not exist)
3. **Retry on 503/504** with exponential backoff (up to 2 retries)
4. **Never log or print tokens** in any output or logs
5. **Normalize host input** to handle user errors (https://, trailing /ocr, etc.)

## Request Example

```bash
curl -X POST https://your-subdomain.aistudio-app.com/ocr \
  -H "Authorization: token YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "file": "https://example.com/test.png",
    "fileType": 1,
    "visualize": false,
    "useDocOrientationClassify": true,
    "useDocUnwarping": false,
    "useTextlineOrientation": false,
    "textDetLimitSideLen": 736,
    "textDetLimitType": "max",
    "textDetThresh": 0.3,
    "textDetBoxThresh": 0.6,
    "textDetUnclipRatio": 1.5,
    "textRecScoreThresh": 0.0
  }'
```
