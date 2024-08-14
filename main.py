from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import sys
import psycopg2


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu_item = self.menuBar().addMenu("&File")
        Help_menu_item = self.menuBar().addMenu("&Help")

        add_student_action = QAction("Add Student", self)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        Help_menu_item.addAction(about_action)

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


app = QApplication(sys.argv)
SMS = MainWindow()
SMS.show()
SMS.load_data()
sys.exit(app.exec())
