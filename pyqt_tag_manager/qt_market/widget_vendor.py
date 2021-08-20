# Import local modules.
from pyqt_tag_manager import QtCore
from pyqt_tag_manager import QtWidgets
from pyqt_tag_manager.qt_market import editors


# Constants.
DEFAULT_WIDGET_WIDTH = 30
DEFAULT_WIDGET_HEIGHT = 24  # 30.
EMPTY_MARGINS = QtCore.QMargins(0, 0, 0, 0)
DEFAULT_TEXT_MARGINS = QtCore.QMargins(5, 2, 5, 2)  # L, T, R, B.
DEFAULT_LAYOUT_CONTENT_MARGINS = QtCore.QMargins(5, 5, 5, 5)


# Decorators.
def apply_default_widget_size(width=False, height=False,
                              width_size=DEFAULT_WIDGET_WIDTH,
                              height_size=DEFAULT_WIDGET_HEIGHT):
    """Decorator that applies consistent sizing to vendored widgets.

    Args:
        width (bool): Apply default width to widget.
        height (bool): Apply default height to widget.
        width_size (int): Override widget width with provided value instead.
        height_size (int): Override widget height with provided value instead.
    """
    def resize_decorator(func):
        def func_wrapper(*args, **kwargs):
            widget = func(*args, **kwargs)

            if width:
                widget.setFixedWidth(width_size)
            if height:
                widget.setFixedHeight(height_size)

            return widget
        return func_wrapper
    return resize_decorator


# Public.
# Layouts.
def get_hbox_layout(parent=None, no_margins=False):
    """Get a custom QHBoxLayout widget.

    Args:
        parent (QtWidgets.QWidget): Parent widget.
        no_margins (bool): Removes all layout margins.
    Returns:
        QtWidgets.QHBoxLayout: Custom horizontal box layout.
    """
    layout = QtWidgets.QHBoxLayout(parent)

    # Override default parameters.
    margins = EMPTY_MARGINS if no_margins else DEFAULT_LAYOUT_CONTENT_MARGINS
    layout.setContentsMargins(margins)

    return layout


def get_vbox_layout(parent=None, no_margins=False):
    """Get a custom QVBoxLayout widget.

    Args:
        parent (QtWidgets.QWidget): Parent widget.
        no_margins (bool): Removes all layout margins.
    Returns:
        QtWidgets.QVBoxLayout: Custom vertical box layout.
    """
    layout = QtWidgets.QVBoxLayout(parent)

    # Override default parameters.
    margins = EMPTY_MARGINS if no_margins else DEFAULT_LAYOUT_CONTENT_MARGINS
    layout.setContentsMargins(margins)

    return layout


def get_form_layout(parent=None, no_margins=False):
    """Get a custom QFormLayout widget.

    Args:
        parent (QtWidgets.QWidget): Parent widget.
        no_margins (bool): Removes all layout margins.
    Returns:
        QtWidgets.QFormLayout: Custom form layout.
    """
    layout = QtWidgets.QFormLayout(parent)

    # Override default parameters.
    margins = EMPTY_MARGINS if no_margins else DEFAULT_LAYOUT_CONTENT_MARGINS
    layout.setContentsMargins(margins)

    return layout


# Misc widgets.
def get_h_spacer():
    """Get a custom horizontal spacer item.

    Returns:
        QtWidgets.QSpacerItem: Custom horizontal spacer item.
    """
    spacer = QtWidgets.QSpacerItem(20, 20,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Minimum
                                   )

    return spacer


def get_v_spacer():
    """Get a custom horizontal spacer item.

    Returns:
        QtWidgets.QSpacerItem: Custom vertical spacer item.
    """
    spacer = QtWidgets.QSpacerItem(20, 20,
                                   QtWidgets.QSizePolicy.Minimum,
                                   QtWidgets.QSizePolicy.Expanding
                                   )

    return spacer


def get_h_divider(parent=None):
    """Get a custom horizontal divider widget.

    Args:
        parent (QtWidgets.QWidget): Parent widget.
    Returns:
        QtWidgets.QFrame: Custom horizontal divider widget.
    """
    div = QtWidgets.QFrame(parent)
    div.setFrameShape(div.HLine)
    div.setFixedHeight(1)

    return div


def get_v_divider(parent=None):
    """Get a custom vertical divider widget.

    Args:
        parent (QtWidgets.QWidget): Parent widget.
    Returns:
        QtWidgets.QFrame: Custom vertical divider widget.
    """
    div = QtWidgets.QFrame(parent)
    div.setFrameShape(div.VLine)
    div.setFixedHeight(1)

    return div


def get_h_splitter(parent=None):
    """Get a custom horizontal splitter widget.

    Args:
        parent (QtWidgets.QWidget): Parent widget.
    Returns:
        QtWidgets.QSplitter: Custom horizontal splitter widget.
    """
    splitter = QtWidgets.QSplitter(parent=parent,
                                   orientation=QtCore.Qt.Horizontal
                                   )
    splitter.setHandleWidth(10)

    return splitter


def get_v_splitter(parent=None):
    """Get a custom vertical splitter widget.

    Args:
        parent (QtWidgets.QWidget): Parent widget.
    Returns:
        QtWidgets.QSplitter: Custom vertical splitter widget.
    """
    splitter = QtWidgets.QSplitter(parent=parent,
                                   orientation=QtCore.Qt.Vertical
                                   )
    splitter.setHandleWidth(10)

    return splitter


# Widgets.
@apply_default_widget_size(width=False, height=True, height_size=20)
def get_empty_widget(parent=None, name='GUI-BASE-WIDGET'):
    """Get a custom empty widget.

    Args:
        parent (QtWidgets.QWidget): Parent widget.
        name (str): Text assigned as the object name of the widget.

    Returns:
        QtWidgets.QWidget: Custom empty widget.
    """
    widget = QtWidgets.QWidget(parent)
    widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    # Override default parameters.
    widget.setObjectName(name)

    return widget


@apply_default_widget_size(height=True)
def get_label(parent=None, text=None, name='GUI-LABEL', elided=False,
              elide_mode=None):
    """Get a custom label widget.

    Args:
        parent (QtWidgets.QWidget): Parent widget.
        text (str): Text value of the label.
        name (str): Text assigned as the object name of the widget.
        elided (bool): Enable text elision for widget.
        elide_mode (QtCore.Qt.TextElideMode): The text elision mode to
            use for the displayed text.

    Returns:
        QtWidgets.QWidget: Custom label widget.
    """
    widget = editors.Label(parent)

    # Override default parameters.
    widget.setObjectName(name)
    widget.enable_elision(elided)
    if elide_mode:
        widget.set_elide_mode(elide_mode)
    if text:
        widget.setText(text)

    return widget


@apply_default_widget_size(height=True)
def get_line_edit(parent=None, name='GUI-LINE-EDIT',
                  elided=False, elide_mode=None):
    """Get a custom line edit widget.

    Args:
        parent (QtWidgets.QWidget): Parent widget.
        name (str): Text assigned as the object name of the widget.
        elided (bool): Enable text elision for widget.
        elide_mode (QtCore.Qt.TextElideMode): The text elision mode to
            use for the displayed text.

    Returns:
        QtWidgets.QWidget: Custom line edit widget.
    """
    widget = editors.LineEdit(parent)

    # Override default parameters.
    widget.setObjectName(name)
    widget.enable_elision(elided)
    if elide_mode:
        widget.set_elide_mode(elide_mode)

    widget.setTextMargins(DEFAULT_TEXT_MARGINS)

    return widget
