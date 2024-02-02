from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QStatusBar, \
    QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox, QToolBar, \
    QMessageBox
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
import sys
import sqlite3
import mysql.connector
from mysql.connector.errors import IntegrityError as ie


class ConnectDatabase():
    def __init__(self, host="localhost", user="root", password="9801333508", database="student_info"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connection_database(self):
        connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password,
                                             database=self.database)
        return connection


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
        about_action.triggered.connect(self.about_student_app)

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
        # add status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # delete a cell
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        for child in children:
            self.status_bar.removeWidget(child)

        self.status_bar.addWidget(edit_button)
        self.status_bar.addWidget(delete_button)

    def load_table(self):
        connection = ConnectDatabase().connection_database()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students")
        result = cursor.fetchall()
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

    def edit(self):
        edit = EditDialog()
        edit.exec()

    def delete(self):
        delete = DeleteDialog()
        delete.exec()

    def about_student_app(self):
        about = AboutStudent()
        about.exec()


class AboutStudent(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        about_student = """
        hello every one this give manage of time to maintain a student 
        it gives you a edit add and delete operation
        """
        self.setText(about_student)
        self.exec()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update STUDENT DETAIL")
        # height and width
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        # set layout
        layout = QVBoxLayout()
        # add name widget
        index = main.table.currentRow()
        # get student id
        self.student_id = main.table.item(index, 0).text()
        # get name of table
        name = main.table.item(index, 1).text()
        self.name = QLineEdit(name)
        self.name.setPlaceholderText("enter name hear")
        layout.addWidget(self.name)
        # add check box
        current_course = main.table.item(index, 2).text()
        self.course_box = QComboBox()
        course = ["Biology", "Science", "Math", "Psychology", "Commerce", "Physics", "Astronomy"]
        self.course_box.addItems(course)
        self.course_box.setCurrentText(current_course)
        layout.addWidget(self.course_box)
        # Add mobile box
        mobile = main.table.item(index, 3).text()
        self.mobile = QLineEdit(mobile)
        self.mobile.setPlaceholderText("enter mobile number hear")
        layout.addWidget(self.mobile)

        # add button
        submit = QPushButton("update")
        submit.clicked.connect(self.update_student_data)
        layout.addWidget(submit)
        # add all widget to box layout
        self.setLayout(layout)

    def update_student_data(self):
        connection = ConnectDatabase().connection_database()
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name =%s,course = %s, mobile = %s where id =%s",
                       (self.name.text(), self.course_box.itemText(self.course_box.currentIndex()),
                        self.mobile.text(), self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        main.load_table()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete record")

        layout = QGridLayout()
        label = QLabel("Are you sure you want to delete")
        yes = QPushButton("YES")
        no = QPushButton("No")

        layout.addWidget(label, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)

        yes.clicked.connect(self.delete_student)

        self.setLayout(layout)

    def delete_student(self):
        index = main.table.currentRow()
        id = main.table.item(index, 0).text()
        connection = ConnectDatabase().connection_database()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students where id =%s", (id,))
        connection.commit()
        cursor.close()
        connection.close()
        main.load_table()

        self.close()

        message_box = QMessageBox()
        message_box.setWindowTitle("Success")
        message_box.setText("The record delete successfully")
        message_box.exec()


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
        connection = ConnectDatabase().connection_database()
        cursor = connection.cursor()
        name = self.name.text()
        course = self.course_box.itemText(self.course_box.currentIndex())
        mobile = self.mobile.text()
        try:
            cursor.execute("INSERT INTO students (name,course,mobile) VALUES(%s,%s,%s)",
                           (name, course, mobile))
            connection.commit()
            connection.close()
            main.load_table()
        except ie:
            warning_box = QMessageBox()
            warning_box.setWindowTitle("Warning")
            warning_box.setText("you enter duplicate data")
            warning_box.exec()


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
        connection = ConnectDatabase().connection_database()
        cursor = connection.cursor()
        name = self.search_name.text()
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
