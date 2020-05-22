import logging
import unittest

logging.basicConfig(filename='test_switch.log', filemode='w', level=logging.DEBUG,
                    format="[%(asctime)s] [%(module)-14.14s] [%(levelname)-5.5s] %(message)s")

logging.info("Running tests...")

import sys	

sys.stdout = open('test_switch_output.txt', 'wt')

suite = unittest.TestLoader().discover('tests.test_switch', 'test_switch*.py')
unittest.TextTestRunner(verbosity=2, failfast=True).run(suite)
