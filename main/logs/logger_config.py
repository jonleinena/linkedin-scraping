import logging

# Create a logger
logger = logging.getLogger('my_logger')

# Create handlers
info_handler = logging.FileHandler('../logs/info-app.log')
info_handler.setLevel(logging.INFO)

warning_handler = logging.FileHandler('../logs/relevant-app.log')
warning_handler.setLevel(logging.WARNING)

# Create formatters and add it to handlers
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
info_handler.setFormatter(formatter)
warning_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(info_handler)
logger.addHandler(warning_handler)
