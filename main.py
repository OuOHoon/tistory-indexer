from tistory_indexer import TistoryIndexer
import os
from dotenv import load_dotenv
import logging


def configure_logging():
    """
    Configure logging for the application.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info("Logging configured.")


# Main entry point
if __name__ == "__main__":
    load_dotenv()
    configure_logging()

    # Load environment variables from .env file
    tistory_blog_url = os.getenv("TISTORY_BLOG_URL")
    credentials_path = os.getenv("CREDENTIALS_PATH")

    if not tistory_blog_url or not credentials_path:
        logging.exception(
            "Please set TISTORY_BLOG_URL and CREDENTIALS_PATH in your .env file.")
        exit(1)

    try:
        indexer = TistoryIndexer(
            tistory_blog_url=tistory_blog_url,
            oauth_credentials_path=credentials_path
        )
        indexer.run(1)
    except Exception as e:
        logging.exception(f"Failed to run TistoryIndexer: {e}")
        exit(1)
