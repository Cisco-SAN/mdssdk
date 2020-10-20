import logging
import random

log = logging.getLogger(__name__)

reserved_id = [4079, 4094]
boundary_id = [0, 4095]


# No need to have end=4094 as there are some inbetween vsans reserved for fport-channel-trunk
def get_random_id(start=2, end=400):
    return random.randint(start, end)
