import logging
import sys

# Global configuration
logging.basicConfig(level = logging.INFO, format='%(asctime)s - %(message)s', stream = sys.stdout)
logger = logging.getLogger()