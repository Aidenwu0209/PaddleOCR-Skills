# Mentor Feedback #2/#3: Naming Convention Changes

**Date**: 2026-02-05
**Status**: Completed

---

## Summary

Standardized directory and skill naming conventions as per mentor feedback.

---

## Breaking Changes

### Directory Renames

| Old Path | New Path |
|----------|----------|
| `skills/ppocrv5/` | `skills/pp-ocrv5/` |
| `skills/paddleocr-vl-1.5/` | `skills/paddleocr-vl/` |
| `npx-package/templates/ppocrv5/` | `npx-package/templates/pp-ocrv5/` |
| `npx-package/templates/paddleocr-vl-1.5/` | `npx-package/templates/paddleocr-vl/` |

### Skill Name Changes

| Old Name | New Name |
|----------|----------|
| `ppocrv5` | `pp-ocrv5` |
| `paddleocr-vl-1.5` | `paddleocr-vl` |

### CLI Flag Changes

| Old Flag | New Flag |
|----------|----------|
| `--ppocrv5` | `--pp-ocrv5` |
| `--skill ppocrv5` | `--skill pp-ocrv5` |
| `--skill paddleocr-vl-1.5` | `--skill paddleocr-vl` |

---

## Alias Support Status

**NOT IMPLEMENTED**

### Reason

The `npx skills add` command (from the Claude Code ecosystem) does not support skill aliases at the installer level. The skill resolution is based on directory structure matching, not a mapping table.

To implement aliases would require:
1. Maintaining a mapping file that maps old names to new directories
2. Modifying the installer logic to check for aliases before directory lookup
3. Potential conflicts with future official skill naming conventions

### Impact

Users who previously installed with old names must:
1. Remove old installation: Delete `~/.claude/skills/ppocrv5/` or `~/.claude/skills/paddleocr-vl-1.5/`
2. Reinstall with new names: `npx skills add Aidenwu0209/PaddleOCR-Skills --skill pp-ocrv5`

### Migration Guide

```bash
# Remove old installations
rm -rf ~/.claude/skills/ppocrv5
rm -rf ~/.claude/skills/paddleocr-vl-1.5

# Install new versions
npx skills add Aidenwu0209/PaddleOCR-Skills

# Or install specific skills
npx skills add Aidenwu0209/PaddleOCR-Skills --skill pp-ocrv5
npx skills add Aidenwu0209/PaddleOCR-Skills --skill paddleocr-vl
```

---

## Files Modified

### Core Files
- `README.md` - Updated all paths and commands
- `README-cn.md` - Updated all paths and commands (Chinese)
- `docs/QUICK_REFERENCE.md` - Updated script paths
- `docs/LARGE_FILES.md` - Updated script paths

### NPX Package
- `npx-package/package.json` - Version bumped to 2.0.0, updated keywords
- `npx-package/README.md` - Updated all paths and examples
- `npx-package/bin/paddleocr-skills.js` - Updated CLI flags and skill names
- `npx-package/lib/installer.js` - Updated skill name checks
- `npx-package/lib/prompts.js` - Updated skill values and display names
- `npx-package/lib/verify.js` - Updated skill name checks

### Skill Definitions
- `skills/pp-ocrv5/SKILL.md` - Updated name and all script paths
- `skills/paddleocr-vl/SKILL.md` - Updated name and all script paths

### Templates (NPX Package)
- All files under `npx-package/templates/pp-ocrv5/`
- All files under `npx-package/templates/paddleocr-vl/`

---

## Version Impact

- **NPX Package**: `1.1.1` → `2.0.0` (Major version bump due to breaking changes)

---

## Verification

```bash
# Check no old references remain in paths/commands
grep -r "ppocrv5\|paddleocr-vl-1\.5" --include="*.md" --include="*.js" --include="*.json" --include="*.py" | grep -v "model_version" | grep -v "aligned with"
# Expected: No output (or only internal references like model_version strings)

# README commands point to new directories
grep "pp-ocrv5\|paddleocr-vl" README.md
# Expected: All paths use new names
```

---

## Notes

- The `model_version` field in API responses may still contain `paddleocr-vl-1.5` as this reflects the actual model version from the provider API, not our skill naming.
- Internal code comments mentioning alignment with "ppocrv5" conventions are acceptable as they describe the design pattern, not a path reference.
