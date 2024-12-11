import pdfplumber
import csv

def parse_pdf(pdf_path, output_csv_path):
    with pdfplumber.open(pdf_path) as pdf:
        with open(output_csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        writer.writerow(row)
