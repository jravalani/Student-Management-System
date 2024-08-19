# each window in out application has to be a new class
# whether it be an insert box or an edit box
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import sys
import psycopg2


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 600)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon("icons/icons/add.png"), "Add Student", self)
        file_menu_item.addAction(add_student_action)
        add_student_action.triggered.connect(self.insert)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        search_action = QAction(QIcon("icons/icons/search.png"), "Search", self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search)

        delete_action = QAction("Delete", self)
        edit_menu_item.addAction(delete_action)
        delete_action.triggered.connect(self.delete)

        # creating a table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        # to remove the unassigned index colum just like pandas
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # creating toolbar and adding elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # creating statusbar and adding elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # detecting a cell click
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)
        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)


    def load_data(self):
        connection = psycopg2.connect(
            dbname="python_mega_course",  # Replace with your database name
            user="postgres",  # Replace with your PostgreSQL username
            password="root",  # Replace with your PostgreSQL password
            host="localhost",  # Replace with your database host (usually 'localhost')
            port="5432"
        )

        cursor = connection.cursor()
        print("Postgres Connection is open!")
        cursor.execute("SELECT * FROM students")
        result = cursor.fetchall()
        # populating the table
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        cursor.close()
        connection.close()
        print("Postgres Connection is close!")

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()
        

class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Record")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # add student name
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # add course list combo box
        self.course_list = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_list.addItems(courses)
        layout.addWidget(self.course_list)

        # add mobile number
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile Number")
        layout.addWidget(self.mobile)

        # add a submit button
        button = QPushButton("Register")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_list.itemText(self.course_list.currentIndex())
        mobile = self.mobile.text()
        connection = psycopg2.connect(
            dbname="python_mega_course",  # Replace with your database name
            user="postgres",  # Replace with your PostgreSQL username
            password="root",  # Replace with your PostgreSQL password
            host="localhost",  # Replace with your database host (usually 'localhost')
            port="5432"
        )

        cursor = connection.cursor()
        print("Postgres Connection is open!")
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES(%s, %s, %s)", (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Record")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("John Doe")
        layout.addWidget(self.search_bar)

        self.button = QPushButton("Search")
        self.button.clicked.connect(self.search)
        layout.addWidget(self.button)

    def search(self):
        name = self.search_bar.text()
        connection = psycopg2.connect(
            dbname="python_mega_course",  # Replace with your database name
            user="postgres",  # Replace with your PostgreSQL username
            password="root",  # Replace with your PostgreSQL password
            host="localhost",  # Replace with your database host (usually 'localhost')
            port="5432"
        )

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students WHERE name = %s", (name,))
        result = cursor.fetchall()
        print(result)
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            main_window.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Record")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("John Doe")
        layout.addWidget(self.search_bar)

        self.button = QPushButton("Delete Record")
        self.button.clicked.connect(self.delete)
        layout.addWidget(self.button)

    def delete(self):
        name = self.search_bar.text()
        connection = psycopg2.connect(
            dbname="python_mega_course",  # Replace with your database name
            user="postgres",  # Replace with your PostgreSQL username
            password="root",  # Replace with your PostgreSQL password
            host="localhost",  # Replace with your database host (usually 'localhost')
            port="5432"
        )

        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE name = %s", (name,))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Record")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # get student name from selected row
        index = main_window.table.currentRow()
        current_student_name = main_window.table.item(index, 1).text()

        # get id from selected row
        self.student_id = main_window.table.item(index, 0).text()

        # add student name
        self.student_name = QLineEdit(current_student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # add course list combo box
        course_name = main_window.table.item(index, 2).text()
        self.course_list = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_list.addItems(courses)
        self.course_list.setCurrentText(course_name)
        layout.addWidget(self.course_list)

        # add mobile number
        mobile_number = main_window.table.item(index, 3).text()
        self.mobile = QLineEdit(mobile_number)
        self.mobile.setPlaceholderText("Mobile Number")
        layout.addWidget(self.mobile)

        # add a submit button
        button = QPushButton("Edit")
        button.clicked.connect(self.edit_student)
        layout.addWidget(button)

    def edit_student(self):
        connection = psycopg2.connect(
            dbname="python_mega_course",  # Replace with your database name
            user="postgres",  # Replace with your PostgreSQL username
            password="root",  # Replace with your PostgreSQL password
            host="localhost",  # Replace with your database host (usually 'localhost')
            port="5432"
        )
        cursor = connection.cursor()
        cursor.execute("UPDATE students set name = %s, course = %s, mobile = %s WHERE id = %s",
                       (self.student_name.text(),
                        self.course_list.itemText(self.course_list.currentIndex()),
                        self.mobile.text(),
                        self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
