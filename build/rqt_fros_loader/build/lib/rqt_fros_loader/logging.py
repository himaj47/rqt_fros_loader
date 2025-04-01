from rclpy.logging import get_logger

logger = get_logger(__package__)

debug = logger.debug
error = logger.error
fatal = logger.fatal
info = logger.info
warn = logger.warning