from celery import Celery
import pdfplumber
import os
import pandas as pd
import logging
import traceback


logger = logging.getLogger(__name__)

# Celery configuration
celery_app = Celery('tasks', 
    broker=os.environ.get('CELERY_BROKER_URL', 'redis://redis-server:6379/0')
)

@celery_app.task(bind=True)
def process_pdf(self, pdf_path, folder_path):

    try:
        logger.info(f"Starting PDF processing: {pdf_path}")
        logger.info(f"Folder path: {folder_path}")

        os.makedirs(folder_path, exist_ok=True)

        if not os.path.exists(pdf_path):
            logger.error(f"PDF file not found: {pdf_path}")
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        with pdfplumber.open(pdf_path) as pdf:
            logger.info(f"Opened PDF with {len(pdf.pages)} pages")
            
            tables = []
            for i, page in enumerate(pdf.pages):
                page_tables = page.extract_tables()
                logger.info(f"Page {i+1}: Found {len(page_tables)} tables")
                if page_tables:
                    tables.extend(page_tables)

        if not tables:
            logger.warning("No tables found in the PDF")
            raise ValueError("No tables found in the PDF")

        combined_data = []
        for table in tables:
            if len(table) > 1:
                try:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    combined_data.append(df)
                except Exception as df_error:
                    logger.error(f"Error processing table: {df_error}")

        if not combined_data:
            logger.error("No valid table data found")
            raise ValueError("No valid table data found")

        combined_df = pd.concat(combined_data, ignore_index=True)
        
        output_csv_path = os.path.join(folder_path, 'output.csv')

        combined_df.to_csv(output_csv_path, index=False)
        logger.info(f"CSV saved to {output_csv_path}")

        return output_csv_path

    except Exception as e:
        error_message = f"Error processing PDF: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_message)

        try:
            error_path = os.path.join(folder_path, 'error.txt')
            os.makedirs(os.path.dirname(error_path), exist_ok=True)
            
            with open(error_path, 'w') as error_file:
                error_file.write(error_message)
        except Exception as write_error:
            logger.critical(f"Could not write error file: {write_error}")

        raise ValueError("Something went wrong")