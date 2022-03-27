import logging
import os

from Qt import QtWidgets, QtCore, QtGui
from Qt import _loadUi

from guiUtil.template import getTextDialog
from guiUtil import prompt

import shapeFile


MODULE_PATH = os.path.dirname(__file__)
UI_FILE = os.path.join(MODULE_PATH, 'shapeManager.ui')


class ShapeManager(QtWidgets.QMainWindow):

    def __init__(self, directory=shapeFile.SHAPE_PATH):
        super(ShapeManager, self).__init__()
        _loadUi(UI_FILE, self)

        self._dir = directory
        self._shapes = None

        self.force_refresh()

        # gui property
        self.icon_size = 150
        self.ui_shape_widget.setIconSize(QtCore.QSize(self.icon_size, self.icon_size))

        # context menu setup
        self.ui_shape_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui_shape_widget.customContextMenuRequested.connect(self.open_context_menu)

        # connect signal and slot
        self.ui_add_btn.clicked.connect(self.create)
        self.ui_icon_slider.valueChanged.connect(self.resize_icon)

    def open_context_menu(self):
        items = self.ui_shape_widget.selectedItems()
        if items:
            menu = QtWidgets.QMenu()

            import_action = menu.addAction("Import selected asset")
            delete_action = menu.addAction("Remove selected asset from entry")

            import_action.triggered.connect(lambda: self.load())
            delete_action.triggered.connect(lambda: self.delete_entry())

            cursor = QtGui.QCursor()
            menu.exec_(cursor.pos())

    def get_shapes(self):
        self._shapes = shapeFile.ShapeFile.get_from_dir(self._dir)

    def populate(self):
        self.ui_shape_widget.clear()

        for shape in self._shapes:
            item = QtWidgets.QListWidgetItem(shape.base)
            item.setIcon(QtGui.QIcon(shape.thumbnail))
            item.setData(QtCore.Qt.UserRole, shape)
            self.ui_shape_widget.addItem(item)

    def force_refresh(self):
        self.get_shapes()
        self.populate()

    def get_current_item(self):
        item = self.ui_shape_widget.currentItem()
        if not item:
            raise ValueError("No item selected for action")
        return item.data(QtCore.Qt.UserRole)

    def resize_icon(self):
        value = self.ui_icon_slider.value()
        self.icon_size = value
        self.ui_shape_widget.setIconSize(QtCore.QSize(self.icon_size, self.icon_size))

    def create(self):
        import maya.cmds as cmds

        if not cmds.ls(selection=1, type='transform'):
            logging.error("Selection Error")
            msg = "Please select curves transform to save"
            prompt.message_log(message=msg, ltype='error', title="Create Fail")
            return

        dialog = getTextDialog.GetTextDialog(title="Enter Name")
        if dialog.exec_():
            name = dialog.get_text()

            transform = cmds.ls(selection=1)[0]
            s = shapeFile.ShapeFile.fsave(transform, os.path.join(self._dir, name+'.json'))

            self.force_refresh()
            prompt.message_log("Creation Success", ltype='info')
        else:
            prompt.message_log("Aborted!", ltype='info')

    def load(self, item=None):
        if not item:
            item = self.get_current_item()
        item.fimport()

    def delete_entry(self):
        item = self.get_current_item()

        user_choice = prompt.message_yesno(
            "Delete the entry: {}?".format(item.name))
        if user_choice == QtWidgets.QMessageBox.No:
            return

        # delete the prop entry
        try:
            item.fdelete()
        except Exception as e:
            logging.error("deletion interrupted: %s", e)

        self.force_refresh()


def show():
    global window
    window = ShapeManager()
    window.show()
    return window


if __name__ == "__main__":
    window = show()
