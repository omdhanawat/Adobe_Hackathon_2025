import os
import argparse
from datetime import datetime
import time

from pdf_parser import create_document_sections
from ranker import rank_sections
from utils import load_input, save_output


def process_collection(base_path, collection_name):
    print(f"\n🚀 Processing collection: {collection_name}")
    start_time = time.time()

    collection_path = os.path.join(base_path, collection_name)
    input_path = os.path.join(collection_path, "input", "input.json")
    pdf_folder = os.path.join(collection_path, "pdfs")
    output_folder = os.path.join(collection_path, "output")
    os.makedirs(output_folder, exist_ok=True)

    input_data = load_input(input_path)
    all_sections = {}

    for doc in input_data["documents"]:
        file_path = os.path.join(pdf_folder, doc["filename"])
        if os.path.exists(file_path):
            sections = create_document_sections(file_path)
            all_sections[doc["filename"]] = sections
        else:
            print(f"❌ Missing file: {doc['filename']}")

    # Extract persona and task
    persona = input_data["persona"]["role"] if isinstance(input_data["persona"], dict) else input_data["persona"]
    task = input_data["job_to_be_done"]["task"] if isinstance(input_data["job_to_be_done"], dict) else input_data["job_to_be_done"]

    # Rank sections
    extracted, analysis = rank_sections(all_sections, persona, task)

    output_data = {
        "metadata": {
            "input_documents": [doc["filename"] for doc in input_data["documents"]],
            "persona": input_data["persona"],
            "job_to_be_done": input_data["job_to_be_done"],
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": extracted,
        "subsection_analysis": analysis
    }

    output_path = os.path.join(output_folder, "output.json")
    save_output(output_path, output_data)

    elapsed_time = round(time.time() - start_time, 2)
    print(f"✅ Output saved to: {output_path}")
    print(f"⏱️ Time taken: {elapsed_time} seconds")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--collection", type=str, help="Name of the collection to process")
    args = parser.parse_args()

    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../collections"))

    if args.collection:
        process_collection(base_path, args.collection)
    else:
        # Process all collections inside /collections/
        all_folders = [
            name for name in os.listdir(base_path)
            if os.path.isdir(os.path.join(base_path, name))
        ]
        for folder in all_folders:
            process_collection(base_path, folder)


if __name__ == "__main__":
    main()
