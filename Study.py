import sys
import random
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import*
from PyQt5 import QtGui
from PyQt5 import QtCore
from JsonParse import JsonList


class StudySet(JsonList):
    """
    Creates sets based on JsonDict

    For settings:
    {
    "Dark Mode" = True/False
    "Full Screen" = True/False
    "Study Type" = One of 6 modes:
        "View"
        "Alter"
        "AnswerSimple"
        "AnswerRandom"
        "AnswerLearn"
        "AnswerLearnRandom"
    "MostRecentSets": [
        Newest is first, oldest is last
    ]
        5 cycles out, 4->5
    }
    """

    shuffled_set = []

    def __init__(self, file_name):
        super().__init__(file_name)

    def create_shuffled_set(self):
        # TODO implement this method
        pass


class ViewLayout(QWidget):
    def __init__(self, main_window, dark_mode, current_set, current_index):
        # Initializes through QMainWindow class
        super().__init__()
        self.main_window = main_window
        self.current_set = current_set
        self.current_index = current_index
        self.flip_view = True
        self.key_up = True

        if dark_mode:
            self.current_style = "color: white; font-size: 20px "
        if not dark_mode:
            self.current_style = "color: black; font-size: 20px "

        self.create_buttons()
        self.create_layout()

    def set_current_set(self, new_set):
        self.current_set = new_set
        self.set_dialog()

    def set_current_index(self, new_index):
        self.current_index = new_index
        self.set_dialog()

    def get_current_index(self):
        return self.current_index

    def create_buttons(self):
        self.change_layout = self.create_push_buttons("Switch", 100)
        self.dialog = self.create_label("", 70)
        self.flip = self.create_push_buttons("Flip", 400)
        self.first = self.create_push_buttons("First", 100)
        self.back = self.create_push_buttons("Previous", 100)
        self.forward = self.create_push_buttons("Next", 100)
        self.last = self.create_push_buttons("Last", 100)

    def create_layout(self):
        self.hbox0 = QHBoxLayout()
        self.hbox0.addWidget(self.change_layout)
        self.hbox0.addStretch(1)

        self.hbox1 = QHBoxLayout()
        self.hbox1.addStretch(1)
        self.hbox1.addWidget(self.dialog)
        self.hbox1.addStretch(1)

        self.hbox2 = QHBoxLayout()
        self.hbox2.addStretch(1)
        self.hbox2.addWidget(self.flip)
        self.hbox2.addStretch(1)

        self.hbox3 = QHBoxLayout()
        self.hbox3.addStretch(1)
        self.hbox3.addWidget(self.first)
        self.hbox3.addWidget(self.back)
        self.hbox3.addWidget(self.forward)
        self.hbox3.addWidget(self.last)
        self.hbox3.addStretch(1)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox0)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addStretch(2)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.hbox3)

        self.setLayout(self.vbox)

        self.change_layout.clicked.connect(self.change_layout_pressed)
        self.first.clicked.connect(self.first_pressed)
        self.back.clicked.connect(self.back_pressed)
        self.forward.clicked.connect(self.forward_pressed)
        self.last.clicked.connect(self.last_pressed)
        self.flip.clicked.connect(self.flip_pressed)

    def create_push_buttons(self, text, minimum_width):
        temp_button = QPushButton(text)
        temp_button.setFlat(True)
        temp_button.setMinimumWidth(minimum_width)
        temp_button.setStyleSheet(self.current_style)
        return temp_button

    def create_label(self, text, height):
        temp_label = QLabel(text)
        temp_label.setFixedHeight(height)
        temp_label.setStyleSheet(self.current_style)
        return temp_label

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            self.first_pressed()
        elif event.key() == Qt.Key_W:
            self.back_pressed()
        elif event.key() == Qt.Key_E:
            self.forward_pressed()
        elif event.key() == Qt.Key_R:
            self.last_pressed()
        elif event.key() == Qt.Key_F:
            self.flip_pressed()
        elif event.key() == Qt.Key_S:
            self.change_layout_pressed()
        elif event.key() == Qt.Key_O:
            self.main_window.open_new_set()
        event.accept()

    def set_dialog(self):
        if self.current_set.return_length_list() == 0:
            self.current_index = 0
            self.dialog.setText("There are no more values in this set")
        elif self.current_index > self.current_set.return_length_list() - 1:
            if self.current_index > self.current_set.return_length_list():
                self.current_index -= 1
            self.dialog.setText("There are no more values in this set")
        elif self.current_index < 0:
            if self.current_index < -1:
                self.current_index += 1
            self.dialog.setText("There are no more values in this set")
        else:
            if self.flip_view:
                if self.key_up:
                    self.dialog.setText(self.current_set.return_list_key(self.current_index))
                else:
                    self.dialog.setText(self.current_set.return_list_value(self.current_index))
            if not self.flip_view:
                return_string = self.current_set.return_list_key(self.current_index) + "\n\n" + \
                                self.current_set.return_list_value(self.current_index)
                self.dialog.setText(return_string)

    def change_layout_pressed(self):
        self.key_up = True
        self.flip_view = not self.flip_view
        if not self.flip_view:
            self.flip.hide()
        if self.flip_view:
            self.flip.show()
        self.set_dialog()

    def first_pressed(self):
        self.key_up = True
        self.current_index = 0
        self.set_dialog()

    def forward_pressed(self):
        self.key_up = True
        self.current_index += 1
        self.set_dialog()

    def back_pressed(self):
        self.key_up = True
        self.current_index -= 1
        self.set_dialog()

    def last_pressed(self):
        self.key_up = True
        self.current_index = self.current_set.return_length_list() - 1
        self.set_dialog()

    def flip_pressed(self):
        self.key_up = not self.key_up
        self.set_dialog()


class AlterLayout(QWidget):
    def __init__(self, main_window, dark_mode, current_set, current_index):
        # Initializes through QMainWindow class
        super().__init__()
        self.main_window = main_window
        self.current_set = current_set


class AnswerLayout(QWidget):
    def __init__(self, main_window, dark_mode, current_set, current_index):
        # Initializes through QMainWindow class
        super().__init__()
        self.current_set = current_set
        self.study_type = None

        QtWidgets.QTextEdit.setFont(self, QtGui.QFont("Gadugi", 15))
        QtWidgets.QLabel.setFont(self, QtGui.QFont("Gadugi", 15))
        self.key = QTextEdit()
        self.key.setMaximumHeight(50)
        self.value = QTextEdit()
        self.value.setMaximumHeight(50)
        self.dialog = QLabel()
        self.dialog.setFixedHeight(70)

        self.forward = QPushButton("Next")
        self.forward.setFlat(True)
        self.forward.setMinimumWidth(200)
        self.back = QPushButton("Previous")
        self.back.setFlat(True)
        self.back.setMinimumWidth(200)

        self.show_answer = QPushButton("Show Answer")
        self.show_answer.setMinimumWidth(200)
        self.skip = QPushButton("Skip")
        self.skip.setMinimumWidth(200)
        self.stupid_machine = QPushButton("I don ben rite")
        self.stupid_machine.setMinimumWidth(200)

        self.forward = QPushButton("Next")
        self.forward.setMinimumWidth(200)
        self.back = QPushButton("Previous")
        self.back.setMinimumWidth(200)

        self.add_value = QPushButton("Add")
        self.add_value.setMinimumWidth(200)
        self.delete_value = QPushButton("Delete")
        self.delete_value.setMinimumWidth(200)

        hbox3 = QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addWidget(self.dialog)
        hbox3.addStretch(1)

        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(self.key)
        hbox2.addStretch(1)
        hbox2.addWidget(self.value)
        hbox2.addStretch(1)

        hbox15 = QHBoxLayout()
        hbox15.addStretch(1)
        hbox15.addWidget(self.back)
        hbox15.addWidget(self.forward)
        hbox15.addStretch(1)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.delete_value)
        hbox.addStretch(2)
        hbox.addWidget(self.add_value)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox3)
        vbox.addStretch(1)
        vbox.addLayout(hbox2)
        vbox.addStretch(1)
        vbox.addLayout(hbox15)
        vbox.addStretch(3)
        vbox.addLayout(hbox)
        vbox.addStretch(0)

        self.forward.clicked.connect(self.switch_input_box)
        self.back.clicked.connect(self.switch_input_box)
        self.add_value.clicked.connect(self.switch_input_box)
        self.delete_value.clicked.connect(self.switch_input_box)

        self.setLayout(vbox)

    def change_study_type(self, mode):
        self.study_type = mode

        if self.study_type == "Find":
            pass
        if self.study_type == "Normal":
            pass
        if self.study_type == "Random":
            pass
        if self.study_type == "Ordered learn":
            pass
        if self.study_type == "Randomized learn":
            pass

    def switch_input_box(self):
        pass


class Studying(QMainWindow):
    """
    Central class in the program: is called when program is first launched
    Responsible for switching between the different layouts, and for communicating with StudySet
    """

    study_type = None
    settings = None
    dark_mode = None
    current_set = None
    current_index = -1
    set_folder = 'C:/Users/Laptop babyyy/Dropbox/Everything/Programming/PyCharm/Personal/Study/StudySets/'
    settings_file = 'SavedSettings.json'
    blank_file = 'Blank.json'
    settings_location = set_folder + settings_file
    blank_file_location = set_folder + blank_file

    def __init__(self):
        # Initializes through QMainWindow class
        super().__init__()

        # Sets basic elemnts of application
        self.resize(600, 300)
        self.center()
        self.setWindowTitle("StudyTimeGangYEEThãhã")

        # Opens settings file, as well as current set
        self.settings = StudySet(self.settings_location)
        self.current_set = StudySet(self.blank_file_location)

        self.dark_mode = False

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.view_layout_light = ViewLayout(self, False, self.current_set, self.current_index)
        self.answer_layout_light = AnswerLayout(self, False, self.current_set, self.current_index)
        self.alter_layout_light = AlterLayout(self, False, self.current_set, self.current_index)
        self.view_layout_dark = ViewLayout(self, True, self.current_set, self.current_index)
        self.answer_layout_dark = AnswerLayout(self, True, self.current_set, self.current_index)
        self.alter_layout_dark = AlterLayout(self, True, self.current_set, self.current_index)

        self.central_widget.addWidget(self.view_layout_light)
        self.central_widget.addWidget(self.answer_layout_light)
        self.central_widget.addWidget(self.alter_layout_light)
        self.central_widget.addWidget(self.view_layout_dark)
        self.central_widget.addWidget(self.answer_layout_dark)
        self.central_widget.addWidget(self.alter_layout_dark)

        # Icon stuff
        temp_icon = self.set_folder + "studyicon.png"
        app_icon = QtGui.QIcon()
        app_icon.addFile(temp_icon, QtCore.QSize(16, 16))
        app_icon.addFile(temp_icon, QtCore.QSize(24, 24))
        app_icon.addFile(temp_icon, QtCore.QSize(32, 32))
        app_icon.addFile(temp_icon, QtCore.QSize(48, 48))
        app_icon.addFile(temp_icon, QtCore.QSize(256, 256))
        app.setWindowIcon(app_icon)

        # Creates basics of menu bar
        menubar = self.menuBar()
        study_set = menubar.addMenu("Study Sets")
        study_options = menubar.addMenu("Studying Options")
        preferences = menubar.addMenu("Preferences")

        # TODO rewrite So it opens file explorer to find new files
        #         but has 5 most recently opened files listed
        study_set_other = QAction("Other Sets", self)
        study_set_add = QAction("Add New Set", self)

        study_set.addAction(study_set_other)
        study_set.addAction(study_set_add)

        # Adds options to study menu
        show_value = QAction("View mode", self)
        alter_value = QAction("Alter mode", self)
        study_find = QAction("Find matching value", self)
        study_value = QAction("Study normal", self)
        study_rand = QAction("Random study", self)
        study_mastery = QAction("Ordered learn study", self)
        study_mastery_rand = QAction("Randomized learn study", self)

        study_options.addAction(show_value)
        study_options.addAction(alter_value)
        study_options.addAction(study_find)
        study_options.addAction(study_value)
        study_options.addAction(study_rand)
        study_options.addAction(study_mastery)
        study_options.addAction(study_mastery_rand)

        # Adds options to preferences menu
        dark_mode = QAction("DarkkModeGANG", self, checkable=True)
        reset_preferences = QAction("Reset Preferences", self)

        preferences.addAction(dark_mode)
        preferences.addAction(reset_preferences)

        # Triggers respective study set methods when menu is pressed
        study_set_other.triggered.connect(self.open_new_set)
        study_set_add.triggered.connect(self.create_new_set)
        # Triggers respective study options methods when menu is pressed
        show_value.triggered.connect(self.study_type_view)
        alter_value.triggered.connect(self.study_type_alter)
        study_find.triggered.connect(self.study_type_find)
        study_value.triggered.connect(self.study_type_value)
        study_rand.triggered.connect(self.study_type_random)
        study_mastery.triggered.connect(self.study_type_mastery)
        study_mastery_rand.triggered.connect(self.study_type_mastery_rand)
        # Triggers respective preferences methods when menu is pressed
        dark_mode.triggered.connect(self.switch_color_mode)
        reset_preferences.triggered.connect(self.default_settings)

        self.current_layout = self.view_layout_light
        self.study_type_view()

    def default_settings(self):
        temp_set = StudySet(self.settings_location)
        temp_set.clear_json()
        temp_set.add_to_json("Dark Mode", False)
        temp_set.add_to_json("Full Screen", False)
        temp_set.add_to_json("Study Type", "View")
        temp_set.add_to_json("Most Recent Sets", [])
        self.settings = temp_set

    def open_new_set(self):
        file_name = QFileDialog.getOpenFileName(None, directory=self.set_folder)
        if file_name != ('', ''):
            self.current_index = -1
            self.current_set = StudySet(file_name[0])
            self.current_layout.set_current_set(self.current_set)

    def create_new_set(self):
        text, ok_pressed = QInputDialog.getText(
            self, " ", "Name of new set:", QLineEdit.Normal, "", Qt.FramelessWindowHint)
        if ok_pressed and text != '':
            new_set_location = self.set_folder + text + '.json'
            self.current_set = StudySet(new_set_location)

    def change_study_type(self, light_name, dark_name):
        self.light_name = light_name
        self.dark_name = dark_name
        temp_index = self.current_layout.get_current_index()
        if self.dark_mode:
            self.current_layout = dark_name
        if not self.dark_mode:
            self.current_layout = light_name
        self.current_layout.set_current_index(temp_index)
        self.current_layout.set_current_set(self.current_set)
        self.central_widget.setCurrentWidget(self.current_layout)
        self.show()

    def study_type_view(self):
        """
        Mode 0
        Changes screen format to allow looking through all values inputted
        Is used to go through data entered, not alter or study it by inputting the answer
        Buttons at the bottom: 3: Next, previous, delete currently visible item from set
        """
        print("mode 0")
        self.change_study_type(self.view_layout_light, self.view_layout_dark)

    def study_type_alter(self):
        """
        Mode 1
        Changes screen format to allow adding of values
        Format is most different out of all, creates a scrolling line of keys and values
        X on the right of the values, pressing x deletes pair, pressing key or value allows respective modification
        At top is the add/delete value button
        Switch button between key and value allows the two to be switched
        """
        print("mode 1")
        self.change_study_type(self.alter_layout_light, self.alter_layout_dark)

    def study_type_find(self):
        """
        Mode 2
        Allows the user to find the matching key to a value or vice versa
        Allows the app to be used as a tool to search through the inputted list
        """
        print("mode 2")
        self.change_study_type(self.answer_layout_light, self.answer_layout_dark)
        self.current_layout.change_study_type("Find")

    def study_type_value(self):
        # Mode 3
        print("mode 3")
        self.change_study_type(self.answer_layout_light, self.answer_layout_dark)
        self.current_layout.change_study_type("Normal")

    def study_type_random(self):
        # Mode 4
        print("mode 4")
        self.change_study_type(self.answer_layout_light, self.answer_layout_dark)
        self.current_layout.change_study_type("Random")

    def study_type_mastery(self):
        # Mode 5
        print("mode 5")
        self.change_study_type(self.answer_layout_light, self.answer_layout_dark)
        self.current_layout.change_study_type("Ordered learn")

    def study_type_mastery_rand(self):
        # Mode 6
        print("mode 6")
        self.change_study_type(self.answer_layout_light, self.answer_layout_dark)
        self.current_layout.change_study_type("Randomized learn")

    def switch_color_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.setStyleSheet("color: white; background-color: rgb(36, 2, 52); ")
        if not self.dark_mode:
            self.setStyleSheet("color: black; background-color: white; ")
        self.change_study_type(self.light_name, self.dark_name)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        self.settings.save_to_json_file()
        self.current_set.save_to_json_file()
        print("goodbye")
        event.accept()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    study_gang = Studying()
    sys.exit(app.exec())
