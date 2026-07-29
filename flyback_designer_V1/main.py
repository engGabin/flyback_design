"""
main.py — Application entry point.

Usage:
    python main.py

Requirements:
    pip install PyQt6 pyqtgraph matplotlib PySpice

Optional (for LTSpice netlist simulation):
    pip install PySpice
    LTSpice XVII installed and on PATH
"""

import sys
import os

# Ensure the project root is on sys.path so `engine` and `ui` import cleanly
sys.path.insert(0, os.path.dirname(__file__))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore    import Qt
from PyQt6.QtGui     import QFont

from ui.main_window  import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Flyback Designer")
    app.setOrganizationName("SOCOMEC")

    # Consistent font across platforms
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    # High-DPI support (Qt6 enables this by default, explicit for clarity)
    app.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
