import logging

import coloredlogs


class CustomFormatter(logging.Formatter):
    fmt = "[%(asctime)s] - %(levelname)s - %(name)s - %(message)s (%(filename)s:%(lineno)d)"

    def format(self, record):
        formatter = logging.Formatter(self.fmt)
        return formatter.format(record)


def init_logger():
    coloredlogs.install()

    logger = logging.getLogger("api")
    logger.setLevel(logging.DEBUG)

    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)

    sh.setFormatter(CustomFormatter())

    logger.addHandler(sh)
