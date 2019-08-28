# testlog.py
# Leaning python, variations on logging
#
# 2019-08-28    PV

import logging
logging.basicConfig(filename='testlog.txt', level=logging.DEBUG)

# Root logger
logging.debug('Hello')

#import pdb; pdb.set_trace()
#breakpoint()

# Per module
logger = logging.getLogger(__name__)
logger.debug('Hello 2')
