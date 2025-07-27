# Adobe "Connecting the Dots" Hackathon 2025 

This repository contains solutions for **Round 1a and 1b challenges** of Adobe's **Connecting the Dots Hackathon 2025**.

Each folder is a self-contained project solving a unique problem statement provided in the hackathon.

---

## 📁 Structure Overview

```
adobe-hackathon-2025/
├── adobe-round1a/                  # Round 1A — PDF Outline Extraction
│   └── README.md                   # Detailed instructions for Round 1A
│   └── app/                        # Source code (main.py, heading_extractor.py)
│   └── input/, output/, etc.
│   ├── requirements.txt            # Shared Python dependencies (if any)
|   ├── Dockerfile                  # Base Dockerfile template (challenge-specific Dockerfiles inside folders)
|
├── adobe-round1b/                  # Round 1B — Persona-based Document Intelligence
│   └── README.md                   # Detailed instructions for Round 1B
│   └── app/                        # Source code (main.py, ranker.py, pdf_parser.py)
│   └── collections/                # Input sets (documents + JSON)
│   ├── requirements.txt            # Shared Python dependencies (if any)
|   ├── Dockerfile                  # Base Dockerfile template (challenge-specific Dockerfiles inside folders)
|                   
└── README.md                   # ← You are here
```

---

## ⚙️ How to Use

Each round (1A, 1B, etc.) has:

- 📄 A dedicated `README.md` with:
  - Setup instructions
  - Docker usage
  - Sample outputs
- 📦 Self-contained Python code
- 📁 Input/output folders

> 💡 **Please read the individual `README.md` inside each round folder to get started.**

---

## 🧩 Compatibility & Constraints

- ✅ Works offline
- ✅ CPU-only (no GPU required)
- ✅ Modular & generic — not hardcoded to sample PDFs

---
