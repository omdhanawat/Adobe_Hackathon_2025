import heapq
from sentence_transformers import SentenceTransformer, util
from tqdm import tqdm

model = SentenceTransformer("all-MiniLM-L6-v2")  # Fast and lightweight


def clean_title(text):
    lines = text.strip().split("\n")
    for line in lines:
        line = line.strip(" •:-—\t")
        if line and len(line.split()) > 2:
            return line[:100]
    return lines[0][:100] if lines else "Untitled Section"


def rank_sections(all_sections, persona, task):
    print("[INFO] Ranking sections based on semantic similarity...")

    query = f"{persona.strip()} - {task.strip()}"
    query_embedding = model.encode(query, convert_to_tensor=True)

    # Flatten all sections into a list
    flat_sections = []
    for doc_name, sections in all_sections.items():
        for section in sections:
            flat_sections.append({
                "document": doc_name,
                "text": section["text"],
                "page_number": section["page_number"]
            })

    # Batch encode all texts
    texts = [s["text"] for s in flat_sections]
    embeddings = model.encode(texts, batch_size=32, convert_to_tensor=True, show_progress_bar=True)

    # Compute scores
    top_heap = []
    seen_docs = set()

    for i, emb in enumerate(embeddings):
        score = util.cos_sim(query_embedding, emb).item()
        doc = flat_sections[i]["document"]
        if doc not in seen_docs:
            heapq.heappush(top_heap, (-score, {
                "document": doc,
                "section_title": clean_title(flat_sections[i]["text"]),
                "importance_score": score,
                "page_number": flat_sections[i]["page_number"],
                "refined_text": flat_sections[i]["text"]
            }))
            seen_docs.add(doc)

    # Get top 5 from different documents
    top_sections = []
    while top_heap and len(top_sections) < 5:
        _, sec = heapq.heappop(top_heap)
        sec["importance_rank"] = len(top_sections) + 1
        top_sections.append(sec)

    extracted = [
        {
            "document": sec["document"],
            "section_title": sec["section_title"],
            "importance_rank": sec["importance_rank"],
            "page_number": sec["page_number"],
        }
        for sec in top_sections
    ]

    analysis = [
        {
            "document": sec["document"],
            "refined_text": sec["refined_text"],
            "page_number": sec["page_number"],
        }
        for sec in top_sections
    ]

    return extracted, analysis
