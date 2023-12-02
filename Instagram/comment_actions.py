from uiautomator import device as d
import random
import re
import logging
from .utils import random_sleep
from .services import InstagramActions

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class CommentInteractions(InstagramActions):
    # ... all methods of CommentInteractions ...
