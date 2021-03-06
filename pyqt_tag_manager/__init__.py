# Import built-in modules.
import logging


# Initialize root logger.
def _init_logger():
    _logger = logging.getLogger(__name__)

    _logger.propagate = False
    _logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '{lvl} [{name}] [{file}:{line}] - {msg}'.format(
            lvl='%(levelname)-8s',
            name='%(name)s',
            file='%(filename)s',
            line='%(lineno)d',
            msg='%(message)s')
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    _logger.addHandler(handler)

    return _logger


logger = _init_logger()


# If Qt.py is available, use it.
# Otherwise, use the vendored version included in this package.
try:
    from Qt import QtCore
    from Qt import QtGui
    from Qt import QtWidgets
    from Qt import QtSql
    print('Using Qt.py.')

except ImportError:
    from PySide2 import QtCore
    from PySide2 import QtGui
    from PySide2 import QtWidgets

    logger.warning('Unable to import package Qt.py, using PySide2 instead.')
    print('Using Pyside2')


__author__ = 'Nevolutionize'
__version__ = '0.1.0'
__all__ = [
]
