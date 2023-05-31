__version__ = "2.0.9"
__app_name__: str = "NSSurge CLI"

try:
    from logging_utils_tddschn import get_logger

    logger, _ = get_logger(__app_name__)
except:
    import logging
    from logging import NullHandler

    logger = logging.getLogger(__app_name__)
    logger.addHandler(NullHandler())
