# Import built-in modules.
import sys

# Import local modules.
from pyqt_tag_manager import QtCore
from pyqt_tag_manager import QtWidgets
from pyqt_tag_manager.qt_market import widget_vendor
from pyqt_tag_manager.tag_manager import TagManager
import mock_db


class TagManagerExampleWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(TagManagerExampleWindow, self).__init__(parent)
        self.setWindowTitle('Tag Manager Example')
        self.setGeometry(500, 250, 600, 1000)

        self.__build_ui()
        self.__mock_populate()

        self.show()

    def __build_ui(self):
        central_widget = QtWidgets.QWidget(self)
        main_layout = QtWidgets.QVBoxLayout(central_widget)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Testing UI for editing mode.
        # # Editor group.
        editing_grp = QtWidgets.QGroupBox(self)
        editing_grp.setTitle('EDITING/PUBLISH MODE:')

        editing_lyt = QtWidgets.QVBoxLayout()
        editing_grp.setLayout(editing_lyt)

        # # Description text.
        editing_txt = QtWidgets.QLabel(self)
        editing_txt.setText('Use this section to test out the sorting '
                            'functionality and to add/remove tags from '
                            'the TagManager widget below.\n'
                            '1) Input the name of a tag. Note how tags '
                            'are sorted and grouped according to the '
                            'matches.\n'
                            '2) When satisfied, press enter to add tag. '
                            'Existing tags cannot be added again.\n'
                            '3) Press the "Publish Tags" button to save the '
                            'changes to the mock database.')
        editing_lyt.addWidget(editing_txt)

        # # Editable Tag manager.
        self.editor_tag_manager = TagManager(self)
        editing_lyt.addWidget(self.editor_tag_manager)

        # # Publish.
        self.publish_tags_btn = QtWidgets.QPushButton('Publish Tags', self)
        editing_lyt.addWidget(self.publish_tags_btn)

        # Testing UI for preview mode.
        # # Preview group.
        prev_grp = QtWidgets.QGroupBox(self)
        prev_grp.setTitle('PREVIEW/QUERY MODE:')

        prev_lyt = QtWidgets.QVBoxLayout()
        prev_grp.setLayout(prev_lyt)

        # # Description text.
        prev_txt = QtWidgets.QLabel(self)
        prev_txt.setText('Use this section to query the tags from the mock '
                         'database and display them in the TagManager widget '
                         'below.\n'
                         '1) Press the "Refresh" button to load the tags from '
                         'the mock database.\n '
                         'Please note that the TagManager\'s editing '
                         'functionality is disabled in this section.')
        prev_lyt.addWidget(prev_txt)

        # # Preview only Tag manager.
        self.prev_tag_manager = TagManager(self)
        self.prev_tag_manager.enable_tag_preview_mode()
        prev_lyt.addWidget(self.prev_tag_manager)

        # # Refresh.
        self.refresh_tags_btn = QtWidgets.QPushButton('Refresh', self)
        prev_lyt.addWidget(self.refresh_tags_btn)

        # Update main layout.
        main_layout.addWidget(editing_grp)
        main_layout.addWidget(widget_vendor.get_empty_widget(self))
        main_layout.addWidget(widget_vendor.get_h_divider(self))
        main_layout.addWidget(widget_vendor.get_empty_widget(self))
        main_layout.addWidget(prev_grp)

        # Signals.
        self.publish_tags_btn.clicked.connect(self._on_tag_publish)
        self.refresh_tags_btn.clicked.connect(self._on_tag_refresh)

    def __mock_populate(self):
        tags = mock_db.get_published_tags_from_db()
        self.editor_tag_manager.add_tags(tags)
        self.prev_tag_manager.add_tags(tags)

    # Slots.
    @QtCore.Slot()
    def _on_tag_publish(self):
        conf_dialog = QtWidgets.QMessageBox.information(
            self,
            'Tags Published',
            'Publish was successful.\n'
            'Please switch over to the "PREVIEW/QUERY MODE" section below.'
        )

        tags = self.editor_tag_manager.get_tags()
        mock_db.publish_tags_to_db(tags)

    @QtCore.Slot()
    def _on_tag_refresh(self):
        db_tags = mock_db.get_published_tags_from_db()
        self.prev_tag_manager.clear_tags()
        self.prev_tag_manager.add_tags(db_tags)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = TagManagerExampleWindow()
    sys.exit(app.exec_())
