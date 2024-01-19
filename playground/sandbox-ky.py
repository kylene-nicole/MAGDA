import os
import logging
import pprint
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain.chains import create_extraction_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", openai_api_key=os.getenv("OPENAI_API_KEY"))

schema = {
    "properties": {
        "news_article_title": {"type": "string"},
        "news_article_summary": {"type": "string"},
    },
    "required": ["news_article_title", "news_article_summary"],
}

def extract(content: str, schema: dict):
    return create_extraction_chain(schema=schema, llm=llm).run(content)

def scrape_with_playwright(urls, schema):
    loader = AsyncChromiumLoader(urls)
    docs = loader.load()
    if not docs:
        logger.error("Failed to load documents.")
        return None
    
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(
        docs, tags_to_extract=["span"]
    )
    print("Extracting content with LLM")

    # Grab the first 1000 tokens of the site
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000, chunk_overlap=0
    )
    splits = splitter.split_documents(docs_transformed)
    if not splits:
        logger.error("No content was split. Please check the input content.")
        return None
    
    extracted_content = extract(schema=schema, content=splits[0].page_content)
    pprint.pprint(extracted_content)
    return extracted_content


def main():
    try:
        logger.debug("Starting HTML loader")
        # Load HTML
        urls = ["https://en.wikipedia.org/wiki/History_of_radar"]
        extracted_content = scrape_with_playwright(urls, schema=schema)

        if extracted_content:
            logger.debug("Extracted Content:")
            pprint.pprint(extracted_content)
        else:
            logger.error("No extracted content available.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()