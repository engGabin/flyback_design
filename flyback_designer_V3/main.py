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
from PyQt6.QtGui     import QFont, QPalette, QColor

from app.main_window  import MainWindow


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

    # ---------------------------------------------------------
    # NEW COLOR PALETTE (Fusion + QPalette)
    # ---------------------------------------------------------
    # Palette: 
    # 0D1321 (Very Dark Blue)
    # 1D2D44 (Dark Blue)
    # 3E5C76 (Medium Blue)
    # 748CAB (Light Blueish Gray)
    # F0EBD8 (Cream / Off-White)

    app.setStyle("Fusion")
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor("#1D2D44"))
    dark_palette.setColor(QPalette.ColorRole.WindowText, QColor("#F0EBD8"))
    dark_palette.setColor(QPalette.ColorRole.Base, QColor("#0D1321"))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#1D2D44"))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#1D2D44"))
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#F0EBD8"))
    dark_palette.setColor(QPalette.ColorRole.Text, QColor("#F0EBD8"))
    dark_palette.setColor(QPalette.ColorRole.Button, QColor("#3E5C76"))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor("#F0EBD8"))
    dark_palette.setColor(QPalette.ColorRole.BrightText, QColor("#748CAB"))
    dark_palette.setColor(QPalette.ColorRole.Link, QColor("#748CAB"))
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor("#3E5C76"))
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#F0EBD8"))
    app.setPalette(dark_palette)
    
    # Global stylesheet for specific tweaks
    app.setStyleSheet("""
        QToolTip { color: #F0EBD8; background-color: #3E5C76; border: 1px solid #748CAB; }
    """)
    # ---------------------------------------------------------
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
