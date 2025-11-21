from autox.autox_logger import logger
from autox.utilities.common_utils import common_util


class TestLogging:
    def test_logger_1(self):
        common_util()
        logger.debug("Test Run 1")
        logger.debug("Test Run 1")