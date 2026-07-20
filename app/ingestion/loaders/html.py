import logfire
from bs4 import BeautifulSoup


def parse_html(file_path: str):
    """
    Parse HTML while preserving section structure.

    Returns:
    [
        {
            "page": None,
            "section": "...",
            "text": "..."
        }
    ]
    """

    with logfire.span("📄 HTML Parsing", filename=file_path):

        try:
            with open(
                file_path,
                "r",
                encoding="utf-8",
                errors="ignore",
            ) as f:
                content = f.read()

            soup = BeautifulSoup(content, "html.parser")

            # Remove junk
            for tag in soup(["script", "style", "meta", "noscript"]):
                tag.decompose()

            documents = []

            current_section = "Introduction"
            current_text = []

            # Walk through headings and paragraphs
            for element in soup.find_all(
                [
                    "h1",
                    "h2",
                    "h3",
                    "h4",
                    "h5",
                    "h6",
                    "p",
                    "li",
                    "pre",
                    "code",
                ]
            ):

                if element.name.startswith("h"):

                    # Save previous section
                    if current_text:

                        documents.append(
                            {
                                "page": None,
                                "section": current_section,
                                "text": "\n".join(current_text).strip(),
                            }
                        )

                        current_text = []

                    current_section = element.get_text(
                        " ",
                        strip=True,
                    )

                else:

                    text = element.get_text(
                        " ",
                        strip=True,
                    )

                    if text:
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

            logfire.info(
                "HTML parsed",
                sections=len(documents),
            )

            return documents

        except Exception as e:
            logfire.error(f"❌ HTML Parse Failed: {e}")
            raise
