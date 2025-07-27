from pathlib import Path
import fitz  
import re
import json
from collections import Counter
import time

class PDFOutlineBuilder:
    def __init__(self, debug=False):
        self.debug = debug

    def _get_title(self, doc):
        meta_title = doc.metadata.get("title", "").strip()
        if meta_title and len(meta_title) > 3:
            return meta_title
        try:
            first_page = doc[0]
            text_items = []
            for block in first_page.get_text("dict")["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            txt = span["text"].strip()
                            if txt:
                                text_items.append((txt, span["size"], span["bbox"][1]))
            if not text_items:
                return "Untitled Document"
            top_limit = doc[0].rect.height * 0.25
            upper_items = [t for t in text_items if t[2] < top_limit]
            if upper_items:
                max_size = max(upper_items, key=lambda x: x[1])[1]
                combined_title = " ".join(t[0] for t in upper_items if abs(t[1] - max_size) < 0.5)
                return combined_title.strip()
        except Exception as e:
            if self.debug:
                print("Title extraction failed:", e)
        return "Untitled Document"

    def _detect_body_font_size(self, doc):
        size_counter = Counter()
        for i in range(min(5, len(doc))):
            for block in doc[i].get_text("dict")["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            if span["text"].strip() and len(span["text"]) > 10:
                                size_counter[round(span["size"], 1)] += 1
        return size_counter.most_common(1)[0][0] if size_counter else 12.0

    def _classify(self, text, size, flags, body_size):
        ratio = size / body_size
        score = {"H1": 0, "H2": 0, "H3": 0}
        if ratio >= 1.5:
            score["H1"] += 3
        elif ratio >= 1.2:
            score["H2"] += 2
        elif ratio >= 1.05:
            score["H3"] += 1
        if flags & (1 << 4):  # bold
            score["H1"] += 1
            score["H2"] += 1
        if text.isupper() and len(text) < 60:
            score["H1"] += 1
        if re.match(r"^(I|II|III|IV|V|VI|VII|VIII|IX|X)[\.\s:]", text):
            score["H1"] += 2
        best = max(score, key=score.get)
        return best if score[best] >= 2 else None

    def _filter_headings(self, outline, normalized_title):
        clean = []
        seen = set()
        for item in outline:
            text = item["text"].strip()
            normalized = re.sub(r'\s+', ' ', text.lower())
            if normalized == normalized_title:
                continue
            if text in seen or len(text) < 3:
                continue
            if re.fullmatch(r'[.\-_=•●]{5,}', text):
                continue
            if re.fullmatch(r'\d{1,2}\s+[A-Z]{3,9}\s+\d{4}', text):
                continue
            if re.fullmatch(r'[A-Z0-9]{3,10}', text):
                continue
            if len(text) <= 5 and text.isupper():
                continue
            if text.lower() in {"version", "remarks", "identifier", "reference"}:
                continue
            if len(set(text.split())) < len(text.split()) / 1.5:  # too many repeats
                continue
            seen.add(text)
            clean.append(item)
        return clean

    def extract_outline(self, pdf_path: Path):
        try:
            doc = fitz.open(pdf_path)
            title = self._get_title(doc)
            normalized_title = re.sub(r'\s+', ' ', title.lower().strip())
            body_font = self._detect_body_font_size(doc)
            headings = []

            for page_num, page in enumerate(doc):
                blocks = page.get_text("dict")["blocks"]
                for block in blocks:
                    if "lines" not in block:
                        continue
                    combined_lines = []
                    temp_line = {"text": "", "size": 0, "flag": 0, "y": None}
                    for line in block["lines"]:
                        line_text = ""
                        max_size = 0
                        max_flag = 0
                        y_pos = line["bbox"][1]
                        for span in line["spans"]:
                            line_text += span["text"]
                            if span["size"] > max_size:
                                max_size = span["size"]
                                max_flag = span["flags"]
                        line_text = line_text.strip()
                        if not line_text:
                            continue
                        if temp_line["text"] and abs(y_pos - temp_line["y"]) < 12 and abs(max_size - temp_line["size"]) <= 0.6:
                            temp_line["text"] += " " + line_text
                        else:
                            if temp_line["text"]:
                                combined_lines.append(temp_line)
                            temp_line = {"text": line_text, "size": max_size, "flag": max_flag, "y": y_pos}
                    if temp_line["text"]:
                        combined_lines.append(temp_line)

                    for entry in combined_lines:
                        cleaned_text = re.sub(r'\s+', ' ', entry["text"].strip())
                        level = self._classify(cleaned_text, entry["size"], entry["flag"], body_font)
                        if level:
                            headings.append({
                                "level": level,
                                "text": cleaned_text,
                                "page": page_num + 1
                            })

            final_outline = self._filter_headings(headings, normalized_title)
            return {
                "title": title,
                "outline": final_outline
            }

        except Exception as e:
            if self.debug:
                print("Error in extract_outline:", e)
            return {
                "title": "Error Extracting Document",
                "outline": []
            }

    def process_all(self, input_dir: Path, output_dir: Path):
        output_dir.mkdir(parents=True, exist_ok=True)
        pdf_files = list(input_dir.glob("*.pdf"))
        if not pdf_files:
            print(f"No PDFs found in {input_dir}")
            return

        for pdf_file in pdf_files:
            print(f"Processing: {pdf_file.name}")
            start = time.time()
            result = self.extract_outline(pdf_file)
            output_file = output_dir / (pdf_file.stem + ".json")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"✅ Done: {pdf_file.name} ({len(result['outline'])} headings) [{time.time() - start:.2f}s]")
