import logfire
from pypdf import PdfReader


def parse_pdf(file_path: str) -> list[dict]:
    """
    Extract text from a PDF locally using pypdf.
    Falls back to pdfplumber for pages that yield no text (e.g. image-heavy pages).
    """
    with logfire.span("📄 PDF Parsing (local)", filename=file_path):
        try:
            reader = PdfReader(file_path)
            total_pages = len(reader.pages)
            logfire.info(f"PDF has {total_pages} pages.")

            pages_data: list[dict] = []
            blank_pages: list[int] = []

            # for i, page in enumerate(reader.pages):
            #     text = page.extract_text() or ""
            #     if text.strip():
            #         text_parts.append(text)
            #     else:
            #         blank_pages.append(i + 1)
            for i, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ""
                if text.strip():
                    pages_data.append(
                        {
                            "page": i,
                            "section": f"Page {i}",
                            "text": text.strip(),
                        }
                    )

                else:
                    blank_pages.append(i)

            # Fallback: use pdfplumber for any pages pypdf returned blank
            if blank_pages:
                logfire.info(
                    f"pypdf returned blank on pages {blank_pages} — retrying with pdfplumber."
                )
                try:
                    import pdfplumber

                    with pdfplumber.open(file_path) as pdf:
                        for page_num in blank_pages:
                            page = pdf.pages[page_num - 1]
                            fallback_text = page.extract_text() or ""
                            if fallback_text.strip():
                                # text_parts.append(fallback_text)
                                pages_data.append(
                                    {
                                        "page": page_num,
                                        "section": f"Page {page_num}",
                                        "text": fallback_text.strip(),
                                    }
                                )
                                # pages_data.sort(key=lambda x: x["page"])
                except Exception as plumber_err:
                    logfire.warning(f"pdfplumber fallback failed: {plumber_err}")

            pages_data.sort(key=lambda x: x["page"])
            # full_text = "\n".join(text_parts)
            total_chars = sum(len(page["text"]) for page in pages_data)

            # if not full_text.strip():
            if not pages_data:
                logfire.warning(
                    f"No text extracted from {file_path}. File may be fully image-based."
                )
            else:
                # logfire.info(f"Extracted {len(full_text)} characters from {file_path}.")
                logfire.info(
                    f"Extracted {total_chars} characters "
                    f"from {len(pages_data)} pages."
                )

            # return full_text
            return pages_data

        except Exception as e:
            logfire.error(f"❌ PDF Parse Failed for {file_path}: {e}")
            raise
