# PaddleOCR-VL Output Schema

This document defines the unified output format returned by `vl_caller.py`, including layout structure and element types.

## Schema Version

**v0.1** (stable)

## Output Structure

All responses follow this top-level structure:

```typescript
{
  ok: boolean,              // true indicates parsing success
  result: Result | null,    // Parsing results (null on error)
  metadata: Metadata,       // Processing metadata
  error: Error | null       // Error details (null on success)
}
```

## Result (success only)

```typescript
{
  layout: Layout,           // Document layout structure
  elements: Element[],      // All detected elements
  full_text: string         // Combined text from all elements
}
```

## Layout Structure

The layout object describes the document's spatial organization:

```typescript
{
  regions: Region[],        // Detected regions
  reading_order: number[],  // Order to read regions (by region id)
  page_number: number       // Current page number
}
```

### Region

```typescript
{
  id: number,               // Unique region identifier
  type: RegionType,         // Region type (see below)
  bbox: [x1, y1, x2, y2],   // Bounding box coordinates
  confidence: number        // Detection confidence (0.0-1.0)
}
```

### Region Types

**Text Regions:**
- `title` - Headings and titles
- `paragraph` - Regular text paragraphs
- `caption` - Image/table captions
- `footnote` - Footnotes and references
- `header` - Page headers
- `footer` - Page footers

**Non-Text Regions:**
- `table` - Tabular data
- `figure` - Images, charts, diagrams
- `formula` - Mathematical formulas

## Element Types

### Text Element

```json
{
  "type": "text",
  "content": "The actual text content",
  "bbox": [100, 200, 500, 250],
  "confidence": 0.95,
  "language": "en"
}
```

### Table Element

```json
{
  "type": "table",
  "content": {
    "rows": 3,
    "cols": 2,
    "cells": [
      ["Header 1", "Header 2"],
      ["Data 1", "Data 2"],
      ["Data 3", "Data 4"]
    ]
  },
  "bbox": [100, 300, 500, 450],
  "confidence": 0.88
}
```

### Formula Element

```json
{
  "type": "formula",
  "content": "E = mc^2",
  "latex": "$E = mc^2$",
  "bbox": [200, 500, 400, 530],
  "confidence": 0.92
}
```

### Figure Element

```json
{
  "type": "figure",
  "content": {
    "description": "Bar chart showing sales data",
    "extracted_data": {...}
  },
  "bbox": [100, 600, 500, 800],
  "confidence": 0.85
}
```

## Metadata

```typescript
{
  processing_time_ms: number,    // Processing time in milliseconds
  total_pages: number,           // Total pages in document
  languages_detected: string[]   // Detected languages (ISO 639-1 codes)
}
```

## Error Response

```typescript
{
  ok: false,
  result: null,
  error: {
    code: ErrorCode,            // Unified error code
    message: string,            // Human-readable message
    details: object             // Additional context
  }
}
```

### ErrorCode Enum

- `CONFIG_ERROR` - Configuration not set
- `PROVIDER_AUTH_ERROR` - Authentication failed (401/403)
- `PROVIDER_QUOTA_EXCEEDED` - Quota/rate limit exceeded (429)
- `PROVIDER_BAD_REQUEST` - Invalid parameters
- `PROVIDER_OVERLOADED` - Service overloaded (503)
- `PROVIDER_TIMEOUT` - Gateway timeout (504)
- `PROVIDER_ERROR` - Other provider errors
- `NETWORK_ERROR` - Network connection error
- `PARSE_ERROR` - Response parsing error

## Example: Success Response

```json
{
  "ok": true,
  "result": {
    "layout": {
      "regions": [
        {"id": 0, "type": "title", "bbox": [100, 50, 500, 100], "confidence": 0.95},
        {"id": 1, "type": "paragraph", "bbox": [100, 150, 500, 300], "confidence": 0.92},
        {"id": 2, "type": "table", "bbox": [100, 350, 500, 550], "confidence": 0.88}
      ],
      "reading_order": [0, 1, 2],
      "page_number": 1
    },
    "elements": [
      {"type": "text", "content": "Chapter 1: Introduction", "bbox": [100, 50, 500, 100], "confidence": 0.95},
      {"type": "text", "content": "This is the main content...", "bbox": [100, 150, 500, 300], "confidence": 0.92},
      {"type": "table", "content": {"rows": 2, "cols": 2, "cells": [["A", "B"], ["1", "2"]]}, "bbox": [100, 350, 500, 550], "confidence": 0.88}
    ],
    "full_text": "Chapter 1: Introduction\n\nThis is the main content..."
  },
  "metadata": {
    "processing_time_ms": 3500,
    "total_pages": 1,
    "languages_detected": ["en"]
  },
  "error": null
}
```

## Example: Error Response

```json
{
  "ok": false,
  "result": null,
  "metadata": {
    "processing_time_ms": 150,
    "total_pages": 0,
    "languages_detected": []
  },
  "error": {
    "code": "PROVIDER_AUTH_ERROR",
    "message": "Authentication failed (HTTP 403). Check your PADDLEOCR_VL_TOKEN.",
    "details": {"status_code": 403}
  }
}
```

## Bounding Box Format

All bounding boxes use the format: `[x1, y1, x2, y2]`
- (x1, y1): Top-left corner
- (x2, y2): Bottom-right corner
- Coordinates are absolute pixel positions

## Reading Order

The `reading_order` array indicates the correct sequence to read regions:
- Determined by spatial layout (top-to-bottom, left-to-right)
- Accounts for document structure (titles before content)
- Handles multi-column layouts automatically

## Quality Metrics

Each element includes a confidence score (0.0 to 1.0):

| Score Range | Quality Level | Description |
|-------------|---------------|-------------|
| 0.90 - 1.00 | Excellent | Highly reliable |
| 0.75 - 0.89 | Good | Generally reliable |
| 0.60 - 0.74 | Acceptable | May have minor errors |
| 0.00 - 0.59 | Poor | Likely has errors |

## Usage Guide

### For Agents/Scripts

1. **Check `ok` first**: `if response.ok:`
2. **Extract text**: `response.result.full_text`
3. **Extract structured data**: Iterate `response.result.elements`
4. **Follow reading order**: Use `response.result.layout.reading_order`
5. **Handle errors**: Check `response.error.code` and `response.error.message`

### For Debugging

1. **Check metadata**: `response.metadata.processing_time_ms`
2. **Check layout**: `response.result.layout.regions` for spatial info
3. **Low confidence**: Filter elements by confidence threshold
