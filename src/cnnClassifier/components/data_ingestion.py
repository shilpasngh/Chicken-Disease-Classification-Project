import os
import urllib.request as request
import zipfile
from cnnClassifier import logger
from cnnClassifier.utils.common import get_size
import ssl
import requests
import urllib.error as URlError
from cnnClassifier.entity.config_entity import DataIngestionConfig
from pathlib import Path



# Disable SSL verification
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

#with request.urlopen("https://google.com", context=ssl_context) as response:
 #   print(response.read())
class DataIngestion:
    
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    '''
    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            filename, headers = request.urlretrieve(
                url = self.config.source_URL,
                filename = self.config.local_data_file
            )
            logger.info(f"{filename} download! with following info: \n{headers}")
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")  
    '''

    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            try:
                response = requests.get(self.config.source_URL, 
                                        stream=True, 
                                        verify=False)  # Bypass SSL certificate verification
                
                with open(self.config.local_data_file, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192): 
                        file.write(chunk)

                logger.info(f"{self.config.local_data_file} downloaded successfully!")
                logger.info(f"Response headers: \n{response.headers}")
            except URLError as e:
                logger.error(f"Error downloading file: {e}")
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")


    def extract_zip_file(self):
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
