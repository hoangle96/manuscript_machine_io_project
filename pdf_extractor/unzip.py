import zipfile
from pathlib import Path 

all_zip_file = Path.home() /'Downloads\PDFServicesSDK-PythonSamples\\adobe-dc-pdf-services-sdk-python\output\ExtractTextTableInfoWithFiguresTablesRenditionsFromPDF'
for zip_file in all_zip_file.glob('*.zip'):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(str(all_zip_file/zip_file.stem))