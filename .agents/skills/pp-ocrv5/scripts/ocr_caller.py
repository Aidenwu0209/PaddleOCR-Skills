#!/usr/bin/env python3
"""
PP-OCRv5 API Caller

Simple CLI wrapper for the PP-OCRv5 OCR library.

Usage:
    python scripts/pp-ocrv5/ocr_caller.py --file-url "URL"
    python scripts/pp-ocrv5/ocr_caller.py --file-path "image.png" --pretty
"""

import argparse
import io
import json
import sys
from pathlib import Path

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add scripts dir to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from lib import ocr


def main():
    parser = argparse.ArgumentParser(
        description="PP-OCRv5 API Caller - OCR images/PDFs via PaddleOCR",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # OCR from URL
  python scripts/pp-ocrv5/ocr_caller.py --file-url "https://example.com/image.png"

  # OCR local file
  python scripts/pp-ocrv5/ocr_caller.py --file-path "./document.pdf" --pretty

  # Save result to file
  python scripts/pp-ocrv5/ocr_caller.py --file-url "URL" --output result.json

Configuration:
  Run: python scripts/pp-ocrv5/configure.py
  Or set in .env: PADDLEOCR_OCR_API_URL, PADDLEOCR_ACCESS_TOKEN
        """
    )

    # Input (mutually exclusive, required)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--file-url", help="URL to image or PDF")
    input_group.add_argument("--file-path", help="Local path to image or PDF")

    # Output options
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output"
    )
    parser.add_argument(
        "--output", "-o",
        metavar="FILE",
        help="Save result to JSON file"
    )

    args = parser.parse_args()

    # Run OCR
    result = ocr(
        file_path=args.file_path,
        file_url=args.file_url,
    )

    # Format output
    indent = 2 if args.pretty else None
    json_output = json.dumps(result, indent=indent, ensure_ascii=False)

    # Save to file or print
    if args.output:
        try:
            output_path = Path(args.output).resolve()
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json_output, encoding="utf-8")
            print(f"Result saved to: {output_path}", file=sys.stderr)
        except (PermissionError, OSError) as e:
            print(f"Error: Cannot write to {args.output}: {e}", file=sys.stderr)
            sys.exit(5)
    else:
        print(json_output)

    # Exit code based on result
    sys.exit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
