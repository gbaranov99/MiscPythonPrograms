import time
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import*
from PyQt5.QtWidgets import*
from PyQt5 import QtGui
from PyQt5 import QtCore
from JsonParse import JsonList


# Class that enables storage of time-tracking data through the use of an external json file
class DataStorage:
    def __init__(self, file_name):
        pass


# Standard timer, with start, stop and time adjustment
class TimerWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.timer_running = False  # Used to keep track of which buttons to show (start / stop)
        self.main_window = main_window  # Reference to window class for timer functionality

        # Two separate layouts for time display: buttons when timer is stopped to allow time adjustment,
        # labels for when timer is running, and start and stop buttons that switch
        self.seconds_button = self.create_push_buttons("", 40, True)
        self.minutes_button = self.create_push_buttons("", 40, True)
        self.hours_button = self.create_push_buttons("", 40, True)
        self.start = self.create_push_buttons("Start", 100, False)
        self.stop = self.create_push_buttons("Stop", 100, False)

        self.category_label = self.create_label("Category")
        self.seconds_label = self.create_label("")
        self.minutes_label = self.create_label("")
        self.hours_label = self.create_label("")

        # QStackedWidget allows for switching between labels and buttons for time and for start / stop switching
        self.seconds_stack = QStackedWidget()
        self.seconds_stack.addWidget(self.seconds_button)
        self.seconds_stack.addWidget(self.seconds_label)

        self.minutes_stack = QStackedWidget()
        self.minutes_stack.addWidget(self.minutes_button)
        self.minutes_stack.addWidget(self.minutes_label)

        self.hours_stack = QStackedWidget()
        self.hours_stack.addWidget(self.hours_button)
        self.hours_stack.addWidget(self.hours_label)

        self.start_stop_stack = QStackedWidget()
        self.start_stop_stack.addWidget(self.start)
        self.start_stop_stack.addWidget(self.stop)

        self.display_divider = self.create_label(":")
        self.display_divider1 = self.create_label(":")

        # Layouts that display time, category and the start / stop button
        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addWidget(self.hours_stack)
        hbox1.addWidget(self.display_divider)
        hbox1.addWidget(self.minutes_stack)
        hbox1.addWidget(self.display_divider1)
        hbox1.addWidget(self.seconds_stack)
        hbox1.addStretch(1)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.category_label)
        hbox2.addStretch(2)
        hbox2.addWidget(self.start_stop_stack)
        hbox2.addStretch(4)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox1)
        vbox.addStretch(1)
        vbox.addLayout(hbox2)

        self.setLayout(vbox)

        # Functions that call methods when the buttons on screen are clicked
        self.hours_button.clicked.connect(self.hours_pressed)
        self.minutes_button.clicked.connect(self.minutes_pressed)
        self.seconds_button.clicked.connect(self.seconds_pressed)
        self.start.clicked.connect(self.start_pressed)
        self.stop.clicked.connect(self.stop_pressed)

        self.time_limit = 3000
        self.time_left = self.time_limit
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.pupdate()

    def start_pressed(self):
        self.switch_buttons()
        self.pstart()

    def stop_pressed(self):
        self.time_left = self.time_limit
        self.switch_buttons()
        self.ptimer.stop()
        self.pupdate()

    def pstart(self):
        self.time_left = self.time_limit

        self.ptimer = QTimer(self)
        self.ptimer.timeout.connect(self.ptimeout)
        self.ptimer.start(1000)

    def ptimeout(self):
        self.time_left -= 1

        if self.time_left == 0:
            self.stop_pressed()
        self.pupdate()

    def update_limit(self):
        self.time_limit = self.hours * 3600 + self.minutes * 60 + self.seconds
        self.time_left = self.time_limit
        self.pupdate()

    def pupdate(self):
        hours = self.time_left // 3600
        minutes = self.time_left % 3600
        minutes = minutes // 60
        seconds = self.time_left - minutes * 60 - hours * 3600

        hours = str(hours)
        if len(hours) == 1:
            hours = "0" + hours
        minutes = str(minutes)
        if len(minutes) == 1:
            minutes = "0" + minutes
        seconds = str(seconds)
        if len(seconds) == 1:
            seconds = "0" + seconds

        self.update_time(hours, minutes, seconds)

    # Switches labels to buttons for time and start to stop or vice versa, depending on if timer is running
    # If timer is running: labels for time and Stop button
    # If timer is not running: buttons for time and Start button
    def switch_buttons(self):
        self.timer_running = not self.timer_running

        if self.timer_running:
            temp_index = 1
        else:
            temp_index = 0

        self.start_stop_stack.setCurrentIndex(temp_index)
        self.hours_stack.setCurrentIndex(temp_index)
        self.minutes_stack.setCurrentIndex(temp_index)
        self.seconds_stack.setCurrentIndex(temp_index)

    # Allows window class to update the category if it is changed
    def update_category(self, new_category):
        self.category_label.setText(new_category)

    # Allows window class to update time as the timer counts down
    def update_time(self, hours, minutes, seconds):

        self.hours_label.setText(hours)
        self.minutes_label.setText(minutes)
        self.seconds_label.setText(seconds)

        self.hours_button.setText(hours)
        self.minutes_button.setText(minutes)
        self.seconds_button.setText(seconds)

    # Method that asks the user to enter a value to replace the current value on button
    def prompt_time(self, output_string):
        text, ok_pressed = QInputDialog.getText(
            self, " ", output_string, QLineEdit.Normal, "", Qt.FramelessWindowHint)
        if ok_pressed:
            return text
        else:
            return None

    # Methods called when user presses hour, minute or second button
    def hours_pressed(self):
        new_hours = self.prompt_time("Enter new hour value: ")
        if new_hours is not None and new_hours.isdigit():
            self.hours = int(new_hours)
            self.update_limit()

    def minutes_pressed(self):
        new_minutes = self.prompt_time("Enter new minutes value: ")
        if new_minutes is not None and new_minutes.isdigit():
            self.minutes = int(new_minutes)
            self.update_limit()

    def seconds_pressed(self):
        new_seconds = self.prompt_time("Enter new seconds value: ")
        if new_seconds is not None and new_seconds.isdigit():
            self.seconds = int(new_seconds)
            self.update_limit()

    # Creates push buttons in a specified style
    @staticmethod
    def create_push_buttons(text, minimum_width, flat_status):
        temp_button = QPushButton(text)
        temp_button.setFlat(flat_status)
        temp_button.setMinimumWidth(minimum_width)
        temp_button.setStyleSheet("color: Black; font-size: 20px ")
        return temp_button

    # Creates labels in a specified style
    @staticmethod
    def create_label(text):
        temp_label = QLabel(text)
        temp_label.setAlignment(Qt.AlignCenter)
        temp_label.setStyleSheet("color: Black; font-size: 20px")
        return temp_label


# QWidget that allows viewing and selection of a category to which record time tracked data
class CategoryWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        pass


# QWidget that allows the viewing of time-tracking data with graphs, and allows insertion of uncollected data
class DataViewer(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        pass


class TimerWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(400, 200)
        self.center()

        self.timer_widget = TimerWidget(self)
        self.category_widget = CategoryWidget(self)
        self.data_widget = DataViewer(self)
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.stack.addWidget(self.timer_widget)
        self.stack.addWidget(self.category_widget)
        self.stack.addWidget(self.data_widget)
        self.stack.setCurrentIndex(0)

        self.setWindowTitle("TimeGangYEEThãhã")
        set_folder = 'C:/Users/Laptop babyyy/Dropbox/Everything/Programming/PyCharm/Personal/Timer/'
        settings_file = 'TimerSettings.json'
        data_file = 'TimerData.json'
        self.settings_location = set_folder + settings_file
        self.data_location = set_folder + data_file

        self.settings = JsonList(self.settings_location)
        self.data = DataStorage(self.data_location)

        if self.settings.return_length_list() == 0:
            self.default_settings()
        else:
            pass  # Get settings out and into program

        self.menu_bar = self.menuBar()
        self.settings_bar = self.menu_bar.addMenu("Settings")

        self.category = QAction("Change category", self)
        self.data_viewer = QAction("View stored data", self)
        self.starting_time = QAction("Starting time", self)
        self.hide_menubar = QAction("Hide menubar", self, checkable=True)
        self.dark_mode = QAction("Dark Mode", self, checkable=True)
        self.reset_settings = QAction("Reset default settings", self)
        self.clear_data = QAction("Clear all data", self)

        self.settings_bar.addAction(self.category)
        self.settings_bar.addAction(self.data_viewer)
        self.settings_bar.addAction(self.starting_time)
        self.settings_bar.addAction(self.hide_menubar)
        self.settings_bar.addAction(self.dark_mode)
        self.settings_bar.addAction(self.reset_settings)
        self.settings_bar.addAction(self.clear_data)

        self.category.triggered.connect(self.category_pressed)
        self.data_viewer.triggered.connect(self.data_viewer_pressed)
        self.starting_time.triggered.connect(self.starting_time_pressed)
        self.hide_menubar.triggered.connect(self.hide_menubar_pressed)
        self.dark_mode.triggered.connect(self.dark_mode_pressed)
        self.reset_settings.triggered.connect(self.default_settings)
        self.clear_data.triggered.connect(self.clear_data_pressed)

        self.show()

    def timer_started(self):
        pass

    def timer_stopped(self):
        pass

    def category_pressed(self):
        self.stack.setCurrentIndex(1)

    def data_viewer_pressed(self):
        self.stack.setCurrentIndex(2)

    def starting_time_pressed(self):
        pass

    def hide_menubar_pressed(self):
        pass

    def dark_mode_pressed(self):
        pass

    def default_settings(self):
        temp_set = JsonList(self.settings_location)
        temp_set.clear_json()
        temp_set.add_to_json("Categories", [])
        temp_set.add_to_json("Starting time", 60)
        temp_set.add_to_json("Show menubar", True)
        temp_set.add_to_json("Dark mode", False)
        self.settings = temp_set

    def clear_data_pressed(self):
        pass

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        self.settings.save_to_json_file()
        print("goodbye")
        event.accept()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    timer_gang = TimerWindow()
    sys.exit(app.exec())
