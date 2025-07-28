# Adobe "Connecting the Dots" – Round 1B Challenge

## 🔍 Challenge Description

This project is a solution to **Round 1B of Adobe's "Connecting the Dots" Hackathon**, where the task is to build a **persona-aware document intelligence system**.

Given:
- A set of PDFs (e.g., travel guides),
- A user persona (e.g., Travel Planner),
- And a specific task (e.g., Plan a 4-day trip for 10 college friends),

## 🧭 Approach

The solution follows a three-stage pipeline:

### 1. Section Extraction
We parse all PDF documents using `PyMuPDF` to extract readable text blocks. Each page is scanned, and blocks with meaningful length are captured along with their page number. This forms a pool of candidate sections.

### 2. Semantic Ranking
Each extracted section is embedded using the `all-MiniLM-L6-v2` model from `sentence-transformers`. We also embed the query string formed by combining the persona and the task. Then we compute cosine similarity between the query and all section embeddings to select the most relevant ones.

### 3. Output Structuring
The top 5 most relevant sections (each from a different document) are selected. For each section:
- The **title** is cleaned and truncated to form a readable heading.
- The **content** is refined to represent meaningful and informative insights for the given persona/task.

All output is structured in a standardized `output.json` format with timestamps and ranking metadata.

---

## 📁 Folder Structure

```
adobe-round1b/
│
├── app/                       # Main source code
│   ├── main.py                # CLI interface
│   ├── ranker.py              # Ranks sections using semantic similarity
│   ├── pdf_parser.py          # Extracts text and sections from PDFs
│   ├── utils.py               # JSON IO helpers
│
├── collections/              # One or more input collections
│   ├── collection1/
│   │   ├── input/input.json
│   │   ├── pdfs/*.pdf
│   │   └── output/output.json
│   └── collection2/
│       ├── ...
│
├── README.md                 # This file
└── requirements.txt          # Python dependencies
└── Dockerfile 
```

---

## ⚙️ Requirements

- Python 3.10+
- pip (Python package manager)
- `poppler-utils` (for PDF parsing – required for `PyMuPDF`)
- (Optional) Docker

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 🐳 Docker Instructions 

### Step 1: Build Docker image

From root directory (`adobe-round1b/`):

```bash
docker build -t adobe-challenge .
```

### Step 2: Run a collection

```bash
docker run -v %cd%/collections:/app/collections adobe-challenge --collection collection1
```

---

## 🚀 Usage (via CLI)

### ✅ Process a single collection
```bash
python app/main.py --collection collection1
```

### ✅ Process all collections in `/collections/`
```bash
python app/main.py
```

✅ The results are saved to:
```
collections/<collection_name>/output/output.json
```

Each run also prints the **execution time** per collection.

---

## 📦 Output Format

The output JSON includes:

```json
{
  "metadata": {
    "input_documents": [...],
    "persona": {...},
    "job_to_be_done": {...},
    "processing_timestamp": "2025-07-27T14:22:10.234Z"
  },
  "extracted_sections": [
    {
      "document": "file.pdf",
      "section_title": "Title",
      "importance_rank": 1,
      "page_number": 3
    }
  ],
  "subsection_analysis": [
    {
      "document": "file.pdf",
      "refined_text": "Important content...",
      "page_number": 3
    }
  ]
}
```

---

## 🧠 Technology Stack

- Python 3.10
- [PyMuPDF (`fitz`)](https://pymupdf.readthedocs.io/en/latest/) – PDF parsing
- [Sentence Transformers](https://www.sbert.net/) – Semantic ranking
- argparse – CLI
- Docker – Containerization

---

## 📌 Notes

- The system **auto-merges multiline headings** and excludes noisy fragments.
- Works across **any PDF documents** and **any persona/task combination**.
- Output is deterministic and reproducible.

---