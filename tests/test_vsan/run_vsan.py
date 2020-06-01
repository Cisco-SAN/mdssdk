import logging
import unittest

# Change root logger level from WARNING (default) to NOTSET in order for all messages to be delegated.
logging.getLogger().setLevel(logging.NOTSET)
logFormatter = logging.Formatter("[%(asctime)s] [%(module)-14.14s] [%(levelname)-5.5s] %(message)s")
# Add stdout handler, with level INFO
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logFormatter)
logging.getLogger().addHandler(console)

# Add file rotating handler, with level DEBUG
fileHandler = logging.FileHandler("test.log")
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(logFormatter)
logging.getLogger().addHandler(fileHandler)

log = logging.getLogger(__name__)

log.info("Running tests...")

suite = unittest.TestLoader().discover('tests.test_vsan', 'test_vsan*.py')
unittest.TextTestRunner(verbosity=2, failfast=True).run(suite)
