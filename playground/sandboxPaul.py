import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

import logging
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

#OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')#'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'#= os.getenv("OPENAI_API_KEY") #os.environ.get("OPENAI_API_KEY")

from langchain.chains import create_extraction_chain

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")#, openai_api_key = OPENAI_API_KEY)



schema = {
    "properties": {
        "news_article_title": {"type": "string"},
        "news_article_summary": {"type": "string"},
    },
    "required": ["news_article_title", "news_article_summary"],
}


def extract(content: str, schema: dict):
    return create_extraction_chain(schema=schema, llm=llm).run(content)




def main():
    try:
        logger.debug("Starting HTML loader")
        # Load HTML
        loader = AsyncChromiumLoader(["https://www.wsj.com"])
        html = loader.load()
        logger.debug("HTML loaded")

        logger.debug("Starting HTML transformation")
        # Transform
        bs_transformer = BeautifulSoupTransformer()
        docs_transformed = bs_transformer.transform_documents(html, tags_to_extract=["span"])
        logger.debug("HTML transformed")

        # Print a portion of the result
        print(docs_transformed[0].page_content[0:500])

    except Exception as e:
        logger.error(f"An error occurred: {e}")


    



if __name__ == "__main__":
    main()