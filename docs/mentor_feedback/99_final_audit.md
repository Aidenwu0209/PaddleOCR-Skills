# Final Mentor Audit Report

**Date**: 2026-02-05
**Scope**: Post step 0-7 comprehensive audit

## A. Legacy URL/Keyword Scan Results

### Keywords Scanned

| Keyword | Status | Notes |
|---------|--------|-------|
| `aistudio.baidu.com` | CLEAN | Only in migration docs (allowed) |
| `ppocrv5` | CLEAN | No matches |
| `paddleocr-vl-1.5` | CLEAN | No matches |
| `AISTUDIO_HOST` | CLEAN | Only in code fallback logic (allowed) |

### aistudio.baidu.com References

**Cleaned** (0 user-facing references):
- `.env.example` - Updated to paddleocr.com
- `README.md` - Updated to paddleocr.com
- `README-cn.md` - Updated to paddleocr.com
- `npx-package/templates/.env.example` - Updated to paddleocr.com
- `skills/*/references/provider_api.md` - Updated to paddleocr.com
- `npx-package/templates/*/references/*/provider_api.md` - Updated

**Preserved** (migration documentation only):
- `docs/mentor_feedback/02_env_unification.md` - Migration guide showing old vs new URLs

## B. Environment Variable Naming Contract

### Recommended (Primary) Names

| Skill | API URL Var | Token Var |
|-------|-------------|-----------|
| **PP-OCRv5** | `PADDLEOCR_OCR_API_URL` | `PADDLEOCR_ACCESS_TOKEN` |
| **PaddleOCR-VL** | `PADDLEOCR_VL_API_URL` | `PADDLEOCR_VL_ACCESS_TOKEN` |

### Compatibility Mapping (Fallback Order)

**PP-OCRv5 API URL**:
1. `PADDLEOCR_OCR_API_URL` (recommended)
2. `PADDLEOCR_API_URL` (legacy v1)
3. `API_URL` (legacy v0)
4. `AISTUDIO_HOST` (legacy v0)

**PP-OCRv5 Token**:
1. `PADDLEOCR_ACCESS_TOKEN` (recommended)
2. `PADDLEOCR_TOKEN` (legacy v1)
3. `PADDLE_OCR_TOKEN` (legacy v0)

**PaddleOCR-VL API URL**:
1. `PADDLEOCR_VL_API_URL` (recommended, unchanged)
2. `VL_API_URL` (legacy v0)

**PaddleOCR-VL Token**:
1. `PADDLEOCR_VL_ACCESS_TOKEN` (recommended)
2. `PADDLEOCR_VL_TOKEN` (legacy v1)
3. `VL_TOKEN` (legacy v0)

### Deprecation Behavior

When legacy env vars are used, code logs a warning:
```
DEPRECATION: PADDLEOCR_TOKEN is deprecated, use PADDLEOCR_ACCESS_TOKEN instead
```

## C. Template Self-Containment Verification

### Compile Results

```
python -m compileall skills/ npx-package/templates/ -q
```
**Result**: SUCCESS (no errors)

### Template Independence

| Template | Status | Notes |
|----------|--------|-------|
| `npx-package/templates/pp-ocrv5/` | Self-contained | `_lib.py` inlines shared code |
| `npx-package/templates/paddleocr-vl/` | Self-contained | `_lib.py` inlines shared code |

Templates do NOT depend on `skills/_common/` - they have their own `_lib.py` with inlined shared code.

### Smoke Test Behavior (No Token)

Both smoke tests exit with code 1 and show friendly guidance:
```
[2/3] Checking configuration...
  X PADDLEOCR_OCR_API_URL not configured

============================================================
HOW TO GET YOUR API CREDENTIALS
============================================================
1. Visit: https://paddleocr.com
...
```

No stack traces are shown.

## D. Additional Fixes Applied

### SKILL.md CLI Flag Update

**PP-OCRv5 SKILL.md**: `--mode` changed to `--preset`
- Line 103-109: Mode selection table updated
- Line 127: Example command updated

## E. Modified Files Summary

### Core Skills (skills/)
- `skills/pp-ocrv5/SKILL.md` - `--mode` → `--preset`
- `skills/pp-ocrv5/scripts/lib.py` - New env var names
- `skills/pp-ocrv5/scripts/smoke_test.py` - New env var names + messages
- `skills/pp-ocrv5/scripts/configure.py` - New env var names
- `skills/pp-ocrv5/references/provider_api.md` - URL reference updated
- `skills/paddleocr-vl/scripts/lib.py` - New env var names
- `skills/paddleocr-vl/scripts/smoke_test.py` - New env var names + messages
- `skills/paddleocr-vl/scripts/configure.py` - New env var names
- `skills/paddleocr-vl/references/provider_api.md` - URL reference updated

### Root Files
- `.env.example` - New env var names, URL updated
- `README.md` - aistudio URL updated
- `README-cn.md` - aistudio URL updated

### NPX Package Templates
- `npx-package/templates/.env.example` - New env var names, URL updated
- `npx-package/templates/pp-ocrv5/scripts/pp-ocrv5/_lib.py` - New env var names
- `npx-package/templates/pp-ocrv5/scripts/pp-ocrv5/smoke_test.py` - New env var names
- `npx-package/templates/pp-ocrv5/scripts/pp-ocrv5/configure.py` - New env var names
- `npx-package/templates/pp-ocrv5/references/pp-ocrv5/provider_api.md` - URL updated
- `npx-package/templates/paddleocr-vl/scripts/paddleocr-vl/_lib.py` - New env var names
- `npx-package/templates/paddleocr-vl/scripts/paddleocr-vl/smoke_test.py` - New env var names
- `npx-package/templates/paddleocr-vl/scripts/paddleocr-vl/configure.py` - New env var names
- `npx-package/templates/paddleocr-vl/references/paddleocr-vl/provider_api.md` - URL updated

## F. Verification Commands

```bash
# Verify no aistudio.baidu.com in user-facing docs
rg "aistudio\.baidu\.com" --type md --glob "!docs/mentor_feedback/*"
# Expected: no results

# Verify syntax
python -m compileall skills/ npx-package/templates/ -q

# Verify friendly error messages
python skills/pp-ocrv5/scripts/smoke_test.py --skip-api-test
python skills/paddleocr-vl/scripts/smoke_test.py --skip-api-test
```

## G. Audit Conclusion

All mentor feedback items #1 and #8 have been addressed:
- #1: All user-facing docs point to `paddleocr.com`
- #8: Environment variables renamed to mentor-suggested format with full backward compatibility

Templates are self-contained and can run independently after installation.
