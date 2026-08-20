"""
pages/stubs.py — Placeholder pages for every design stage not yet implemented.

Each stub shows its page title and a "coming soon" message.
Replace each class with a real implementation as the project develops.
"""

from PyQt6.QtWidgets import QLabel, QVBoxLayout
from PyQt6.QtCore    import Qt

from ..widgets.common import PageBase, SectionHeader, ResultRow, HLine


def _make_stub(title: str, description: str):
    """Factory that returns a minimal stub PageBase subclass."""

    class _StubPage(PageBase):
        def __init__(self, ds, res, parent=None):
            super().__init__(ds, res, title=title, parent=parent)

        def _build_ui(self):
            lbl = QLabel(description)
            lbl.setWordWrap(True)
            lbl.setStyleSheet("color: #888; font-style: italic; padding: 12px 0;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            self._content_layout.addWidget(lbl)

        def refresh(self):
            pass

    _StubPage.__name__ = title.replace(" ", "") + "Page"
    return _StubPage


# ------------------------------------------------------------------ #
# One stub per unimplemented page
# ------------------------------------------------------------------ #



