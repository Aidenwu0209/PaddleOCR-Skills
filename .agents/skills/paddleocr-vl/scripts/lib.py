"""
PaddleOCR-VL Skill Library

Simple document parsing API wrapper for PaddleOCR vision-language model.
"""

import base64
import logging
import os
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse, unquote

import httpx

logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

DEFAULT_TIMEOUT = 60  # seconds (VL takes longer)
DEFAULT_MAX_FILE_SIZE_MB = 20
API_GUIDE_URL = "https://paddleocr.com"


# =============================================================================
# Environment
# =============================================================================

_env_loaded = False


def _load_env():
    """Load .env file if available."""
    global _env_loaded
    if _env_loaded:
        return
    try:
        from dotenv import load_dotenv
        env_file = Path(__file__).parent.parent.parent / ".env"
        if env_file.exists():
            load_dotenv(env_file)
    except ImportError:
        pass
    _env_loaded = True


def _get_env(key: str, *fallback_keys: str) -> str:
    """Get environment variable with fallback keys."""
    _load_env()
    value = os.getenv(key, "").strip()
    if value:
        return value
    for fallback in fallback_keys:
        value = os.getenv(fallback, "").strip()
        if value:
            logger.debug(f"Using fallback env var: {fallback}")
            return value
    return ""


def get_config() -> tuple[str, str]:
    """
    Get API URL and token from environment.

    Returns:
        tuple of (api_url, token)

    Raises:
        ValueError: If not configured
    """
    api_url = _get_env("PADDLEOCR_VL_API_URL", "VL_API_URL")
    token = _get_env("PADDLEOCR_VL_ACCESS_TOKEN", "PADDLEOCR_VL_TOKEN", "VL_TOKEN")

    if not api_url:
        raise ValueError(f"PADDLEOCR_VL_API_URL not configured. Get your API at: {API_GUIDE_URL}")
    if not token:
        raise ValueError(f"PADDLEOCR_VL_ACCESS_TOKEN not configured. Get your API at: {API_GUIDE_URL}")

    # Normalize URL
    if not api_url.startswith(("http://", "https://")):
        api_url = f"https://{api_url}"

    return api_url, token


# =============================================================================
# File Utilities
# =============================================================================

def _detect_file_type(path_or_url: str) -> int:
    """Detect file type: 0=PDF, 1=Image."""
    path = path_or_url.lower()
    if path.startswith(("http://", "https://")):
        path = unquote(urlparse(path).path)

    if path.endswith(".pdf"):
        return 0
    elif path.endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".webp")):
        return 1
    else:
        raise ValueError(f"Unsupported file format: {path_or_url}")


def _load_file_as_base64(file_path: str) -> str:
    """Load local file and encode as base64."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Check file size
    max_size_mb = int(os.getenv("PADDLEOCR_VL_MAX_FILE_SIZE_MB", str(DEFAULT_MAX_FILE_SIZE_MB)))
    file_size_mb = path.stat().st_size / 1024 / 1024
    if file_size_mb > max_size_mb:
        raise ValueError(f"File too large: {file_size_mb:.1f}MB (max {max_size_mb}MB). Use file_url instead.")

    return base64.b64encode(path.read_bytes()).decode("utf-8")


# =============================================================================
# API Request
# =============================================================================

def _make_api_request(api_url: str, token: str, params: dict) -> dict:
    """
    Make PaddleOCR-VL API request.

    Args:
        api_url: API endpoint URL
        token: Access token
        params: Request parameters

    Returns:
        API response dict

    Raises:
        RuntimeError: On API errors
    """
    headers = {
        "Authorization": f"token {token}",
        "Content-Type": "application/json",
    }

    timeout = float(os.getenv("PADDLEOCR_VL_TIMEOUT", str(DEFAULT_TIMEOUT)))

    try:
        with httpx.Client(timeout=timeout) as client:
            resp = client.post(api_url, json=params, headers=headers)
    except httpx.TimeoutException:
        raise RuntimeError(f"API request timed out after {timeout}s")
    except httpx.RequestError as e:
        raise RuntimeError(f"API request failed: {e}")

    # Handle HTTP errors
    if resp.status_code == 401 or resp.status_code == 403:
        raise RuntimeError(f"Authentication failed ({resp.status_code}). Check your token.")
    elif resp.status_code == 429:
        raise RuntimeError("API rate limit exceeded (429)")
    elif resp.status_code >= 500:
        raise RuntimeError(f"API service error ({resp.status_code})")
    elif resp.status_code != 200:
        raise RuntimeError(f"API error ({resp.status_code}): {resp.text[:200]}")

    # Parse response
    try:
        result = resp.json()
    except Exception:
        raise RuntimeError(f"Invalid JSON response: {resp.text[:200]}")

    # Check API-level error
    if result.get("errorCode", 0) != 0:
        raise RuntimeError(f"API error: {result.get('errorMsg', 'Unknown error')}")

    return result


# =============================================================================
# Main API
# =============================================================================

def parse_document(
    file_path: Optional[str] = None,
    file_url: Optional[str] = None,
    **options,
) -> dict[str, Any]:
    """
    Parse document with PaddleOCR-VL.

    Args:
        file_path: Local file path
        file_url: URL to file
        **options: Additional API options

    Returns:
        {
            "ok": True,
            "text": "extracted text...",
            "result": { raw API result },
            "error": None
        }
        or on error:
        {
            "ok": False,
            "text": "",
            "result": None,
            "error": {"code": "...", "message": "..."}
        }
    """
    # Validate input
    if not file_path and not file_url:
        return _error("INPUT_ERROR", "file_path or file_url required")

    # Get config
    try:
        api_url, token = get_config()
    except ValueError as e:
        return _error("CONFIG_ERROR", str(e))

    # Build request params
    try:
        if file_url:
            params = {"file_url": file_url}
        else:
            params = {
                "file": _load_file_as_base64(file_path),
                "fileType": _detect_file_type(file_path),
            }

        params.update(options)

    except (ValueError, FileNotFoundError) as e:
        return _error("INPUT_ERROR", str(e))

    # Call API
    try:
        result = _make_api_request(api_url, token, params)
    except RuntimeError as e:
        return _error("API_ERROR", str(e))

    # Extract text
    text = _extract_text(result)

    return {
        "ok": True,
        "text": text,
        "result": result,
        "error": None,
    }


def _extract_text(result: dict) -> str:
    """Extract text from VL result."""
    # Try different possible response structures
    res = result.get("result", result)

    # Direct markdown/text field
    if "markdown" in res:
        return res["markdown"]
    if "text" in res:
        return res["text"]
    if "full_text" in res:
        return res["full_text"]

    # Layout regions
    layout = res.get("layout", {})
    regions = layout.get("regions", [])
    if regions:
        texts = [r.get("content", "") for r in regions if isinstance(r.get("content"), str)]
        return "\n\n".join(texts)

    # Fallback: convert entire result to string representation
    return str(res)


def _error(code: str, message: str) -> dict:
    """Create error response."""
    return {
        "ok": False,
        "text": "",
        "result": None,
        "error": {"code": code, "message": message},
    }
