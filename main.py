# each window in out application has to be a new class
# whether it be an insert box or an edit box

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import sys
import psycopg2


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        search_action = QAction("Search", self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

        # creating a table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        # to remove the unassigned index colum just like pandas
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

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
        SMS.load_data()


app = QApplication(sys.argv)
SMS = MainWindow()
SMS.show()
SMS.load_data()
sys.exit(app.exec())
