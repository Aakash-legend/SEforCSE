from bs4 import BeautifulSoup
class HTMLParser:
    def parse(self, html):
        """
        Convert raw HTML into structured content.
        """
        soup = BeautifulSoup(html, "lxml")
        # ---------- Title ----------
        title = ""
        if soup.title:
            title = soup.title.get_text(strip=True)
        # ---------- Meta Description ----------
        description = ""
        meta = soup.find("meta", attrs={"name": "description"})
        if meta and meta.get("content"):
            description = meta["content"]
        # ---------- Headings ----------
        headings = []
        for tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            for h in soup.find_all(tag):
                text = h.get_text(" ", strip=True)
                if text:
                    headings.append(text)
        # ---------- Paragraphs ----------
        paragraphs = []
        for p in soup.find_all("p"):
            text = p.get_text(" ", strip=True)
            if text:
                paragraphs.append(text)
        # ---------- Code Blocks ----------
        code_blocks = []
        for code in soup.find_all(["code", "pre"]):
            text = code.get_text("\n", strip=True)
            if text:
                code_blocks.append(text)
        # ---------- Complete Text ----------
        text = "\n".join(headings + paragraphs)
        return {
            "title": title,
            "description": description,
            "headings": headings,
            "paragraphs": paragraphs,
            "code_blocks": code_blocks,
            "text": text
        }