"""
widgets/common.py — Reusable UI building blocks for every design page.

Provides:
  - LabeledInput   : label + QDoubleSpinBox + unit label, in one row
  - SectionHeader  : bold grouping title with horizontal rule
  - ResultRow      : read-only label + value + unit (for computed outputs)
  - HLine          : plain horizontal separator
  - PageBase       : base class every design page should inherit from
"""

from PyQt6.QtWidgets import (
    QWidget, QLabel, QDoubleSpinBox, QHBoxLayout, QVBoxLayout,
    QFrame, QSizePolicy, QSpinBox,
)
from PyQt6.QtCore    import Qt, pyqtSignal
from PyQt6.QtGui     import QFont


# ────────────────────────────────────────────────────────────────────
# Horizontal rule
# ────────────────────────────────────────────────────────────────────

class HLine(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)


# ────────────────────────────────────────────────────────────────────
# Section header
# ────────────────────────────────────────────────────────────────────

class SectionHeader(QWidget):
    """Bold title + thin rule — visually groups related fields."""

    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(4)

        lbl = QLabel(title)
        font = QFont()
        font.setPointSize(11)
        font.setWeight(QFont.Weight.Bold)
        lbl.setFont(font)

        # on force une hauteur minimale pour empêcher PyQt de couper le texte
        lbl.setMinimumHeight(22)

        lay.addWidget(lbl)
        lay.addWidget(HLine())


# ────────────────────────────────────────────────────────────────────
# Labeled numeric input
# ────────────────────────────────────────────────────────────────────

class LabeledInput(QWidget):
    """
    One row: [label .............. ] [ spinbox ] [ unit ]

    Parameters
    ----------
    label    : field description
    unit     : physical unit string (e.g. "V", "µF", "kHz")
    min_val  : spinbox minimum
    max_val  : spinbox maximum
    decimals : decimal places
    default  : initial value
    tooltip  : optional hover text
    """

    value_changed = pyqtSignal(float)

    def __init__(
        self,
        label: str,
        unit: str = "",
        min_val: float = 0.0,
        max_val: float = 1e9,
        decimals: int = 3,
        default: float = 0.0,
        tooltip: str = "",
        parent=None,
    ):
        super().__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 2, 0, 2)
        lay.setSpacing(8)

        self._lbl = QLabel(label)
        self._lbl.setMinimumWidth(200)
        self._lbl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        if tooltip:
            self._lbl.setToolTip(tooltip)

        self._spin = QDoubleSpinBox()
        self._spin.setMinimum(min_val)
        self._spin.setMaximum(max_val)
        self._spin.setDecimals(decimals)
        self._spin.setValue(default)
        self._spin.setFixedWidth(110)
        self._spin.setAlignment(Qt.AlignmentFlag.AlignRight)
        self._spin.valueChanged.connect(self.value_changed.emit)

        self._unit = QLabel(unit)
        self._unit.setMinimumWidth(48)
        self._unit.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self._unit.setStyleSheet("color: #888; font-size: 11px;")

        lay.addWidget(self._lbl)
        lay.addStretch()
        lay.addWidget(self._spin)
        lay.addWidget(self._unit)

    @property
    def value(self) -> float:
        return self._spin.value()

    @value.setter
    def value(self, v: float):
        self._spin.blockSignals(True)
        self._spin.setValue(v)
        self._spin.blockSignals(False)

    def set_enabled(self, enabled: bool):
        self._spin.setEnabled(enabled)


# ────────────────────────────────────────────────────────────────────
# Integer input variant
# ────────────────────────────────────────────────────────────────────

class LabeledIntInput(QWidget):
    """Same layout as LabeledInput but uses QSpinBox (integer)."""

    value_changed = pyqtSignal(int)

    def __init__(
        self,
        label: str,
        unit: str = "",
        min_val: int = 0,
        max_val: int = 10000,
        default: int = 0,
        tooltip: str = "",
        parent=None,
    ):
        super().__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 2, 0, 2)
        lay.setSpacing(8)

        self._lbl = QLabel(label)
        self._lbl.setMinimumWidth(200)
        self._lbl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        if tooltip:
            self._lbl.setToolTip(tooltip)

        self._spin = QSpinBox()
        self._spin.setMinimum(min_val)
        self._spin.setMaximum(max_val)
        self._spin.setValue(default)
        self._spin.setFixedWidth(110)
        self._spin.setAlignment(Qt.AlignmentFlag.AlignRight)
        self._spin.valueChanged.connect(self.value_changed.emit)

        self._unit = QLabel(unit)
        self._unit.setMinimumWidth(48)
        self._unit.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self._unit.setStyleSheet("color: #888; font-size: 11px;")

        lay.addWidget(self._lbl)
        lay.addStretch()
        lay.addWidget(self._spin)
        lay.addWidget(self._unit)

    @property
    def value(self) -> int:
        return self._spin.value()

    @value.setter
    def value(self, v: int):
        self._spin.blockSignals(True)
        self._spin.setValue(v)
        self._spin.blockSignals(False)


# ────────────────────────────────────────────────────────────────────
# Result row (read-only computed output)
# ────────────────────────────────────────────────────────────────────

class ResultRow(QWidget):
    """
    Read-only display row for computed results.
    [ label .............. ] [ bold value ] [ unit ]
    """

    def __init__(self, label: str, unit: str = "", decimals: int = 3, parent=None):
        super().__init__(parent)
        self._decimals = decimals

        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 2, 0, 2)
        lay.setSpacing(8)

        self._lbl = QLabel(label)
        self._lbl.setMinimumWidth(200)
        self._lbl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self._lbl.setStyleSheet("color: #555;")

        self._val = QLabel("—")
        self._val.setMinimumWidth(110)
        self._val.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        font = QFont()
        font.setWeight(QFont.Weight.Medium)
        self._val.setFont(font)

        self._unit = QLabel(unit)
        self._unit.setMinimumWidth(48)
        self._unit.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self._unit.setStyleSheet("color: #888; font-size: 11px;")

        lay.addWidget(self._lbl)
        lay.addStretch()
        lay.addWidget(self._val)
        lay.addWidget(self._unit)

        self.setStyleSheet("background: transparent;")

    def set_value(self, v: float):
        self._val.setText(f"{v:.{self._decimals}f}")

    def set_text(self, s: str):
        self._val.setText(s)

    def set_warning(self, warn: bool):
        color = "#e05c2a" if warn else ""
        self._val.setStyleSheet(f"color: {color};" if color else "")


# ────────────────────────────────────────────────────────────────────
# Base page class
# ────────────────────────────────────────────────────────────────────

class PageBase(QWidget):
    """
    Every design page inherits from PageBase.
    Subclasses implement:
      - _build_ui()  → construct widgets and add to self.layout()
      - _load_from_state()  → populate fields from ds
      - _save_to_state()    → write field values to ds, then recalc + notify
      - refresh()    → called when upstream data changes (connected to signals)
    """

    def __init__(self, ds, title: str = "", parent=None):
        super().__init__(parent)
        self.ds = ds
        self._title = title

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(6)

        # Page title
        if title:
            title_lbl = QLabel(title)
            f = QFont()
            f.setPointSize(13)
            f.setWeight(QFont.Weight.DemiBold)
            title_lbl.setFont(f)
            title_lbl.setContentsMargins(0, 0, 0, 8)
            root.addWidget(title_lbl)
            root.addWidget(HLine())

        self._content_layout = QVBoxLayout()
        self._content_layout.setSpacing(4)
        root.addLayout(self._content_layout)
        root.addStretch()

        self._build_ui()
        self._load_from_state()

    # ------ To be overridden by subclasses ------

    def _build_ui(self):
        """Subclasses add widgets to self._content_layout."""
        pass

    def _load_from_state(self):
        """Populate input widgets from self.ds."""
        pass

    def _save_to_state(self):
        """Write current field values to self.ds and trigger recalc."""
        pass

    def refresh(self):
        """Update displayed results after upstream data changed."""
        pass
