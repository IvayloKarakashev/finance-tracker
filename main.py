from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5 import uic

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.setup_ui()

    def setup_ui(self):
        self.layout1 = uic.loadUi("finance_tracker.ui")
        self.layout2 = uic.loadUi("expense_categories.ui")

        self.central_widget.addWidget(self.layout1)
        self.central_widget.addWidget(self.layout2)

        self.layout1.dashboardButton.clicked.connect(self.switch_to_layout2)
        self.layout2.categoriesButton.clicked.connect(self.switch_to_layout1)

    def switch_to_layout1(self):
        self.central_widget.setCurrentWidget(self.layout1)

    def switch_to_layout2(self):
        self.central_widget.setCurrentWidget(self.layout2)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
