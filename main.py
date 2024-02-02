from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox, QToolBar
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Student Management System")
        self.setMinimumSize(600, 600)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        # search functionality
        edit_action = QAction(QIcon("icons/search.png"), "Search", self)
        edit_action.triggered.connect(self.search)
        edit_menu_item.addAction(edit_action)

        # add toolbar
        tool_bar = QToolBar()
        tool_bar.setMovable(True)
        self.addToolBar(tool_bar)

        tool_bar.addAction(add_student_action)
        tool_bar.addAction(edit_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def load_table(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM Students")
        self.table.setRowCount(0)
        for row_number, data in enumerate(result):
            self.table.insertRow(row_number)
            for colum_number, colum_data in enumerate(data):
                self.table.setItem(row_number, colum_number, QTableWidgetItem(str(colum_data)))

        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        search = SearchDialog()
        search.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ADD STUDENT DETAIL")
        # height and width
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        # set layout
        layout = QVBoxLayout()
        # add name widget
        self.name = QLineEdit()
        self.name.setPlaceholderText("enter name hear")
        layout.addWidget(self.name)
        # add check box
        self.course_box = QComboBox()
        course = ["biology", "science", "math", "psychology", "commerce"]
        self.course_box.addItems(course)
        layout.addWidget(self.course_box)
        # Add mobile box
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("enter mobile number hear")
        layout.addWidget(self.mobile)

        # add button
        submit = QPushButton("submit")
        submit.clicked.connect(self.insert_data)
        layout.addWidget(submit)
        # add all widget to box layout
        self.setLayout(layout)

    def insert_data(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        name = self.name.text()
        course = self.course_box.itemText(self.course_box.currentIndex())
        mobile = self.mobile.text()

        cursor.execute("INSERT INTO students (name,course,mobile) VALUES(?,?,?)",
                       (name, course, mobile))
        connection.commit()
        connection.close()
        main.load_table()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("search student data")
        self.setFixedWidth(400)
        self.setFixedHeight(400)

        layout = QVBoxLayout()

        # add search box
        self.search_name = QLineEdit()
        self.search_name.setPlaceholderText("student name...")
        layout.addWidget(self.search_name)

        # add search button
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search)
        layout.addWidget(search_button)

        # add label
        self.error_display = QLabel()
        layout.addWidget(self.error_display)

        self.setLayout(layout)

    def search(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        name = self.search_name.text()
        result = cursor.execute("SELECT * FROM students WHERE name= ?", (name,))
        items = main.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        if items.__len__() == 0:
            self.error_display.setText("match not found..")
        else:
            for item in items:
                if item:
                    main.table.item(item.row(), 1).setSelected(True)
        cursor.close()
        connection.close()


app = QApplication(sys.argv)
main = MainWindow()
main.show()
main.load_table()
sys.exit(app.exec())