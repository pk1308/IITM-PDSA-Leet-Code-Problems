import os

from shared.app_log import logger
from shared.functions import deploy_mkdocs, update_my_docs

if __name__ == "__main__":

    repo_path = os.getcwd()
    update_my_docs()
    logger.info("successful update")
    deploy_mkdocs()
    logger.info("deployed mk docs ")
