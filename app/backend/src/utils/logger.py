import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

def get_logger(module_name: str):
    setup_logging()
    return logging.getLogger(module_name)
