"""
tabs/component_db.py — Component database tab.

Browsable tables for:
  - Ferrite cores (E/ER/ETD series) with Ae, Aw, Ve, AL
  - Controllers (ICE2QR, VIPER35, …)
  - MOSFETs (900/1000 V CoolMOS, SuperJunction)
  - Schottky diodes for output

Data is loaded from data/cores_db.json and data/controllers_db.json.
Currently shows placeholder tables; JSON loading to be added.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QTableWidget, QTableWidgetItem,
    QLabel, QHeaderView,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui  import QFont


CORES_DATA = [
    # ref,       Ae mm², Aw mm², Ve mm³,  AL nH/t², material
    ("E25/13/7",  52,    62,   2500,   250, "N87"),
    ("E30/15/7",  60,    115,  3400,   320, "N87"),
    ("E32/16/9",  83,    130,  4700,   350, "N87"),
    ("E36/18/11", 111,   175,  7200,   430, "N87"),
    ("E42/20/15", 178,   240,  14000,  590, "N97"),
    ("ETD29",     76,    100,  5470,   280, "N87"),
    ("ETD34",     97.1,  123,  7740,   355, "N87"),
    ("ETD39",     125,   177,  11500,  449, "N97"),
    ("RM10",      96,    35,   5600,   1900,"N87"),
]

CONTROLLERS_DATA = [
    # ref,             Manuf,     V_max V, pkg,    PSR, notes
    ("ICE2QR4565G",  "Infineon", 800,  "DIP8",  True,  "StackFET, 65 kHz, 4 W OB"),
    ("ICE5QR4780AG", "Infineon", 800,  "DIP8",  True,  "StackFET, 80 kHz, 5 W OB"),
    ("VIPER35HD",    "ST",       800,  "DIP8",  True,  "StackFET, 60 kHz"),
    ("VIPER35LD",    "ST",       800,  "SOP8",  True,  "StackFET, 60 kHz SMD"),
    ("NCP1379",      "ON Semi",  600,  "SOP8",  False, "CRM/DCM, external MOSFET"),
    ("LNK306P",      "PI",       700,  "DIP8",  True,  "LinkSwitch, 360 mA max"),
    ("TEA1721",      "NXP",      800,  "DIP8",  False, "SSR, external MOSFET"),
]

MOSFETS_DATA = [
    # ref,                 V_DS V, Rds_on mΩ, pkg,    Qg nC
    ("IPW90R120C3",        900,   120,  "TO247",  54),
    ("IPW90R250C3",        900,   250,  "TO247",  29),
    ("STW11NM80",          800,   420,  "TO247",  20),
    ("IPD60R385C7",        600,   385,  "TO252",  8),
    ("SPA07N65C3",         650,   570,  "TO220",  24),
    ("FCH072N65S3",        650,   72,   "TO247",  175),
]


def _make_table(headers: list[str], data: list[tuple]) -> QTableWidget:
    t = QTableWidget(len(data), len(headers))
    t.setHorizontalHeaderLabels(headers)
    t.verticalHeader().setVisible(False)
    t.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    t.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
    t.setAlternatingRowColors(True)
    t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
    t.horizontalHeader().setStretchLastSection(True)

    for r, row in enumerate(data):
        for c, cell in enumerate(row):
            item = QTableWidgetItem(str(cell))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            t.setItem(r, c, item)
    return t


class ComponentDbTab(QWidget):
    """Tabbed component database browser."""

    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(8, 8, 8, 8)

        inner = QTabWidget()
        lay.addWidget(inner)

        # ── Cores ──────────────────────────────────────────────────
        cores_tbl = _make_table(
            ["Reference", "Ae (mm²)", "Aw (mm²)", "Ve (mm³)", "AL (nH/t²)", "Material"],
            CORES_DATA
        )
        inner.addTab(cores_tbl, "Ferrite cores")

        # ── Controllers ────────────────────────────────────────────
        ctrl_tbl = _make_table(
            ["Reference", "Manufacturer", "V_max (V)", "Package", "PSR", "Notes"],
            CONTROLLERS_DATA
        )
        inner.addTab(ctrl_tbl, "Controllers")

        # ── MOSFETs ────────────────────────────────────────────────
        mos_tbl = _make_table(
            ["Reference", "V_DS (V)", "Rds_on (mΩ)", "Package", "Qg (nC)"],
            MOSFETS_DATA
        )
        inner.addTab(mos_tbl, "MOSFETs")

        note = QLabel(
            "Data is indicative. Always verify against manufacturer datasheet "
            "before finalising component selection."
        )
        note.setWordWrap(True)
        note.setStyleSheet("color: #888; font-size: 11px; padding: 6px 0;")
        lay.addWidget(note)
