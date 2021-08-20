"""This module contains Mixin classes that extend the functionality of the
existing Qt Widgets.

Usage:
    It is a PySide2 requirement that QObject must be the first inheritance
    of multi-inheritance classes.

    >>> class MyLineEdit(MixinElided, QtWidgets.QLineEdit):
    >>>     def __init__(self, parent=None):
    >>>         super(MyLineEdit, self).__init__(parent)

"""
# Import local modules.
from pyqt_tag_manager import QtCore
from pyqt_tag_manager import QtGui
from pyqt_tag_manager import QtWidgets


class MixinElided(object):
    """Adds text elision parameters and functionality, when used with text
    widgets.

    Notes:
        When checking for attrs, use...
            `hasattr(super(MixinElided, self), 'attr')`
        instead of...
            `hasattr(self, 'attr')`
        otherwise, PySide2 crashes when a widget uses multiple inheritances.

        I think this issue and other multiple inheritance issues stem from
        using QObject as base for mixin.
        It appears to be resolved when using python object instead.

    """
    def __init__(self, parent=None):
        # Validation.
        assert isinstance(self, (QtWidgets.QLineEdit,
                                 QtWidgets.QTextEdit,
                                 QtWidgets.QLabel
                                 )), \
            'Unable to use mixin with widget type {!r}'.format(
                self.__class__.__bases__[-1])

        # Init.
        super(MixinElided, self).__init__(parent)
        self._real_text = ''
        self._use_elision = True

        self.elide_mode = QtCore.Qt.ElideRight

        self.setObjectName('test')

    # Private.
    def __set_elided_text(self):
        """Elide the real text and display it on the widget."""
        r_margin_padding = 0

        if hasattr(self, 'textMargins'):
            r_margin_padding = self.textMargins().right() + \
                               self.textMargins().left() + \
                               2  # Cuts off elision within display area.

        font_metrics = QtGui.QFontMetrics(self.font())
        width = self.geometry().width() - r_margin_padding

        elided_text = font_metrics.elidedText(self._real_text,
                                              self.elide_mode,
                                              width
                                              )

        super(MixinElided, self).setText(elided_text)
        self.__set_cursor_to_start()

    def __set_cursor_to_start(self):
        """If the widget has editable text, move the text cursor position
        back to the beginning.
        """
        if hasattr(self, 'setCursorPosition'):
            self.setCursorPosition(0)

    # Public.
    def enable_elision(self, state):
        """Enable elided text display.

        Args:
            state (bool): Toggles on/off state of elision.
        """
        self._use_elision = state
        self.setText(self._real_text)  # Force dynamic text update.

    def set_elide_mode(self, elide_mode):
        """Set the elision mode.

        Args:
            elide_mode (QtCore.Qt.TextElideMode): The text elision mode to
                use for the displayed text.
        """
        self.elide_mode = elide_mode

    # Overrides.
    def setText(self, text):
        """Override the inherited setText method.
        Display the elided text or real text, based on elision state.

        Args:
            text (str): Text to display.
        """
        # Store the real text.
        self._real_text = text

        # If elision is enabled, display the elided text.
        if self._use_elision:
            self.__set_elided_text()

        # Otherwise, display the real text.
        else:
            super(MixinElided, self).setText(self._real_text)
            self.__set_cursor_to_start()

    def resizeEvent(self, event):
        """Override the inherited resizeEvent method.
        Updates the displayed text as widget is scaled.

        Args:
            event (QtCore.Qt.QEvent): Pass-through event.
        """
        super(MixinElided, self).resizeEvent(event)

        if self._use_elision:
            self.__set_elided_text()

        event.accept()


class MixinTextToolTip(object):
    """Updates tooltip for text/editor widgets with the real text value.

    Usage:
        When using this mixin in a class with multiple inheritances, make sure
        this mixin has precedence over any mixins which modify text
        (such as MixinElided).
        This will ensure that the real text is displayed as tooltip, rather
        than the modified display text.

    """
    def __init__(self, parent=None):
        # Validation.
        assert isinstance(self, (QtWidgets.QLineEdit,
                                 QtWidgets.QLabel)), \
            'Unable to use mixin with widget type {!r}'.format(
                self.__class__.__bases__[-1])

        # Init.
        super(MixinTextToolTip, self).__init__(parent)

    def setText(self, text):
        """Override the inherited setText method.
        Sets the real text as tooltip for quick referencing.

        Args:
            text (str): Text to display.
        """
        super(MixinTextToolTip, self).setText(text)
        self.setToolTip(text)
