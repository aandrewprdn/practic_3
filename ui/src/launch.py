import logging

import coloredlogs

from main_page import demo


def init_logger():
    logger = logging.getLogger("ui")
    logger.setLevel(logging.DEBUG)

    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))

    logger.addHandler(sh)

    coloredlogs.install()


init_logger()
demo.launch(share=False, show_error=True)
