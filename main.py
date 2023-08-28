import sys

from PyQt5.QtCore import Qt, QAbstractListModel, QModelIndex
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QListView, QLineEdit, QListWidget, QDialog, \
    QDialogButtonBox
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


class AddCategoryDialog(QDialog):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add category")
        uic.loadUi("add_category_dialog.ui", self)  # Load the UI file
        self.model = model

        # Define elements
        self.nameLineEdit = self.findChild(QLineEdit, "nameLineEdit")
        self.descriptionLineEdit = self.findChild(QLineEdit, "descriptionLineEdit")
        self.budgetLineEdit = self.findChild(QLineEdit, "budgetLineEdit")
        self.expensesLineEdit = self.findChild(QLineEdit, "expensesLineEdit")
        self.buttonBox = self.findChild(QDialogButtonBox, "buttonBox")

        self.accepted.connect(self.add_expense_category)

    def add_expense_category(self):  # TODO: Add validation
        name = self.nameLineEdit.text()
        description = self.descriptionLineEdit.text()
        budget = float(self.budgetLineEdit.text())

        if not any(cat.name == name for cat in self.model.categories):
            # Create an ExpenseCategory object
            expense_category = ExpenseCategory(name, description, budget)
            self.model.insertRow(len(self.model.categories))
            index = self.model.index(len(self.model.categories) - 1)
            self.model.setData(index, expense_category, Qt.DisplayRole)
            self.model.categories.append(expense_category)
            self.model.layoutChanged.emit()

        else:
            print("Category already exists.")

        self.nameLineEdit.clear()



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


        # self.addExpenseCategoryButton.clicked.connect(self.add_expense_category)

    # def add_expense_category(self):
    #     category_name_input = self.expenseCategoryNameInput.text()
    #
    #     try:
    #         if category_name_input:
    #             # Check if the category already exists in the model
    #             if not any(cat.name == category_name_input for cat in self.model.categories):
    #                 # Create an ExpenseCategory object
    #                 expense_category = ExpenseCategory(category_name_input)
    #
    #                 # Insert a row into the model
    #                 self.model.insertRow(len(self.model.categories))
    #                 index = self.model.index(len(self.model.categories) - 1)
    #                 self.model.setData(index, expense_category, Qt.DisplayRole)
    #                 self.model.categories.append(expense_category)
    #                 self.model.layoutChanged.emit()
    #                 self.expenseCategoriesList.setModel(self.model)
    #
    #                 print(self.model.categories)
    #             else:
    #                 print("Category already exists.")
    #     except Exception as e:
    #         # Handle exceptions here (e.g., display an error message)
    #         print(f"An error occurred: {e}")

        # self.expenseCategoryNameInput.clear()

        # Clear the QLineEdit after adding the category

    def setup_ui(self):
        uic.loadUi("expense_categories.ui", self)  # Load the .ui file and set up UI elements
        self.model = ExpenseCategoryModel()
        self.expenseCategoriesList.setModel(self.model)
        self.addExpenseCategoryButton.clicked.connect(self.open_new_category_dialog)

    def open_new_category_dialog(self):
        dialog = AddCategoryDialog(self.model)
        dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
