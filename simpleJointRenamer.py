# Simple Hierarchy Renamer created by konstap
# Created on 07/02/2021
import maya.cmds as cmds
from string import ascii_letters
from PySide2 import QtWidgets
import maya.OpenMayaUI as omu
import shiboken2 as sh


class SimpleJointRenamer():

    # Method returns a list of all objects that are children to the selected joint.
    # In conflicts method returns None and gives a respective warning.
    @staticmethod
    def __list_hierarchy():
        try:
            root = cmds.ls(sl=True)
            if not cmds.objectType(root, isType='joint'):
                cmds.warning('Selected object is not joint')
                return None
            cmds.select(root[0], hi=True)
            objects = cmds.ls(sl=True)
            # After listing all the joints in the hierarchy method will select joint that was selected first
            cmds.select(root)
            return objects
        except RuntimeError:
            cmds.warning('Nothing selected. Please select an object')
            return None

    # This method goes through joint hierarchy and depending on selected label uses either consecutive
    # alphabets or numbers in naming convention.
    # For hierarchy's last joint label is always 'END'.
    @staticmethod
    def __rename_hierarchy(objects, user_input, label):
        # With '/' user slice input text and insert consecutive label in between the input text.
        # Without '/' consecutive label will be added to the end of the input text.
        if '/' in user_input:
            user_mod = user_input.split('/')
        else:
            user_mod = [user_input, ""]
        last = len(objects) - 1
        char = ascii_letters[26:52]
        for obj, objects in enumerate(objects):
            if obj is last:
                name = user_mod[0] + 'END' + user_mod[1]
            elif label:
                name = user_mod[0] + char[obj] + user_mod[1]
            else:
                name = user_mod[0] + str(obj + 1) + user_mod[1]
            cmds.rename(objects, name)


    @staticmethod
    def run_renamer(user_input, label):
        objects = SimpleJointRenamer.__list_hierarchy()
        if objects:
            SimpleJointRenamer.__rename_hierarchy(objects, user_input, label)


# Returns Maya's main window for the Simple UI class.
# With out this Maya does not recognize our simpleUI window as part of Maya's UI.
def maya_main_window():
    main_window = omu.MQtUtil.mainWindow()
    return sh.wrapInstance(long(main_window), QtWidgets.QWidget)


class SimpleUI(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(SimpleUI, self).__init__(parent)
        self.setWindowTitle('Simple Joint Hierarchy Renamer')
        self.setFixedWidth(400)
        self.setFixedHeight(100)
        self.buildUI()

    def buildUI(self):
        # Here we create a a grid based layout for the window.
        # Grid layout uses cell coordinates in widget alignment.
        main_layout = QtWidgets.QGridLayout(self)
        infoLabel = QtWidgets.QLabel('Select a consecutive naming method for your hierarchy.')
        main_layout.addWidget(infoLabel, 0, 0)
        # These two radio buttons are used in selection of consecutive label for naming.
        self.radioAlpha = QtWidgets.QRadioButton('Alphabets')
        self.radioAlpha.setChecked(True)
        main_layout.addWidget(self.radioAlpha, 1, 0)
        radioNum = QtWidgets.QRadioButton('Numbers')
        main_layout.addWidget(radioNum, 1, 1)
        # Input field and rename button are the main functionality widgets in this UI.
        # These widgets are used for assigning naming convention for the joint hierarchy.
        self.inputField = QtWidgets.QLineEdit()
        self.inputField.setPlaceholderText('Use / to split your text. Eg. R_LEG_/_JNT')
        main_layout.addWidget(self.inputField, 2, 0)
        renameBtn = QtWidgets.QPushButton('Rename')
        main_layout.addWidget(renameBtn, 2, 1)
        renameBtn.clicked.connect(self.rename_clicked)

    def rename_clicked(self):
        SimpleJointRenamer.run_renamer(self.inputField.text(), self.radioAlpha.isChecked())

if __name__ == "__main__":
    # Destroys window if it exist already
    try:
        ui.close()
    except:
        pass
    # Creates a new window
    ui = SimpleUI()
    ui.show()