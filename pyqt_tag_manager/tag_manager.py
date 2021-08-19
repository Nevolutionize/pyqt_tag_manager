# Import local modules.
from Qt import QtCore
from Qt import QtGui
from Qt import QtWidgets
from pyqt_tag_manager.qt_market import widget_vendor
from pyqt_tag_manager.qt_market import color_utils
from pyqt_tag_manager.qt_market import animations


# Constants.
DISPLAY_ROLE = QtCore.Qt.DisplayRole  # Text display for tag.
SORTING_MATCH_ROLE = QtCore.Qt.UserRole + 1  # Tag is prioritized when sorting.


class TagManager(QtWidgets.QWidget):
    """Tag management interface used for editing and displaying tags."""
    # Signals.
    mode_changed = QtCore.Signal(str)
    tag_is_valid = QtCore.Signal(str)
    tag_is_invalid = QtCore.Signal(str)
    tag_registered = QtCore.Signal(bool)

    # Constants.
    EDIT_MODE = 'TagManager.editor_mode'
    VIEWER_MODE = 'TagManager.viewer_mode'

    def __init__(self, parent=None):
        super(TagManager, self).__init__(parent)
        self.editing_mode = True

        self.__build_ui()

    # Private.
    def __build_ui(self):
        """Build the base UI."""
        main_layout = widget_vendor.get_vbox_layout(self, no_margins=True)
        self.setLayout(main_layout)

        # Add tag manager.
        self.tag_manager = _TaggingWidget(self)
        self.tag_editor = self.tag_manager.get_editor()
        self.tag_viewer = self.tag_manager.get_viewer()

        main_layout.addWidget(self.tag_manager)

        # Signals.
        self.tag_editor.textChanged.connect(self._on_editor_text_changed)
        self.tag_editor.returnPressed.connect(self._on_return_pressed)

        self.mode_changed.connect(self._on_mode_changed)
        self.tag_is_valid.connect(self._on_tag_is_valid)
        self.tag_is_invalid.connect(self._on_tag_is_invalid)

    def __register_tag(self, tag_name):
        """Register the tag so that it's available in the underlying model.

        Args:
            tag_name (str): Name of the tag to register.
        """
        # Prevent duplication: Add tag only if it doesn't exist.
        if not self.has_tag(tag_name):
            self.tag_viewer.add_tags([tag_name])
            return True
        else:
            return False

    # Public.
    def add_tag(self, tag_name):
        """Add a uniquely named tag item to the viewer.

        Args:
            tag_name (str): Name of the tag to add.

        Emits:
            tag_registered: True if tag was added, otherwise False.
        """
        if self.__register_tag(tag_name):
            self.tag_registered.emit(True)
            return True

        else:
            self.tag_registered.emit(False)
            return False

    def add_tags(self, tags):
        """Add a list of tags to the viewer.

        Args:
            tags (list): List of tags toa dd.
        """
        for tag in tags:
            self.add_tag(tag)

    def clear_tags(self):
        """Clear all existing tags from the viewer's model."""
        self.tag_viewer.clear_tags()

    def has_tag(self, tag_name):
        """Check if a tag already exists in the viewer's model.

        Args:
            tag_name (str): Name of the tag to search for.

        Returns:
            bool: True if tag already exists, otherwise False.
        """
        return self.tag_viewer.find_tag(tag_name)

    def get_tags(self):
        """Return all of the registered tags.

        Returns:
            list: List of all registered tags.
        """
        return self.tag_viewer.get_tags()

    def enable_tag_management(self, enabled):
        """Allows editing functionality for tags within the manager.

        Args:
            enabled (bool): Determines if tags can be edited.
        """
        mode = self.EDIT_MODE if enabled else self.VIEWER_MODE
        self.mode_changed.emit(mode)

    def enable_tag_editor_mode(self):
        """Enables editing functionality for tags. """
        self.enable_tag_management(True)

    def enable_tag_preview_mode(self):
        """Disables editing functionality for tags (read-only). """
        self.enable_tag_management(False)

    # Slots.
    @QtCore.Slot()
    def _on_editor_text_changed(self, text):
        """Triggered when the tag input editor text is changed.

        Args:
            text (str): The current text input value.
        """
        self.tag_viewer.sort_tags_by_search_criteria(text=text)

    @QtCore.Slot()
    def _on_return_pressed(self):
        """Triggered when the tag input editor is returned. """
        tag_name = self.tag_editor.text()

        if tag_name and not self.has_tag(tag_name):
            self.tag_is_valid.emit(tag_name)
        else:
            self.tag_is_invalid.emit(tag_name)

    @QtCore.Slot()
    def _on_mode_changed(self, mode):
        """Triggered when the editing functionality of the manager changes. """
        enabled = True if mode == self.EDIT_MODE else False
        self.tag_manager.enable_editing(enabled)

    @QtCore.Slot()
    def _on_tag_is_valid(self, tag_name):
        """Triggered when the tag input editor value is valid. """
        self.add_tag(tag_name)
        self.tag_editor.clear()
        self.tag_viewer.scroll_to_last_added_item()

    @QtCore.Slot()
    def _on_tag_is_invalid(self, tag_name):
        """Triggered when the tag input editor value is invalid. """
        anm = animations.FailColorAnimation(parent=self.tag_editor)
        anm.play()


# Protected: Not intended for use outside this module!
class _TaggingWidget(QtWidgets.QFrame):
    """Base widget containing the tag editor and viewer."""
    def __init__(self, parent=None):
        super(_TaggingWidget, self).__init__(parent)
        self.setFrameShape(self.StyledPanel)
        self.setAutoFillBackground(True)
        self.setBackgroundRole(self.palette().Base)

        self._build_ui()

    # Public.
    def _build_ui(self):
        """Build the base UI."""
        main_layout = widget_vendor.get_vbox_layout(self, no_margins=True)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

        # Add the tag editor widgets.
        self.tag_editor = _InputEditor(self)
        main_layout.addWidget(self.tag_editor)

        # Add divider.
        self.divider = widget_vendor.get_h_divider(self)
        main_layout.addWidget(self.divider)

        # Add the tag viewer widgets.
        self.tag_viewer = _TagListViewer(self)

        # Blend in with the frame.
        self.tag_viewer.setFrameShape(self.NoFrame)
        viewport = self.tag_viewer.viewport()
        viewport.setAutoFillBackground(False)

        main_layout.addWidget(self.tag_viewer)

    def get_editor(self):
        """Returns the input editor widget that allows user to
        add/filter/sort tags."""
        return self.tag_editor.get_editor()

    def get_viewer(self):
        """Returns the viewer widget that allows user to see all available
        tags. """
        return self.tag_viewer

    def enable_editing(self, enabled):
        # Show/hide the editing portion of the widget.
        self.tag_editor.setVisible(enabled)
        self.divider.setVisible(enabled)

        # Make the tags un-editable.
        self.tag_viewer.enable_tag_management(enabled)


class _InputEditor(QtWidgets.QWidget):
    """Base widget used for editing the tag input value. """
    def __init__(self, parent=None):
        super(_InputEditor, self).__init__(parent)
        self._valid_characters = [' ', '_', '.']

        self._build_ui()

    def _build_ui(self):
        """Build the base UI."""
        # Add layouts.
        main_layout = widget_vendor.get_hbox_layout(self, no_margins=True)
        self.setLayout(main_layout)

        # Add editor widget.
        self.add_tag_edit = widget_vendor.get_line_edit()
        self.add_tag_edit.setProperty('vendored', False)  # Exclude from QSS.

        self.add_tag_edit.setClearButtonEnabled(True)
        self.add_tag_edit.setFrame(False)

        # TODO: Why am I enforcing this? Validator needs to be configurable.
        # validator = validators.no_special_characters(
        #     allow_chars=self._valid_characters,
        #     limit=50
        # )
        # self.add_tag_edit.setValidator(validator)

        valid_chrs = 'a-Z, 0-9, "{c}"'.format(
            c='", "'.join(self._valid_characters))
        self.add_tag_edit.setToolTip(
            'Supported characters: {valid}'.format(valid=valid_chrs))
        self.add_tag_edit.setPlaceholderText('Add tag...')

        # Disable the editor background.
        # Since certain widgets inherit styling from the OS, changing their
        # backgroundRole to Window won't do anything.
        # To get around this, we'll make the palette transparent.
        palette = self.add_tag_edit.palette()
        palette.setColor(palette.Base, QtGui.QColor(255, 255, 255, 25))
        self.add_tag_edit.setPalette(palette)

        main_layout.addWidget(self.add_tag_edit)

    def get_editor(self):
        """Returns the line edit widget that accepts the input. """
        return self.add_tag_edit


class _TagListViewer(QtWidgets.QListView):
    """Base list viewport widget used to display all available tags. """
    def __init__(self, parent=None):
        super(_TagListViewer, self).__init__(parent)
        self.__tag_management_enabled = False
        self.__dark_mode_enabled = True
        self.__last_item_added = None

        # Defaults.
        self.setSpacing(3)
        self.setFlow(self.LeftToRight)
        self.setWrapping(True)
        self.setViewMode(self.ListMode)
        self.setWordWrap(True)
        self.setFrameShape(self.NoFrame)
        self.setSelectionMode(self.NoSelection)
        self.setMouseTracking(True)
        self.setItemDelegate(_TagDelegate(self))

        viewport = self.viewport()
        viewport.setAutoFillBackground(False)
        self.setViewportMargins(2, 4, 2, 4)

        self.__setup_model()
        self.enable_tag_management(True)

    # Private.
    def __setup_model(self):
        """Setup for the model(s) used by the viewer. """
        self._model = QtGui.QStandardItemModel(self)

        self._proxy_model = _TagListProxyModel(self)
        self._proxy_model.setSourceModel(self._model)
        self.setModel(self._proxy_model)

    def scroll_to_last_added_item(self):
        """Scrolls viewer to the last tag (item) that was added to the model.

        Since model sorting is handled by the QSortFilterProxyModel, it will
        scroll to the positional index of the proxy model.
        """
        if self.__last_item_added:
            index = self.__last_item_added.index()

            if index.isValid():
                self.scrollTo(self._proxy_model.mapFromSource(index),
                              self.PositionAtBottom
                              )

    # Public.
    def find_tag(self, tag_name):
        """Checks if a tag exists in the model.

        Returns:
            bool: True if tag name exists, otherwise False.
        """
        match = self._model.findItems(tag_name, QtCore.Qt.MatchExactly, 0)
        return True if match else False

    def add_tag(self, tag_name):
        """Add a tag to the model.

        Args:
            tag_name (str): The name of the tag to add.
        """
        item = QtGui.QStandardItem()
        item.setData(tag_name, DISPLAY_ROLE)
        item.setData(False, SORTING_MATCH_ROLE)
        item.setEditable(False)
        item.setSelectable(False)

        self._model.appendRow(item)
        self.__last_item_added = item

    def add_tags(self, tags):
        """Add a list of tags to the model.

        Note:
            Sorting after every item has a significant affect on performance
            when adding tags from a large list of tags.

            This is specially true when the proxy model sorting is triggered.
            Therefore, we'll only sort once all the tags are added.

        Args:
            tags (list): List of tags to add to the model.
        """
        for tag in tags:
            self.add_tag(tag)

        self.sort()

    def clear_tags(self):
        """Clear the model of all tags/items."""
        self._model.clear()

    def delete_tag(self, tag_name):
        """Delete a specific tag from the model, by name.

        Args:
            tag_name (str): The name of the tag to delete.
        """
        match = self._model.findItems(tag_name, QtCore.Qt.MatchExactly, 0)

        for item in match:
            self._model.removeRow(item.row())

    def get_tags(self):
        """Returns a list of all available tags in the model."""
        tag_list = []
        for row in range(self._model.rowCount()):
            index = self._model.index(row, 0)
            tag_name = self._model.data(index, DISPLAY_ROLE)
            tag_list.append(tag_name)

        return tag_list

    def sort(self):
        """Sort the proxy model based on the pre-defined sort criteria.
        Warning: This can be a time-intensive operation when lots of tags
        exist (> 200). Use sparingly and only when needed.
        """
        self._proxy_model.sort(0)

    def sort_tags_by_search_criteria(self, text):
        """Sorts the tags by the provided text.

        Args:
            text (str): Text pattern to sort tags by.
        """
        self.scrollToTop()
        self._proxy_model.sort_by_match(text)

    def enable_tag_management(self, enabled):
        """Allows editing functionality for tags within the manager.

        Args:
            enabled (bool): Determines if tags can be edited.
        """
        self.__tag_management_enabled = enabled

    def is_tag_management_enabled(self):
        """Checks if the tag editing mode is enabled or disabled.

        Returns:
            bool: True if editing mode is enabled, False if preview mode is
              enabled.
        """
        return self.__tag_management_enabled

    def enable_dark_mode(self, enabled):
        """Enables dark mode styling of the tag delegates.

        Args:
            enabled (bool): Enables dark mode styling.
        """
        self.__dark_mode_enabled = enabled

    def is_dark_mode_enabled(self):
        """Checks if dark mode is enabled. """
        return self.__dark_mode_enabled


class _TagDelegate(QtWidgets.QStyledItemDelegate):
    """Custom delegate representation of the tag/item in the viewer. """
    def __init__(self, parent=None):
        super(_TagDelegate, self).__init__(parent)
        self.__is_hovering_delete_btn = False

        self._height = 20
        self._height_padding = 2
        self._width_padding = 20
        self._delete_btn_size = QtCore.QSize(24, self._height)

        self.__font_setup()

    # Private.
    def __font_setup(self):
        """Sets up the font used to render the label.

        Since we're calculating the delegate sizeHint based on the text length
        and font render styling, QFontMetrics is used to achieve this.

        Unfortunately, QFontMetrics seems to be plagued with bugs when
        calculating the width.
        See: https://bugreports.qt.io/projects/QTBUG/issues/
        (Text: "QFontMetrics, boundingRect, width")

        While debugging and searching online for solutions, I've managed to
        identify a few rules that need to be followed for accurate widths.

        Rules:
            1) Always set the font family via constructor or setFamily(),
            even if it's the same value as the default.
            2) If the above doesn't work, use a monospace font (fixed width).
            3) Always set the pointSize or pixelSize, even if it's the same
            value as the default.
            4) Use of font weight/bold may or may not (font family dependent)
            calculate font boundingRect correctly.
        """
        # The font family and size must absolutely be set, even if it's the
        # same value as the default.
        self._label_font = QtGui.QFont('verdana')
        self._label_font.setPointSize(10)

        self._label_font.setWeight(self._label_font.Black)
        self._label_font.setKerning(False)

    # TODO: Deprecate? Now that editorEvent is informing the paint method when
    #  the cursor is hovering over the delete button, is this still needed?
    # def __is_cursor_in_delete_button_rect(self, rect, pos):
    #     """Checks if the cursor is within the bounds of the "Delete Tag"
    #     button of the delegate.
    #
    #     Args:
    #         rect(QtCore.QRect):
    #     """
    #     return self.__delete_button_rect(rect).contains(pos)

    def __delete_button_rect(self, rect):
        """Returns a custom adjusted rect for the "delete" button of the
        delegate.

        Args:
            rect (QtCore.QRect):
        """
        padding = 4  # Applies padding to offset the button from the sides.
        return rect.adjusted(
            rect.width() - self._delete_btn_size.width() - padding,  # Right.
            (rect.height() - self._delete_btn_size.height()) / 2,  # Center.
            -padding,  # Left.
            -(rect.height() - self._delete_btn_size.height()) / 2,  # Center.
        )

    def __label_rect(self, rect):
        # If viewer is editable, subtract the delete button from the label.
        if self.is_tag_management_enabled():
            rect = rect.adjusted(0, 0, -self._delete_btn_size.width(), 0)
            return rect

        return rect

    # Inherited.
    def paint(self, painter, option, index):
        """Override the inherited paint method.

        Custom paint implementation is used here to draw and style the item.
        """
        tag_name = index.data(DISPLAY_ROLE)
        base_color = color_utils.get_mapped_color(text=tag_name)

        # Styling.
        radius = 4

        # Light mode: Set colors to reduce eye strain and improve
        # readability on white background.
        fg_color = QtGui.QColor(QtCore.Qt.white)
        fg_color.setAlpha(235)

        bg_color = color_utils.pastelize_color(base_color)
        bg_color = color_utils.desaturate(bg_color, percent=15)
        bg_color.setAlpha(255)

        fg_button_color = QtGui.QColor(fg_color)
        fg_button_color.setAlpha(125)

        border_color = base_color.darker(125)
        border_color.setAlpha(255)  # Border only visible in light mode.

        # Dark mode: Hide the border and make the label full alpha for
        # readability.
        if self.is_dark_mode_enabled():
            fg_color.setAlpha(255)
            border_color.setAlpha(0)  # Hide border in dark mode.

        # Check the item's data for SORTING_MATCH_ROLE, to determine if it
        # matches the search query. If it doesn't, make it semi-transparent.
        if not index.data(SORTING_MATCH_ROLE):
            # Light mode: Adjust alpha for readability on white bg.
            bg_color.setAlpha(75)
            fg_color.setAlpha(150)
            fg_button_color.setAlpha(75)
            border_color.setAlpha(50)  # Border slightly visible in light mode.

            # Dark mode: Adjust alpha for readability on darker bg.
            if self.is_dark_mode_enabled():
                bg_color.setAlpha(50)
                fg_color.setAlpha(50)
                fg_button_color.setAlpha(50)
                border_color.setAlpha(0)  # Keep border hidden in dark mode.

        bg_brush = QtGui.QBrush(bg_color, QtCore.Qt.SolidPattern)

        # Start painting the delegate.
        rect = option.rect

        painter.save()
        painter.setRenderHint(painter.Antialiasing)
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(QtCore.Qt.NoPen)

        # Paint background.
        painter.setBrush(bg_brush)
        painter.setPen(QtGui.QPen(border_color, 2, QtCore.Qt.SolidLine))

        painter.drawRoundedRect(rect, radius, radius, QtCore.Qt.AbsoluteSize)

        # Draw label text.
        painter.setFont(self._label_font)
        painter.setPen(fg_color)
        painter.drawText(self.__label_rect(rect),
                         QtCore.Qt.AlignCenter,
                         tag_name)

        # Draw the "Delete Tag" button if tag management is enabled.
        if self.is_tag_management_enabled():
            # Draw button background.
            painter.setBrush(QtCore.Qt.NoBrush)  # Transparent background.
            painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))  # Transparent border.
            painter.drawRoundedRect(
                self.__delete_button_rect(rect), 0, 0, QtCore.Qt.AbsoluteSize)

            # Draw button text.
            font = QtGui.QFont('verdana')
            font.setBold(True)
            font.setPointSize(10)
            painter.setFont(font)

            # First, check if delegate/item has cursor focus (hover).
            # Note: Skipping this step can result in false-positives,
            # since the editorEvent is only aware of hovering while the
            # respective item is being edited.
            # This can fool the delegate into thinking that there's focus on
            # the delete buttons for both the current and previous item.
            if option.state & QtWidgets.QStyle.State_MouseOver:
                # Now that we've determined the current item is in focus,
                # we check if editorEvent determined the cursor is hovering
                # over the delete button.
                if self.__is_hovering_delete_btn:
                    if not index.data(SORTING_MATCH_ROLE):
                        fg_button_color.setAlpha(fg_button_color.alpha() + 50)
                    else:
                        fg_button_color.setAlpha(225)

            painter.setPen(fg_button_color)
            painter.drawText(self.__delete_button_rect(rect),
                             QtCore.Qt.AlignCenter, 'X')

        painter.restore()

    def editorEvent(self, event, model, option, index):
        """Override the inherited editorEvent method.

        Triggered when starting the editing of an item.
        """
        # If tag management is enabled, capture QMouseEvents for delete button.
        if self.is_tag_management_enabled():
            if self.__delete_button_rect(option.rect).contains(event.pos()):
                # Delete tag when button is pressed.
                if event.type() == QtCore.QEvent.MouseButtonRelease:
                    self.parent().delete_tag(index.data(DISPLAY_ROLE))
                    return True

                # For styling purposes, inform the painter that the cursor is
                # moving (hovering) over the delete button.
                if event.type() == QtCore.QEvent.MouseMove:
                    self.__is_hovering_delete_btn = True
                    return True

            # Once event (cursor) exists delete button, disable styling.
            else:
                self.__is_hovering_delete_btn = False
                return True

        return super(_TagDelegate, self).editorEvent(event, model, option,
                                                     index)

    def sizeHint(self, option, index):
        """Override the inherited sizeHint method.

        Custom logic re-calculates the correct size of the delegate so that
        items don't get overlapped in the viewport.
        """
        rect = QtGui.QFontMetricsF(self._label_font).boundingRect(
            option.rect,
            QtCore.Qt.TextSingleLine,
            index.data(DISPLAY_ROLE)
        )

        label_width = rect.width()
        label_height = rect.height()

        # Ignore the "hidden" delete button if tag management is disabled.
        delete_btn_width = self._delete_btn_size.width() if \
            self.is_tag_management_enabled() else 0

        width = self._width_padding + label_width + delete_btn_width

        if label_height < 20:
            height = self._height_padding + self._height
        else:
            height = self._height_padding + label_height

        return QtCore.QSize(width, height)

    # Public.
    def is_tag_management_enabled(self):
        """Checks if tag editing functionality is enabled on the parent
        viewer.

        The "Delete Tag" button will only be drawn if editing is enabled.
        """
        return self.parent().is_tag_management_enabled()

    def is_dark_mode_enabled(self):
        """Checks if dark mode is enabled on the parent viewer.

        The delegate paint styling is adjusted accordingly, to make it easy
        on the eyes.
        """
        return self.parent().is_dark_mode_enabled()


class _TagListProxyModel(QtCore.QSortFilterProxyModel):
    """Custom model for sorting and filtering.

    Our ideal sorting mechanism is expected to...
        A) Always prioritize items matching the search pattern.
        B) Followed by the non-matching items.
        C) Both must always be sorted in ascending order.

        Additionally, non-matching items will be semi-transparent to provide
        focus on matching items.

        Example:
            items = [taxi, crown, tea, cat, boat, car, zoo, 001, 2]
            search_pattern = 'c.*'

            sorted_result = [car, cat, crown][001, 2, boat, taxi, tea, zoo]

        As seen in the result above, the first group indicates items
        that match the search pattern, fulfilling criteria A.

        The second group indicates non-matching items, fulfilling criteria B.
        This group will also display semi-transparent, as noted above.

        Finally, both groups are sorted ascending, fulfilling criteria C.
    """
    # Signals.
    item_priority_checked = QtCore.Signal(object, bool)  # Emit on regex match.

    def __init__(self, parent=None):
        super(_TagListProxyModel, self).__init__(parent)
        self.setSortRole(DISPLAY_ROLE)

        # DynamicSortFilter can't be True when updating source model via proxy.
        # Since we need to do this (item_matches_query) to inform the source
        # model when an item matches the search criteria (for delegate
        # styling), let's disable it.
        self.setDynamicSortFilter(False)

        self.__search_query_regex = QtCore.QRegExp(
            '.*',
            QtCore.Qt.CaseInsensitive,
            QtCore.QRegExp.RegExp
        )

    # Inherited.
    def sort(self, column, order=QtCore.Qt.AscendingOrder):
        """Override the inherited sort method.

        Most of the time tags will be added to the viewer manually using
        the InputEditor, which triggers the textChanged signal and calls
        sort_by_match.
        Adding tags directly to TagListViewer skips sort_by_match and it also
        doesn't trigger lessThan, since only 1 item exists in the list.

        As a result SORTING_MATCH_ROLE won't be updated and the delegate
        will be painted incorrectly.
        To get around this, we can force sort_by_match to trigger when the
        model only contains 1 item.
        """
        super(_TagListProxyModel, self).sort(column, order)

        if self.rowCount() == 1:
            self.sort_by_match('')

    def lessThan(self, left, right):
        """Override the inherited lessThan method.

        The ideal sorting mechanism is expected to...
            A) Always prioritize items matching the search pattern.
            B) Followed by the non-matching items.
            C) Both must always be sorted in ascending order.

        See class docstring for more details.
        """
        # Get the items from the source modules.
        l_item = self.sourceModel().itemFromIndex(left)
        r_item = self.sourceModel().itemFromIndex(right)

        # Get the values from the item.
        # Ascii comparisons will prioritize uppercase over lowercase,
        # which can mess up our intended order.
        # We don't want this, so let's force a lowercase comparison instead.
        # E.g. Original list: ['cat', 'con', 'Zoo', 'Cave']
        #   - Incorrect sort (mixed case): ['Cave', 'Zoo', 'cat', 'con']
        #   - Correct sort (forced lowercase): ['cat', 'Cave', 'con', 'Zoo']
        l_data = l_item.data(DISPLAY_ROLE).lower()
        r_data = r_item.data(DISPLAY_ROLE).lower()

        is_l_match = self.__is_match_for_search_query(l_item)
        is_r_match = self.__is_match_for_search_query(r_item)

        # Left items matching search pattern will always be less than
        # non-matching right items.
        # This will ensure matching items get priority in list.
        if is_l_match and not is_r_match:
            return True

        # Non-matching left items will always be greater than matching right
        # items.
        # This will ensure non-matching items never get re-order priority
        # over matching items.
        if not is_l_match and is_r_match:
            return False

        # Now that priorities have been established, all other comparisons are
        # sorted in ascending order.
        return l_data < r_data

    # Private.
    def __is_match_for_search_query(self, item):
        """Checks the item against the search regex, to determine if it's a
        match.

        Sets the data on the item so it's available to the delegate for
        styling.

        Note:
            Initially there was a signal being emitted here, to notify the
            associated QListView that a comparison was performed.
            Unfortunately, due to the frequency of comparisons performed
            with larger data sets, this put a significant strain on the
            event loop and overall performance.
            Now I'm updating the item data directly in the proxy.

        Args:
            item (QtGui.QStandardItem): The current item being compared.

        Returns:
            bool: True if item matches search regex, otherwise False.
        """
        data = item.data(DISPLAY_ROLE).lower()
        is_match = self.__search_query_regex.exactMatch(data)

        # Set the sorting role data on the item, so it's available to the
        # delegate for styling.
        item.setData(is_match, SORTING_MATCH_ROLE)

        return is_match

    # Public.
    def sort_by_match(self, search_text):
        """Sort the proxy model with the provided text.

        Args:
            search_text (str): The text pattern to sort tags by.

        """
        # Make sure any Regex special characters are escaped.
        search_text = self.__search_query_regex.escape(search_text)

        # Search pattern to find tags is a fixed word anywhere in the string.
        # I'm intentionally enforcing wildcards as I want to find any
        # matching text within a tag.
        search_pattern = '.*{pat}.*'.format(pat=search_text) if search_text \
            else '.*'

        self.__search_query_regex.setPattern(search_pattern)

        # Start sorting: Sorting won't trigger lessThan, unless more than one
        # item exists in the model.
        # Since delegate painting relies on SORTING_MATCH_ROLE, we need to
        # account for single item models, so that searching re-paints the
        # delegate appropriately. Otherwise the item's SORTING_MATCH_ROLE
        # will stay False until a second item is added and allows lessThan
        # to trigger.
        self.invalidate()
        if self.rowCount() == 1:
            src_index = self.mapToSource(self.index(0, 0))
            item = self.sourceModel().itemFromIndex(src_index)

            self.__is_match_for_search_query(item)
        else:
            self.sort(0)
