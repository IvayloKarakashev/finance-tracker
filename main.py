import sys

from PyQt5.QtCore import Qt, QAbstractListModel, QModelIndex
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QListView, QLineEdit, QListWidget
from PyQt5 import uic, QtGui

from expense_categories import ExpenseCategory


class ExpenseCategoryModel(QAbstractListModel):
    def __init__(self, categories=None):
        super().__init__()
        self.categories = categories or []

    def rowCount(self, parent=QModelIndex()):
        return len(self.categories)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.categories)):
            return None

        category = self.categories[index.row()]

        if role == Qt.DisplayRole:
            return category.name  # Display the category name

        return None  # Return None for other roles


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()  # Initialize UI elements

        # Define elements
        self.expenseCategoriesList = self.findChild(QListView, "expenseCategoriesList")

        self.dashboardButton = self.findChild(QPushButton, "dashboardButton")
        self.expenseCategoriesButton = self.findChild(QPushButton, "expenseCategoriesButton")
        self.expenseCategoryNameInput = self.findChild(QLineEdit, "expenseCategoryNameInput")
        self.addExpenseCategoryButton = self.findChild(QPushButton, "addExpenseCategoryButton")


        self.model = ExpenseCategoryModel()

        self.addExpenseCategoryButton.clicked.connect(self.add_expense_category)

    def add_expense_category(self):
        category_name_input = self.expenseCategoryNameInput.text()

        try:
            if category_name_input:
                # Check if the category already exists in the model
                if not any(cat.name == category_name_input for cat in self.model.categories):
                    # Create an ExpenseCategory object
                    expense_category = ExpenseCategory(category_name_input)

                    # Insert a row into the model
                    self.model.insertRow(len(self.model.categories))
                    index = self.model.index(len(self.model.categories) - 1)
                    self.model.setData(index, expense_category, Qt.DisplayRole)
                    self.model.categories.append(expense_category)
                    self.model.layoutChanged.emit()
                    self.expenseCategoriesList.setModel(self.model)

                    print(self.model.categories)
                else:
                    print("Category already exists.")
        except Exception as e:
            # Handle exceptions here (e.g., display an error message)
            print(f"An error occurred: {e}")

        self.expenseCategoryNameInput.clear()

            # Clear the QLineEdit after adding the category

    def setup_ui(self):
        uic.loadUi("expense_categories.ui", self)  # Load the .ui file and set up UI elements



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
