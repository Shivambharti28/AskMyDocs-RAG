import logfire

from unstructured.partition.auto import partition


def parse_office(file_path: str):
    """
    Parse DOCX/PPTX while preserving document structure.

    Returns:
    [
        {
            "page": None,
            "section": "...",
            
            "text": "..."
        }
    ]
    """

    with logfire.span(
        "📄 Office Document Parsing",
        filename=file_path,
    ):

        try:

            elements = partition(filename=file_path)

            documents = []

            current_section = "Document"
            current_text = []

            for element in elements:

                category = getattr(element, "category", "")

                text = str(element).strip()

                if not text:
                    continue

                # Title starts a new section
                if category == "Title":

                    if current_text:

                        documents.append(
                            {
                                "page": None,
                                "section": current_section,
                                "text": "\n".join(current_text).strip(),
                            }
                        )

                        current_text = []

                    current_section = text

                else:

                    current_text.append(text)

            # Save final section
            if current_text:

                documents.append(
                    {
                        "page": None,
                        "section": current_section,
                        "text": "\n".join(current_text).strip(),
                    }
                )

            total_chars = sum(
                len(doc["text"])
                for doc in documents
            )

            logfire.info(
                "Office document parsed",
                sections=len(documents),
                characters=total_chars,
            )

            return documents

        except Exception as e:
            logfire.error(f"❌ Office Parse Failed: {e}")
            raise