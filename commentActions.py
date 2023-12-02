from uiautomator import device as d
import random
import re
import logging
from Instagram.instagram import InstagramActions
from Instagram.utils import random_sleep

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
