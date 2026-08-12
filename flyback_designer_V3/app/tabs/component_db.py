"""
tabs/component_db.py — Component database tab.

Browsable tables for:
  - Ferrite cores (E/ER/ETD series) with Ae, Aw, Ve, AL
  - Controllers (ICE2QR, VIPER35, …)
  - MOSFETs (900/1000 V CoolMOS, SuperJunction)
  - Schottky diodes for output

Data is loaded from JSON files via ComponentManager.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QTableWidget, QTableWidgetItem,
    QLabel, QHeaderView,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui  import QFont

from models.component_manager import ComponentManager


def _make_table(headers: list[str], data: list[dict]) -> QTableWidget:
    t = QTableWidget(len(data), len(headers))
    t.setHorizontalHeaderLabels(headers)
    t.verticalHeader().setVisible(False)
    t.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    t.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
    t.setAlternatingRowColors(True)
    t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
    t.horizontalHeader().setStretchLastSection(True)

    for r, row in enumerate(data):
        # row is a dict now for all components
        row_vals = list(row.values())
        for c, cell in enumerate(row_vals):
            # Format booleans nicely
            if isinstance(cell, bool):
                val_str = "Yes" if cell else "No"
            else:
                val_str = str(cell)
            item = QTableWidgetItem(val_str)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            t.setItem(r, c, item)
    return t


class ComponentDbTab(QWidget):
    """Tabbed component database browser."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.lay = QVBoxLayout(self)
        self.lay.setContentsMargins(8, 8, 8, 8)

        self.inner = QTabWidget()
        self.lay.addWidget(self.inner)
        
        self.note = QLabel(
            "Data is loaded from user database. Always verify against manufacturer datasheet "
            "before finalising component selection."
        )
        self.note.setWordWrap(True)
        self.note.setStyleSheet("color: #888; font-size: 11px; padding: 6px 0;")
        
        self.refresh()

    def refresh(self):
        """Reload data from ComponentManager and rebuild the tables."""
        # Clear existing tabs
        while self.inner.count() > 0:
            self.inner.removeTab(0)
            
        mgr = ComponentManager()
        
        # ── Cores ──────────────────────────────────────────────────
        cores_data = mgr.get_components("cores")
        cores_tbl = _make_table(
            ["Ref", "Geom", "Ae (mm²)", "Aw (mm²)", "Ap (mm⁴)", "Ve (mm³)", "AL (nH/t²)", "le (mm)", "ln (mm)", "Weight (g)", "µ core", "Window (mm)", "Pv"],
            cores_data
        )
        self.inner.addTab(cores_tbl, "Ferrite cores")

        # ── Controllers ────────────────────────────────────────────
        ctrl_data = mgr.get_components("controllers")
        ctrl_tbl = _make_table(
            ["Reference", "Manufacturer", "V_max (V)", "Package", "PSR", "Notes"],
            ctrl_data
        )
        self.inner.addTab(ctrl_tbl, "Controllers")

        # ── MOSFETs ────────────────────────────────────────────────
        mos_data = mgr.get_components("mosfets")
        mos_tbl = _make_table(
            ["Reference", "V_DS (V)", "Rds_on (mΩ)", "Package", "Qg (nC)"],
            mos_data
        )
        self.inner.addTab(mos_tbl, "MOSFETs")

        # Make sure note is at the bottom (remove if already there, add again)
        self.lay.removeWidget(self.note)
        self.lay.addWidget(self.note)
