import json
from pathlib import Path 

all_files_path = Path.home() /'Downloads\PDFServicesSDK-PythonSamples\\adobe-dc-pdf-services-sdk-python\output\ExtractTextTableInfoWithFiguresTablesRenditionsFromPDF'

for parsed_paper_json in all_files_path.glob('**/structuredData.json'):
    single_paper = ''
    with open(str(parsed_paper_json)) as f:
        data = json.load(f)

        for 
    
    
