import logging
import os

# Convenience class for shared methods

# absolute path helps portability when reading properties files
absolute_path = os.path.dirname(os.path.abspath(__file__))


# Convert values to string or None if blank, supports int, boolean an
def converttostring(str):
    if type(str) is int:
        return "{}".format(str)
    if type(str) is bool:
        return "{}".format(str)
    if str is None:
        return 'None'
    if str == "":
        return 'None'
    return str


# Get the API key from the environment
def getgithubapikey():
    return os.environ['INPUT_GITHUBAPIKEY']


logger = logging.getLogger('gha-logger')
logger.setLevel(logging.DEBUG)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)


def logaudititem(msg):
    logger.debug(msg)


LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(format='%(asctime)s - %(levelname)s - {%(pathname)s:%(lineno)d} - %(message)s', level=LOGLEVEL)


def logitem(msg):
    logging.error(LOGLEVEL)
    if LOGLEVEL == 'DEBUG':
        logging.debug(msg)
    elif LOGLEVEL == 'INFO':
        logging.info(msg)
    elif LOGLEVEL == 'WARNING':
        logging.warning(msg)
    elif LOGLEVEL == 'ERROR':
        logging.error(msg)
    else:
        logging.critical(msg)
