import sys

from PyQt5.QtCore import Qt, QAbstractListModel, QModelIndex
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QListView, QLineEdit, QListWidget, QDialog, \
    QDialogButtonBox, QStackedWidget, QFrame, QWidget
from PyQt5 import uic, QtGui

from expense_categories import ExpenseCategory


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.dashboard_page = Dashboard()
        # uic.loadUI('finance_tracker.ui', self)
        self.central_widget.addWidget(self.dashboard_page)
        self.central_widget.setCurrentWidget(self.dashboard_page)

        self.nav_menu = NavWidget()
        self.central_widget.addWidget(self.nav_menu)
        uic.loadUi('navigation.ui', self)

        self.expense_categories_page = ExpenseCategories()
        self.central_widget.addWidget(self.expense_categories_page)

        # Navigation
        self.dashboard_button = self.findChild(QPushButton, "dashboardButton")
        self.expense_categories_button = self.findChild(QPushButton, "expenseCategoriesButton")

        self.dashboard_button.clicked.connect(self.go_to_dashboard)
        self.expense_categories_button.clicked.connect(self.go_to_expense_categories)

        # self.setup_ui()  # Initialize UI elements

        # TODO: Move these buttons to their respective views(classes)
        self.expenseCategoriesList = self.findChild(QListView, "expenseCategoriesList")
        self.expenseCategoryNameInput = self.findChild(QLineEdit, "expenseCategoryNameInput")
        self.addExpenseCategoryButton = self.findChild(QPushButton, "addExpenseCategoryButton")

    def go_to_dashboard(self):
        self.central_widget.setCurrentWidget(self.dashboard_page)

    def go_to_expense_categories(self):
        self.central_widget.setCurrentWidget(self.expense_categories_page)

        #  TODO: Implement these former setup_ui() features
        # Expense categories layout features
        # self.model = ExpenseCategoryModel()
        # self.expenseCategoriesList.setModel(self.model)
        # self.addExpenseCategoryButton.clicked.connect(self.open_new_category_dialog)

        # self.dashboardButton.clicked.connect(lambda: self.switch_to_layout(self.finance_tracker_layout))
        # self.expenseCategoriesButton.clicked.connect(lambda: self.switch_to_layout(self.expense_categories_layout))

    # def switch_to_layout(self, layout):
    #     self.central_widget.setCurrentWidget(uic.loadUi(layout))

    # def open_new_category_dialog(self):
    #     dialog = AddCategoryDialog(self.model)
    #     dialog.exec_()


class Dashboard(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('finance_tracker.ui', self)


class ExpenseCategories(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('expense_categories.ui', self)


class NavWidget(QFrame):
    def __init__(self):
        super().__init__()
        uic.loadUi('navigation.ui', self)


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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
