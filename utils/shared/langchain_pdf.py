import os

from app_log import logger
from functions import load_pdf_from_file
from langchain_google_genai import ChatGoogleGenerativeAI


def summarize(file_path , context_base = "summarize the following not less than 2000 words lec slide and transcript text" ):
    """_summary_

    Args:
        file_path (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    base_name = os.path.basename(file_path)
    pages = load_pdf_from_file(file_path=file_path)
    logger.info(f"loaded {file_path}")
    parts = file_path.split("/")

    # Assuming the folder name is the second-to-last element (one level before the filename)
    folder_name = parts[-2]
    trans_file = os.path.join(f"/home/pk/Desktop/dbms/Transcripts/{folder_name}", base_name)
    transcript = load_pdf_from_file(trans_file)
    logger.info(f"loaded {trans_file}")
    # Setup the Google Generative AI model and invoke it using a human-friendly prompt
    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    result = llm.invoke(f"{context_base}: \n {pages}: \n {transcript}")

    return result.content
