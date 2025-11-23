import sys
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import pipeline stages
from extract import extract
from transform import transform
from load_data import load_to_supabase

def run_pipeline(skip_extract=False, skip_transform=False, skip_load=False):
    """
    Execute the complete ETL pipeline in sequence.
    
    Args:
        skip_extract (bool): Skip the extract stage
        skip_transform (bool): Skip the transform stage
        skip_load (bool): Skip the load stage
    """
    try:
        # Stage 1: Extract data from PDF files
        if not skip_extract:
            logger.info("=" * 60)
            logger.info("Extracting data from PDF files")
            logger.info("=" * 60)
            extract()
            logger.info("Extract completed")
            logger.info("")
        
        # Stage 2: Transform and clean data
        if not skip_transform:
            logger.info("=" * 60)
            logger.info("Cleaning and transforming data")
            logger.info("=" * 60)
            transform()
            logger.info("Transform completed")
            logger.info("")
        
        # Stage 3: Load data to database
        if not skip_load:
            logger.info("=" * 60)
            logger.info(" Loading data to database")
            logger.info("=" * 60)
            load_to_supabase()
            logger.info("Load completed")
            logger.info("")
        
        # Pipeline finished successfully
        logger.info("=" * 60)
        logger.info("Pipeline finished successfully")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Pipeline failed with error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Run the complete pipeline
    run_pipeline()