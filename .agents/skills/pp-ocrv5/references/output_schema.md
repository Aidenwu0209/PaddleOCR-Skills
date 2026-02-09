# PP-OCRv5 Output Schema

This document defines the output format returned by `ocr_caller.py`.

## Schema Version

**v1.0** (simplified)

## Output Structure

All responses follow this structure:

```typescript
{
  ok: boolean,           // true = success, false = error
  text: string,          // Extracted text (empty on error)
  result: object | null, // Raw API response (null on error)
  error: Error | null    // Error details (null on success)
}
```

## Success Response

```json
{
  "ok": true,
  "text": "Line 1\nLine 2\n\nPage 2 text...",
  "result": {
    "errorCode": 0,
    "errorMsg": "success",
    "result": {
      "ocrResults": [
        {
          "prunedResult": {
            "rec_texts": ["Line 1", "Line 2"],
            "rec_scores": [0.98, 0.95],
            "rec_boxes": [[10, 20, 100, 50], [10, 60, 200, 90]]
          }
        }
      ]
    }
  },
  "error": null
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `ok` | boolean | `true` if OCR succeeded |
| `text` | string | All recognized text, pages separated by `\n\n` |
| `result` | object | Raw API response for debugging |
| `error` | null | Always null on success |

## Error Response

```json
{
  "ok": false,
  "text": "",
  "result": null,
  "error": {
    "code": "API_ERROR",
    "message": "Authentication failed (403). Check your token."
  }
}
```

### Error Codes

| Code | Description |
|------|-------------|
| `INPUT_ERROR` | Invalid input (missing file, unsupported format) |
| `CONFIG_ERROR` | API not configured |
| `API_ERROR` | API call failed (auth, timeout, server error) |

## Usage Examples

### Extract Text

```python
import json
import subprocess

result = subprocess.run(
    ["python", "scripts/pp-ocrv5/ocr_caller.py", "--file-url", "URL"],
    capture_output=True, text=True
)
data = json.loads(result.stdout)

if data["ok"]:
    print(data["text"])
else:
    print(f"Error: {data['error']['message']}")
```

### Check Success

```python
if data["ok"]:
    # Success - use data["text"]
    pass
else:
    # Error - check data["error"]["code"] and data["error"]["message"]
    pass
```

## Command Line

```bash
# Basic OCR
python scripts/pp-ocrv5/ocr_caller.py --file-url "URL" --pretty

# OCR local file
python scripts/pp-ocrv5/ocr_caller.py --file-path "doc.pdf" --pretty

# Save to file
python scripts/pp-ocrv5/ocr_caller.py --file-url "URL" --output result.json
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (check `error` field) |
