"""
ui/main_window.py — Application main window.

Layout:
  ┌─────────────────────────────────────────────┐
  │  Menu bar                                   │
  ├───────────────┬─────────────────────────────┤
  │               │                             │
  │   Sidebar     │   QStackedWidget            │
  │  (nav tree)   │   (design pages)            │
  │               │                             │
  ├───────────────┴─────────────────────────────┤
  │  Status bar   (efficiency · Vbulk · Ipk)   │
  └─────────────────────────────────────────────┘

  Info tabs (Formula ref, Component DB) open in a floating QDockWidget.
"""

import json
import os
from pathlib import Path

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QListWidget, QListWidgetItem, QStackedWidget,
    QStatusBar, QLabel, QMenuBar, QFileDialog,
    QDockWidget, QTabWidget, QMessageBox, QSplitter,
)
from PyQt6.QtCore  import Qt, QSize
from PyQt6.QtGui   import QAction, QFont, QIcon

from models.flyback_states  import *
from models.calc_engine   import *

from app.pages  import (
    InputSpecsPage, PreDesignPage, StructurePage,
    TransformerPage, TransformerRecapPage, WireSectionsPage,
    LossesPage, SnubberPage, OutputStagePage,
)
from app.tabs.formula_ref_web import FormulaRefTabWeb as FormulaRefTab
from app.tabs.component_db  import ComponentDbTab


# ────────────────────────────────────────────────────────────────────
# Sidebar item data
# ────────────────────────────────────────────────────────────────────

NAV_ITEMS = [
    ("Input specifications",  InputSpecsPage),
    ("Pre-design section",    PreDesignPage),
    ("Switching structure",   StructurePage),
    ("Transformer",           TransformerPage),
    ("Transformer recap",     TransformerRecapPage),
    ("Wire sections",         WireSectionsPage),
    ("Losses",                LossesPage),
    ("Clamp circuit",         SnubberPage),
    ("Output stage",          OutputStagePage),
]


# ────────────────────────────────────────────────────────────────────
# Main window
# ────────────────────────────────────────────────────────────────────

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flyback Designer")
        self.resize(1100, 760)
        self.setMinimumSize(900, 600)

        # Central shared data model
        self.ds = FlybackState()
        self.res = FlybackResults()

        from models.snubber_state import SnubberState, SnubberResults
        self.snubber_ds = SnubberState()
        self.snubber_res = SnubberResults()
        calc_inputPower(self.ds)   # seed computed values from defaults
        calc_bulkCapacitance(self.res, self.ds)

        self._build_menu()
        self._build_central()
        self._build_status_bar()
        self._build_info_dock()
        self._connect_signals()

        # Select first page by default
        self._nav.setCurrentRow(0)

    # ──────────────────────────────────────────────────────────────
    # Menu bar
    # ──────────────────────────────────────────────────────────────

    def _build_menu(self):
        mb = self.menuBar()

        # File
        file_menu = mb.addMenu("&File")

        act_new  = QAction("&New project",  self); act_new.setShortcut("Ctrl+N")
        act_open = QAction("&Open project…", self); act_open.setShortcut("Ctrl+O")
        act_save = QAction("&Save project",  self); act_save.setShortcut("Ctrl+S")
        act_save_as = QAction("Save &as…",  self); act_save_as.setShortcut("Ctrl+Shift+S")
        act_quit = QAction("&Quit",          self); act_quit.setShortcut("Ctrl+Q")

        act_new.triggered.connect(self._new_project)
        act_open.triggered.connect(self._open_project)
        act_save.triggered.connect(self._save_project)
        act_save_as.triggered.connect(self._save_project_as)
        act_quit.triggered.connect(self.close)

        file_menu.addAction(act_new)
        file_menu.addAction(act_open)
        file_menu.addSeparator()
        file_menu.addAction(act_save)
        file_menu.addAction(act_save_as)
        file_menu.addSeparator()
        file_menu.addAction(act_quit)

        # Edit
        edit_menu = mb.addMenu("&Edit")
        act_compile = QAction("Co&mpile", self)
        act_compile.setShortcut("Ctrl+Shift+C")
        act_compile.triggered.connect(self._compile_all)
        edit_menu.addAction(act_compile)
        
        edit_menu.addSeparator()
        
        act_add_comp = QAction("Ajout d'un composant", self)
        act_add_comp.triggered.connect(self._add_component)
        edit_menu.addAction(act_add_comp)
        
        act_del_comp = QAction("Supprimer un composant", self)
        act_del_comp.triggered.connect(self._delete_component)
        edit_menu.addAction(act_del_comp)

        # View
        view_menu = mb.addMenu("&View")
        act_info = QAction("Show &info panel", self, checkable=True, checked=True)
        act_info.setShortcut("Ctrl+I")
        act_info.triggered.connect(self._toggle_info_dock)
        view_menu.addAction(act_info)
        self._act_info = act_info

        # Help
        help_menu = mb.addMenu("&Help")
        act_about = QAction("&About", self)
        act_about.triggered.connect(self._show_about)
        help_menu.addAction(act_about)

        self._project_path: str | None = None

    # ──────────────────────────────────────────────────────────────
    # Central widget: sidebar + stacked pages
    # ──────────────────────────────────────────────────────────────

    def _build_central(self):
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(1)

        # ── Sidebar ─────────────────────────────────────────────
        self._nav = QListWidget()
        self._nav.setFixedWidth(200)
        self._nav.setSpacing(2)
        self._nav.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                color: #F0EBD8;
                border: none;
                outline: none;
                font-family: 'Segoe UI', sans-serif;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #1D2D44;
            }
            QListWidget::item:hover {
                background-color: #1D2D44;
            }
            QListWidget::item:selected {
                background-color: #3E5C76;
                color: #F0EBD8;
                border-left: 4px solid #F0EBD8;
            }
        """)

        # Section label above nav items
        sidebar_widget = QWidget()
        sidebar_widget.setStyleSheet("background-color: #0D1321;")
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        sidebar_header = QLabel("  Design stages")
        sidebar_header.setStyleSheet(
            "color: #748CAB; font-weight: bold; padding: 10px;"
        )
        sidebar_layout.addWidget(sidebar_header)
        sidebar_layout.addWidget(self._nav)

        for label, _ in NAV_ITEMS:
            item = QListWidgetItem(label)
            item.setSizeHint(QSize(0, 36))
            self._nav.addItem(item)

        # ── Stacked pages ────────────────────────────────────────
        self._stack = QStackedWidget()
        self._pages: list[QWidget] = []

        for _, PageClass in NAV_ITEMS:
            if PageClass.__name__ == "SnubberPage":
                page = PageClass(self.snubber_ds, self.snubber_res)
            else:
                page = PageClass(self.ds, self.res)
            self._pages.append(page)
            self._stack.addWidget(page)

        self._nav.currentRowChanged.connect(self._stack.setCurrentIndex)

        splitter.addWidget(sidebar_widget)
        splitter.addWidget(self._stack)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([200, 900])

        self.setCentralWidget(splitter)

    # ──────────────────────────────────────────────────────────────
    # Status bar
    # ──────────────────────────────────────────────────────────────

    def _build_status_bar(self):
        sb = QStatusBar()
        sb.setStyleSheet("background-color: #F0EBD8; color: #0D1321; border-top: 1px solid #748CAB;")
        self.setStatusBar(sb)

        self._sb_vbulk = QLabel()
        self._sb_ipk   = QLabel()
        self._sb_lmag  = QLabel()
        self._sb_eta   = QLabel()

        for lbl in (self._sb_vbulk, self._sb_ipk, self._sb_lmag, self._sb_eta):
            lbl.setStyleSheet("padding: 0 12px; font-size: 13px; font-weight: bold; color: #0D1321;")
            sb.addPermanentWidget(lbl)

        self._refresh_status_bar()

    def _refresh_status_bar(self):
        ds = self.ds
        res = self.res
        self._sb_vbulk.setText(
            f"V_bulk  {res.v_bulk_min_nH_calc:.0f} – {ds.v_in_max:.0f} V")
        self._sb_ipk.setText(f"I_pk  {ds.i_p_max:.2f} A")
        self._sb_lmag.setText(f"L_mag  {ds.Lp:.3f} mH")
        self._sb_eta.setText(f"η  {ds.eta*100:.0f} %")

    # ──────────────────────────────────────────────────────────────
    # Info dock (formula ref + component DB)
    # ──────────────────────────────────────────────────────────────

    def _build_info_dock(self):
        self._info_dock = QDockWidget("Reference", self)
        self._info_dock.setAllowedAreas(
            Qt.DockWidgetArea.RightDockWidgetArea |
            Qt.DockWidgetArea.BottomDockWidgetArea
        )
        self._info_dock.setMinimumWidth(340)

        tabs = QTabWidget()
        tabs.addTab(FormulaRefTab(),   "Formulas")
        self._component_db_tab = ComponentDbTab()
        tabs.addTab(self._component_db_tab,  "Components")
        self._info_dock.setWidget(tabs)

        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self._info_dock)
        self._info_dock.hide()   # hidden by default; Ctrl+I to show

    def _toggle_info_dock(self, checked: bool):
        if checked:
            self._info_dock.show()
        else:
            self._info_dock.hide()

    # ──────────────────────────────────────────────────────────────
    # Signal wiring
    # ──────────────────────────────────────────────────────────────

    def _connect_signals(self):
        """Connect DesignState signals to page refresh methods."""
        ds = self.ds

        def _refresh_all():
            for page in self._pages:
                if hasattr(page, "refresh"):
                    page.refresh()
            self._refresh_status_bar()

        ds.signals.any_changed.connect(_refresh_all)

    # ──────────────────────────────────────────────────────────────
    # File operations
    # ──────────────────────────────────────────────────────────────

    def _new_project(self):
        reply = QMessageBox.question(
            self, "New project",
            "Discard current design and start fresh?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.ds.__init__()          # reset to defaults
            calc_inputPower(self.ds)
            self.ds.signals.any_changed.emit()
            self._project_path = None
            self.setWindowTitle("Flyback Designer — new project")

    def _open_project(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open project", "",
            "Flyback project (*.flyback.json);;All files (*)"
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            new_ds = FlybackState.from_dict(data)
            # Copy fields into existing ds (keeps signal connections)
            for k, v in data.items():
                if hasattr(self.ds, k):
                    setattr(self.ds, k, v)
            calc_inputPower(self.ds)
            self.ds.signals.any_changed.emit()
            self._project_path = path
            self.setWindowTitle(f"Flyback Designer — {Path(path).name}")
        except Exception as e:
            QMessageBox.critical(self, "Open failed", str(e))

    def _save_project(self):
        if self._project_path:
            self._write_project(self._project_path)
        else:
            self._save_project_as()

    def _save_project_as(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save project", "untitled.flyback.json",
            "Flyback project (*.flyback.json);;All files (*)"
        )
        if path:
            self._write_project(path)
            self._project_path = path
            self.setWindowTitle(f"Flyback Designer — {Path(path).name}")

    def _write_project(self, path: str):
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.ds.to_dict(), f, indent=2)
            self.statusBar().showMessage(f"Saved to {path}", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Save failed", str(e))

    # ──────────────────────────────────────────────────────────────
    # About
    # ──────────────────────────────────────────────────────────────

    def _compile_all(self):
        from models.calc_engine import (
            calc_inputPower, calc_bulkCapacitance, calc_preDesign_transformer,
            calc_transformer, calc_flybackState, calc_wire_sections
        )
        from app.pages.pre_design import PreDesignPage

        ds = self.ds
        res = self.res

        try:
            calc_inputPower(ds)
            calc_bulkCapacitance(res, ds)
            if ds.c_bulk == 0:
                ds.c_bulk = PreDesignPage.c_bulk.value * 1e-6
                calc_preDesign_transformer(ds, res)
            else: 
                calc_preDesign_transformer(ds, res)
            calc_transformer(ds, res)
            calc_flybackState(ds, res)
            calc_wire_sections(ds, res)
        except Exception as e:
            QMessageBox.warning(self, "Compilation Error", f"An error occurred during calculations:\n{e}")
            return
            
        ds.notify("all")

        # Refresh the current active page
        idx = self._stack.currentIndex()
        if idx >= 0:
            page = self._stack.widget(idx)
            if hasattr(page, "refresh"):
                page.refresh()
                
        QMessageBox.information(self, "Compile Success", "All calculations finished successfully.")

    def _show_about(self):
        QMessageBox.about(
            self,
            "Flyback Designer",
            "<b>Flyback Power Supply Designer</b><br>"
            "DCM flyback design tool — 85–528 V AC input<br><br>"
            "Built with PyQt6 + Python.<br>"
            "LTSpice / PySpice simulation integration planned."
        )

    def _add_component(self):
        from app.widgets.component_dialogs import AddComponentDialog
        dlg = AddComponentDialog(self)
        if dlg.exec():
            self._refresh_components()
            
    def _delete_component(self):
        from app.widgets.component_dialogs import DeleteComponentDialog
        dlg = DeleteComponentDialog(self)
        if dlg.exec():
            self._refresh_components()
            
    def _refresh_components(self):
        if hasattr(self, "_component_db_tab"):
            self._component_db_tab.refresh()
            
        for page in self._pages:
            # If it's the transformer page, we might want to refresh its combos.
            # We don't have a dedicated refresh_combos(), but _on_geom_changed("All") 
            # will reconstruct the reference combo based on the current component DB.
            if hasattr(page, "_cb_geom") and hasattr(page, "_on_geom_changed"):
                # Save the currently selected ref if possible
                current_ref = page._cb_ref.currentText()
                page._on_geom_changed("All")
                # Try to restore the selected ref
                idx = page._cb_ref.findText(current_ref)
                if idx >= 0:
                    page._cb_ref.setCurrentIndex(idx)

