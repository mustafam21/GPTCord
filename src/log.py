import logging
import os

def setup_logger(module_name: str) -> logging.Logger:
    # create logger
    library, _, _ = module_name.partition('.py')
    logger = logging.getLogger(library)

    # specify the log file path
    grandparent_dir = os.path.abspath(__file__ + "/../../")
    log_name = 'botlogs.log'
    log_path = os.path.join(grandparent_dir, log_name)

    # set up the logger using basicConfig
    logging.basicConfig(
        filename=log_path,
        filemode='w',
        format='%(asctime)s %(levelname)-8s %(name)s -> %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )

    # add a StreamHandler to log to the console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)-8s %(name)s -> %(message)s',
        '%Y-%m-%d %H:%M:%S'
    ))
    logger.addHandler(console_handler)

    return logger
