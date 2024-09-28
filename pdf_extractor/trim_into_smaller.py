from PyPDF2 import PdfWriter, PdfReader
from pathlib import Path

NUM_PAGES = 8
paper_path = Path.home() / "Downloads\CVPR2020_FULL\CVPR 2020"
output_path = Path(paper_path.parent / 'trimmed_papers')
output_path.mkdir(exist_ok=True)

for f in paper_path.glob("*.pdf"):
    inputpdf = PdfReader(open(f, "rb"))
    n_pages = len(inputpdf.pages)

    output = PdfWriter()
    for i in range(NUM_PAGES):
        if i < n_pages:
            output.add_page(inputpdf.pages[i])

    with open(output_path/f"{f.stem}_trimmed.pdf", "wb") as outputStream:
        output.write(outputStream)