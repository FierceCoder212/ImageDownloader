import base64
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from Helpers.GoogleDriveHelper import GoogleDriverHelper
from Helpers.SqlLiteHelper import SQLiteHelper

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('app.log'),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)

google_drive_helper = GoogleDriverHelper('John Dheere Images')
db_file = r'C:\Workspace\JohnDeereScraper\Images.db'
num_threads = 10
print('Fetching Total Records...')
total_count = SQLiteHelper(db_file).fetch_total_records()
print(f'Total Records Fetched {total_count}...')
page_size = total_count // num_threads
print(f'Page Size {page_size}')


def process_page(thread_index):
    """ Processes a specific page of records. """
    offset = thread_index * page_size
    print(f'Starting Thread : {thread_index} Ranging : {page_size} - {offset}')
    sql_lite_helper = SQLiteHelper(db_file)
    for section_diagram, base_64_img in sql_lite_helper.fetch_records_by_page(page_size=page_size, offset=offset):
        try:
            base_64_img = base_64_img.replace('data:image/PNG;base64,', '')
            image_data = base64.b64decode(base_64_img)

            google_drive_helper.upload_file_from_content(file_bytes=image_data, file_name=section_diagram)
            print(f'Uploaded {section_diagram} to Google Drive.')

            if os.path.exists(section_diagram):
                os.remove(section_diagram)
        except Exception as ex:
            logger.error(f"Error processing {section_diagram}: {ex}")


# helper.save_prev_drive_files_on_folder()
with ThreadPoolExecutor(max_workers=num_threads) as executor:
    futures = [executor.submit(process_page, i) for i in range(num_threads)]

    for future in as_completed(futures):
        try:
            future.result()
        except Exception as e:
            logger.error(f"An error occurred during processing: {e}")

print("All records have been uploaded to Google Drive.")
