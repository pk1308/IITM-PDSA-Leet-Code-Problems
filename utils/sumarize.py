import os
import sys

from shared.app_log import logger
from shared.functions import ( create_md)

if __name__ == "__main__":

    repo_path = os.getcwd()
    print(sys.argv[1])
    path = sys.argv[1]
    logger.info("converting files to PDF to MD ")
    for  file in os.listdir(path):
        file_path = os.path.join(path, file)
        to_covert = input(f" covert {file_path} : ")
        if to_covert == "y":
            status = create_md(files_to_create=[file_path])
            logger.info(f"converted files to pdf to md  status ; {status} ")

