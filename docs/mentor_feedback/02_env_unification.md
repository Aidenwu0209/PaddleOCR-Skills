# Mentor Feedback #4: Environment Variable Unification

**Date**: 2026-02-05
**Status**: Completed

---

## Summary

Unified API domain to `paddleocr.com` and standardized environment variable naming to `PADDLEOCR_*` prefix across all components.

---

## Changes Made

### 1. Environment Variable Naming

| Component | Old Variable | New Variable |
|-----------|-------------|--------------|
| **PP-OCRv5** | `API_URL` | `PADDLEOCR_API_URL` |
| **PP-OCRv5** | `PADDLE_OCR_TOKEN` | `PADDLEOCR_TOKEN` |
| **PP-OCRv5** | `AISTUDIO_HOST` | `PADDLEOCR_API_URL` |
| **PP-OCRv5** | `PADDLE_OCR_TIMEOUT_MS` | `PADDLEOCR_TIMEOUT_MS` |
| **PP-OCRv5** | `PADDLE_OCR_MAX_RETRY` | `PADDLEOCR_MAX_RETRY` |
| **PP-OCRv5** | `PADDLE_OCR_CACHE_TTL_SEC` | `PADDLEOCR_CACHE_TTL_SEC` |
| **PaddleOCR-VL** | `VL_API_URL` | `PADDLEOCR_VL_API_URL` |
| **PaddleOCR-VL** | `VL_TOKEN` | `PADDLEOCR_VL_TOKEN` |
| **PaddleOCR-VL** | `VL_TIMEOUT_MS` | `PADDLEOCR_VL_TIMEOUT_MS` |
| **PaddleOCR-VL** | `VL_MAX_RETRY` | `PADDLEOCR_VL_MAX_RETRY` |
| **PaddleOCR-VL** | `VL_CACHE_TTL_SEC` | `PADDLEOCR_VL_CACHE_TTL_SEC` |
| **PaddleOCR-VL** | `VL_MAX_FILE_SIZE_MB` | `PADDLEOCR_VL_MAX_FILE_SIZE_MB` |

### 2. API Domain Unification

| Old Domain | New Domain |
|------------|------------|
| `https://aistudio.baidu.com/paddleocr/task` | `https://paddleocr.com` |
| `https://aistudio.baidu.com/paddleocr` | `https://paddleocr.com` |

---

## Legacy Support

**Backward compatibility is maintained** - Old environment variables will continue to work but will emit deprecation warnings.

### Deprecation Warning Examples

When using old environment variables, users will see warnings like:
```
DEPRECATION: API_URL is deprecated, please use PADDLEOCR_API_URL instead
DEPRECATION: VL_TOKEN is deprecated, please use PADDLEOCR_VL_TOKEN instead
```

### Priority Order (PP-OCRv5)

1. `PADDLEOCR_API_URL` (new standard)
2. `API_URL` (legacy, deprecated)
3. `AISTUDIO_HOST` (legacy, deprecated)

For token:
1. `PADDLEOCR_TOKEN` (new standard)
2. `PADDLE_OCR_TOKEN` (legacy, deprecated)
3. `PADDLE_OCR_TOKEN_FALLBACK` (legacy)
4. `COZE_PP_OCRV5_*` prefix scan (legacy)

### Priority Order (PaddleOCR-VL)

1. `PADDLEOCR_VL_API_URL` (new standard)
2. `VL_API_URL` (legacy, deprecated)

For token:
1. `PADDLEOCR_VL_TOKEN` (new standard)
2. `VL_TOKEN` (legacy, deprecated)

---

## Files Modified

### Core Libraries
- `skills/pp-ocrv5/scripts/lib.py` - Updated Config class with new env var names
- `skills/paddleocr-vl/scripts/lib.py` - Updated Config class with new env var names

### Configuration Scripts
- `skills/pp-ocrv5/scripts/configure.py` - Writes `PADDLEOCR_*` keys, points to paddleocr.com
- `skills/paddleocr-vl/scripts/configure.py` - Writes `PADDLEOCR_VL_*` keys, points to paddleocr.com

### Skill Definitions
- `skills/pp-ocrv5/SKILL.md` - Updated configuration guidance
- `skills/paddleocr-vl/SKILL.md` - Updated configuration guidance

### NPX Package
- `npx-package/lib/installer.js` - Updated URL references
- `npx-package/lib/verify.js` - Updated URL references
- `npx-package/README.md` - Updated env var examples and URLs
- `npx-package/templates/.env.example` - New env var format

### NPX Package Templates
- `npx-package/templates/pp-ocrv5/scripts/pp-ocrv5/_lib.py` - Synced with skills/
- `npx-package/templates/pp-ocrv5/scripts/pp-ocrv5/configure.py` - Synced with skills/
- `npx-package/templates/pp-ocrv5/skills/pp-ocrv5/SKILL.md` - Updated guidance
- `npx-package/templates/paddleocr-vl/scripts/paddleocr-vl/_lib.py` - Synced with skills/
- `npx-package/templates/paddleocr-vl/scripts/paddleocr-vl/configure.py` - Synced with skills/
- `npx-package/templates/paddleocr-vl/skills/paddleocr-vl/SKILL.md` - Updated guidance

### Documentation
- `README.md` - Updated all URL references
- `README-cn.md` - Updated all URL references
- `.env.example` - New env var format with deprecation notice

---

## Migration Guide

### For Existing Users

Users with existing `.env` files can continue using old variable names - they will work but show deprecation warnings.

**Recommended migration**:

1. Open `.env` file
2. Rename variables:
   ```bash
   # Before
   API_URL=https://xxx.aistudio-app.com/ocr
   PADDLE_OCR_TOKEN=your_token
   VL_API_URL=https://xxx.com/v1
   VL_TOKEN=your_vl_token

   # After
   PADDLEOCR_API_URL=https://xxx.paddleocr.com/ocr
   PADDLEOCR_TOKEN=your_token
   PADDLEOCR_VL_API_URL=https://xxx.paddleocr.com/v1
   PADDLEOCR_VL_TOKEN=your_vl_token
   ```

### For New Users

New installations will automatically use the new environment variable names.

---

## Verification

```bash
# Check no old URL references remain
grep -r "aistudio\.baidu\.com/paddleocr" --include="*.md" --include="*.js" --include="*.json" --include="*.py"
# Expected: No output

# Verify Python syntax
python -m py_compile skills/pp-ocrv5/scripts/lib.py
python -m py_compile skills/pp-ocrv5/scripts/configure.py
python -m py_compile skills/paddleocr-vl/scripts/lib.py
python -m py_compile skills/paddleocr-vl/scripts/configure.py
# Expected: No errors
```

---

## Notes

- Error messages now point to `https://paddleocr.com` instead of the old Baidu AI Studio URL
- The `model_version` field in API responses may still contain `paddleocr-vl-1.5` as this reflects the actual model version from the provider API
- Template files in `npx-package/templates/` are now synchronized with `skills/` directory
