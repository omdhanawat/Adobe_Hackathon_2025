# 📄 PDF Structured Outline Extraction Tool

⏱ Efficient | 📄 Accurate | 🐳 Dockerized | 🧩 Offline | ✅ CPU-only

---

## 🧠 Overview

This project is a solution to **Round 1A of Adobe's "Connecting the Dots" Hackathon**, where the task is to extracts a **structured outline** from PDF documents with:

- 📌 Document **title**
- 📂 Section Headings: Hierarchically classified as **H1**, **H2**, **H3**
- 📄 **Page number** for each heading

Output is a JSON file in the required Adobe challenge format.

---
"""
## 🧭 Approach

This tool works in three intelligent stages:

### 1. Title Extraction
It first tries to extract the document title from the PDF metadata. If unavailable or too short, it intelligently scans the top portion of the first page for the largest and most prominent text block(s), merging lines where needed to generate a meaningful document title.

### 2. Heading Detection & Classification
Each page is scanned for text spans, which are grouped into lines and then merged if they belong to the same heading (based on vertical proximity and font size similarity). The font size of the main body text is statistically inferred to serve as a baseline. Using this:
- **Font size ratios**, 
- **Boldness flags**, 
- **ALL CAPS usage**, and 
- **Roman numeral prefixes**

...are used to classify headings into `H1`, `H2`, or `H3`.

### 3. Noise Filtering
The detected headings are passed through a noise filter to exclude:
- Short or generic words,
- Decorative or repeated elements (e.g., lines of dots),
- Page headers/footers,
- Common metadata tokens like "version", "remarks", etc.

Finally, the structured outline is saved in a clean, standardized JSON format.
"""

## 🚀 Features

- Extracts title from metadata or top of the first page
- Identifies headings using:
  - Font size relative to body text
  - Boldness and uppercase patterns
- Filters out noise and irrelevant text
- Fully **offline** and **CPU-only**
- Compliant with `linux/amd64` architecture
- Executes under **10 seconds** for 50-page PDFs
- Designed to work **modularly** on any PDF (not hardcoded)

---

## 📁 Project Structure

```
Adobe_Hackathon
├─adobe-round1a
| ├── app/
| │   ├── heading_extractor.py      # Core logic for title and headings extraction
| │   └── main.py                   # Entry script to process PDFs from input/ and generate JSON
| ├── input/                        # Place PDF files here
| |   ├── Pdfs
| ├── output/                       # Output JSON files
| |   ├──output.json
| ├── Dockerfile                    # Docker container definition
| ├── requirements.txt              # Python dependencies
| └── README.md                     # This file
```

---

## ⚙️ Setup & Usage

### 1. Prerequisites
- Docker installed on your machine
- PDF files (≤ 50 pages each) placed in the `input/` directory

### 2. Build the Docker Image

```bash
docker build --platform linux/amd64 -t adobe-outline-round1 .
```

### 3. Run the Container

```bash
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  adobe-outline-round1
```

✅ This processes all PDFs in `input/` and generates JSON in `output/`.

---

## 📤 Sample Output Format

```json
{
  "title": "Document Title",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "Background", "page": 2 },
    { "level": "H3", "text": "Subtopic Details", "page": 3 }
  ]
}
```

---

## 📌 Compliance with Hackathon Constraints

- ✅ Offline execution: No web/API calls
- ✅ Platform: `linux/amd64`
- ✅ CPU-only, model size ≤ 200MB
- ✅ Runtime ≤ 10 seconds for 50-page documents
- ✅ Generic & modular: works across various PDFs

---

## 🧰 Dependencies

- Python 3.10
- PyMuPDF (`fitz`)

### `requirements.txt`

```
pymupdf==1.22.3
```
