from heading_extractor import PDFOutlineBuilder
from pathlib import Path

def main():
    # Detect Docker-style mounted folders (for compatibility)
    docker_input = Path("/app/input")
    docker_output = Path("/app/output")

    if docker_input.exists() and docker_output.exists():
        input_folder = docker_input
        output_folder = docker_output
    else:
        # Fallback: input/output are one level up from /app/
        base_dir = Path(__file__).resolve().parent.parent
        input_folder = base_dir / "input"
        output_folder = base_dir / "output"

    builder = PDFOutlineBuilder()
    builder.process_all(input_folder, output_folder)

if __name__ == "__main__":
    main()
