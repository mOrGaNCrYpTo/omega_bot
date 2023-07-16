import logging

def setup_logger(name="TradeMonkey_Logger", log_file="trade_monkey.log", level=logging.DEBUG):
    """
    Set up a logger for application debug and runtime info.

    Parameters:
    name (str): The name of the logger
    log_file (str): The name of the log file
    level (logging.level): The logging level (e.g., logging.DEBUG, logging.INFO, etc.)
    
    logger = setup_logger()
    
    logger.debug("This is a debug message.")
    logger.info("This is an informational message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")
    
    Returns:
    logger: a logger instance
    """
    # Set up the logger
    logger = logging.getLogger(name) 
    logger.setLevel(level) 

    # Create a file handler
    handler = logging.FileHandler(log_file) 

    # Create a logging format
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")) 

    # Add the handler to the logger
    logger.addHandler(handler)
    
    return logger
