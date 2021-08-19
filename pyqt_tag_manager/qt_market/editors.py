# Import local modules.
from Qt import QtWidgets
from pyqt_tag_manager.qt_market import mixins


class Label(mixins.MixinElided, QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(Label, self).__init__(parent)


class LineEdit(mixins.MixinTextToolTip, mixins.MixinElided,
               QtWidgets.QLineEdit):
    def __init__(self, parent=None):
        super(LineEdit, self).__init__(parent)


class TextEdit(mixins.MixinElided, QtWidgets.QTextEdit):
    def __init__(self, parent=None):
        super(TextEdit, self).__init__(parent)
