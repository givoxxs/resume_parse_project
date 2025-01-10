import logging
import os

def setup_logger():
    logger = logging.getLogger("document_processing")
    logger.setLevel(logging.DEBUG)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    
     # Tạo thư mục logs nếu chưa tồn tại
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # File handler
    fh = logging.FileHandler(os.path.join(log_dir, "app.log"), mode='a')
    fh.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    
    logger.addHandler(ch)
    logger.addHandler(fh)
    
    return logger

logger = setup_logger()