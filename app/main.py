from PyQt5.QtWidgets import QApplication
import sys
import ui
import utils


def main(argv: list[str]) -> None:
    app = QApplication(argv)
    form = ui.MainForm()
    form.show()
    sys.exit(app.exec())
