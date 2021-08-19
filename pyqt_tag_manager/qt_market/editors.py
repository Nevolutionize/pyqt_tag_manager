# Import local modules.
from Qt import QtWidgets
from pyqt_tag_manager.qt_market import mixins


class Label(mixins.MixinElided, QtWidgets.QLabel):
    """Custom QLabel with text elision."""
    def __init__(self, parent=None):
        super(Label, self).__init__(parent)


class LineEdit(mixins.MixinTextToolTip, mixins.MixinElided,
               QtWidgets.QLineEdit):
    """Custom QLineEdit with text elision and tool tip display of text
    values. """
    def __init__(self, parent=None):
        super(LineEdit, self).__init__(parent)


class TextEdit(mixins.MixinElided, QtWidgets.QTextEdit):
    """Custom QTextEdit with elision."""
    def __init__(self, parent=None):
        super(TextEdit, self).__init__(parent)
