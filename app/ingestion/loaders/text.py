import logfire


def parse_text(file_path: str):
    """
    Parse plain text files.

    Returns:
    [
        {
            "page": None,
            "section": None,
            "text": "..."
        }
    ]
    """

    with logfire.span(
        "📄 Text Parsing",
        filename=file_path,
    ):

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8",
                errors="ignore",
            ) as f:

                text = f.read().strip()

            if not text:

                logfire.warning(
                    f"No text extracted from {file_path}"
                )

                return []

            documents = [
                {
                    "page": None,
                    "section": None,
                    "text": text,
                }
            ]

            logfire.info(
                "Text parsed",
                characters=len(text),
            )

            return documents

        except Exception as e:
            logfire.error(f"❌ Text Parse Failed: {e}")
            raise