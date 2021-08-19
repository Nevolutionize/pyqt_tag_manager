import types

# Import local modules.
from Qt import QtCore
from Qt import QtGui
from Qt import QtWidgets
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


def set_default_property(name, value):
    def property_decorator(func):
        def func_wrapper(*args, **kwargs):
            widget = func(*args, **kwargs)
            widget.setProperty(name, value)

            return widget
        return func_wrapper
    return property_decorator


# Public.
# Layouts.
def get_hbox_layout(parent=None, no_margins=False):
    """Get a custom QHBoxLayout widget.

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
    spacer = QtWidgets.QSpacerItem(20, 20,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Minimum
                                   )
    return spacer


def get_v_spacer():
    spacer = QtWidgets.QSpacerItem(20, 20,
                                   QtWidgets.QSizePolicy.Minimum,
                                   QtWidgets.QSizePolicy.Expanding
                                   )

    return spacer


def get_h_divider(parent=None):
    div = QtWidgets.QFrame(parent)
    div.setFrameShape(div.HLine)
    div.setFixedHeight(1)

    return div


def get_v_divider(parent=None):
    div = QtWidgets.QFrame(parent)
    div.setFrameShape(div.VLine)
    div.setFixedHeight(1)

    return div


def get_h_splitter(parent=None):
    splitter = QtWidgets.QSplitter(parent=parent,
                                   orientation=QtCore.Qt.Horizontal
                                   )
    splitter.setHandleWidth(10)

    return splitter


def get_v_splitter(parent=None):
    splitter = QtWidgets.QSplitter(parent=parent,
                                   orientation=QtCore.Qt.Vertical
                                   )
    splitter.setHandleWidth(10)

    return splitter


# Widgets.
@apply_default_widget_size(width=False, height=True, height_size=20)
def get_empty_widget(parent=None, name='CENT-GUI-BASE-WIDGET'):
    widget = QtWidgets.QWidget(parent)
    widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    # Override default parameters.
    widget.setObjectName(name)

    return widget


@apply_default_widget_size(height=True)
def get_label(parent=None, text=None, name='CENT-GUI-LABEL', elided=False,
              elide_mode=None):
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
@set_default_property(name='vendored', value=True)
def get_line_edit(parent=None, name='CENT-GUI-LINE-EDIT',
                  elided=False, elide_mode=None):
    widget = editors.LineEdit(parent)

    # Override default parameters.
    widget.setObjectName(name)
    widget.enable_elision(elided)
    if elide_mode:
        widget.set_elide_mode(elide_mode)

    widget.setTextMargins(DEFAULT_TEXT_MARGINS)

    return widget


# @apply_default_widget_size(height=True)
# @set_default_property(name='vendored', value=True)
# def get_line_display(parent=None, name='CENT-GUI-LINE-EDIT',
#                      elided=True, elide_mode=None):
#     widget = get_line_edit(parent, name, elided, elide_mode)
#
#     # Override default parameters.
#     widget.setReadOnly(True)
#
#     return widget


# def get_text_edit(parent=None, name='CENT-GUI-TEXT-EDIT', elided=True,
#                   elide_mode=None):
#     widget = editors.TextEdit(parent)
#
#     # Override default parameters.
#     widget.setObjectName(name)
#     widget.enable_elision(elided)
#     if elide_mode:
#         widget.set_elide_mode(elide_mode)
#
#     widget.setReadOnly(True)
#
#     return widget
#
#
# @apply_default_widget_size(height=True)
# def get_spin_box(parent=None, name='CENT-GUI-SPIN-BOX'):
#     widget = editors.SpinBox(parent)
#
#     # Override default parameters.
#     widget.setObjectName(name)
#
#     widget.lineEdit().setTextMargins(DEFAULT_TEXT_MARGINS)
#
#     return widget
#
#
# @apply_default_widget_size(height=True)
# def get_double_spin_box(parent=None, name='CENT-GUI-DOUBLE-SPIN_BOX'):
#     widget = editors.DoubleSpinBox(parent)
#
#     # Override default parameters.
#     widget.setObjectName(name)
#
#     widget.lineEdit().setTextMargins(DEFAULT_TEXT_MARGINS)
#
#     return widget
#
#
# @apply_default_widget_size(height=True)
# def get_combo_box(parent=None, name='CENT-GUI-COMBO-BOX'):
#     widget = editors.ComboBox(parent)
#
#     # QComboBox drop down viewer has a delegate by default, which prevents
#     # any QSS styling from working. e.g. "QComboBox QAbstractItemView:item {
#     # border: 2px solid red;}" won't do anything.
#     # Setting the view no longer uses the delegate and allows the QSS to work.
#     widget.setView(QtWidgets.QListView(widget))
#
#     # Override default parameters.
#     widget.setObjectName(name)
#
#     return widget
#
#
# def get_scroll_area(parent=None, name='CENT-GUI-SCROLL-AREA'):
#     widget = QtWidgets.QScrollArea(parent)
#
#     # Override default parameters.
#     widget.setObjectName(name)
#
#     widget.setContentsMargins(DEFAULT_LAYOUT_CONTENT_MARGINS)
#     widget.setWidgetResizable(True)
#
#     return widget
#
#
# def get_group_box(parent=None, name='CENT-GUI-GROUP-BOX', title=None):
#     widget = QtWidgets.QGroupBox(parent)
#
#     # Override default parameters.
#     widget.setObjectName(name)
#
#     widget.setContentsMargins(DEFAULT_LAYOUT_CONTENT_MARGINS)
#     widget.setTitle(title)
#
#     return widget
