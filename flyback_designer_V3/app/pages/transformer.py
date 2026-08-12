from PyQt6.QtWidgets import (
    QPushButton, QHBoxLayout, QFrame, QVBoxLayout, QComboBox, QLabel, QLineEdit, QWidget, QMessageBox
)
from PyQt6.QtCore import Qt

from app.widgets.common import PageBase, LabeledInput, SectionHeader
from models.component_manager import ComponentManager

class TransformerPage(PageBase):

    def __init__(self, ds, res, parent=None):
        super().__init__(ds, res, title="Transformer", parent=parent)

    def _build_ui(self):
        cl = self._content_layout

        # ------------------------------------------------------------
        # DATABASE SELECTION
        # ------------------------------------------------------------


        # Geometry Dropdown
        geom_lay = QHBoxLayout()
        geom_lbl = QLabel("Core Geometry")
        geom_lbl.setMinimumWidth(200)
        geom_lbl.setStyleSheet("color: #748CAB;")
        self._cb_geom = QComboBox()
        self._cb_geom.setFixedWidth(180)
        
        # Populate geometries
        geoms = set(core["geometry"] for core in ComponentManager().get_components("cores"))
        self._cb_geom.addItem("All")
        for g in sorted(geoms):
            self._cb_geom.addItem(g)
        self._cb_geom.addItem("Custom")
        
        geom_lay.addWidget(geom_lbl)
        geom_lay.addStretch()
        geom_lay.addWidget(self._cb_geom)

        # Reference Dropdown
        ref_lay = QHBoxLayout()
        ref_lbl = QLabel("Ferrite Reference")
        ref_lbl.setMinimumWidth(200)
        ref_lbl.setStyleSheet("color: #748CAB;")
        self._cb_ref = QComboBox()
        self._cb_ref.setFixedWidth(180)
        
        ref_lay.addWidget(ref_lbl)
        ref_lay.addStretch()
        ref_lay.addWidget(self._cb_ref)
        
        db_center_lay = QHBoxLayout()
        db_center_lay.addStretch()
        db_container = QWidget()
        db_container.setFixedWidth(450)
        db_inner = QVBoxLayout(db_container)
        db_inner.setContentsMargins(0, 0, 0, 0)
        db_inner.addWidget(SectionHeader("Ferrite Database Selection", center=True))
        db_inner.addLayout(geom_lay)
        db_inner.addLayout(ref_lay)
        db_center_lay.addWidget(db_container)
        db_center_lay.addStretch()
        cl.addLayout(db_center_lay)



        # ------------------------------------------------------------
        # CORE CHARACTERISTICS (Editable)
        # ------------------------------------------------------------
        cl.addSpacing(20)

        # Core ref text input (in case they want to override)
        ref_input_lay = QHBoxLayout()
        ref_input_lbl = QLabel("Core Reference (Name)")
        ref_input_lbl.setMinimumWidth(200)
        ref_input_lbl.setStyleSheet("color: #748CAB;")
        self._le_core_ref = QLineEdit()
        self._le_core_ref.setFixedWidth(180)
        self._le_core_ref.setAlignment(Qt.AlignmentFlag.AlignRight)
        ref_input_lay.addWidget(ref_input_lbl)
        ref_input_lay.addStretch()
        ref_input_lay.addWidget(self._le_core_ref)
        # Add a dummy unit label for alignment
        dummy_unit = QLabel("")
        dummy_unit.setMinimumWidth(48)
        ref_input_lay.addWidget(dummy_unit)

        # Numeric characteristics
        self._Ae = LabeledInput("Ae (Effective Area)", "mm²", decimals=2, max_val=10000)
        self._Aw = LabeledInput("Aw (Window Area)", "mm²", decimals=2, max_val=10000)
        self._Ap = LabeledInput("Ap (Area Product)", "mm⁴", decimals=2, max_val=1000000)
        self._Ve = LabeledInput("Ve (Effective Volume)", "mm³", decimals=2, max_val=1000000)
        self._Al = LabeledInput("AL (Inductance Factor)", "nH/t²", decimals=2, max_val=20000)
        self._le = LabeledInput("le (Effective Length)", "mm", decimals=2, max_val=1000)
        self._ln = LabeledInput("Mean Turn Length", "mm", decimals=2, max_val=1000)
        self._weight = LabeledInput("Weight", "g", decimals=2, max_val=10000)
        self._mu_core = LabeledInput("Relative Permeability", "", decimals=2, max_val=50000)
        self._window_length = LabeledInput("Core Window Length", "mm", decimals=2, max_val=1000)
        self._Pv = LabeledInput("Relative Core Losses", "mW/cm³", decimals=2, max_val=10000)

        char_center_lay = QHBoxLayout()
        char_center_lay.addStretch()
        char_container = QWidget()
        char_container.setFixedWidth(450)
        char_inner = QVBoxLayout(char_container)
        char_inner.setContentsMargins(0, 0, 0, 0)
        
        char_inner.addWidget(SectionHeader("Core Characteristics", center=True))
        char_inner.addLayout(ref_input_lay)
        char_inner.addWidget(self._Ae)
        char_inner.addWidget(self._Aw)
        char_inner.addWidget(self._Ap)
        char_inner.addWidget(self._Ve)
        char_inner.addWidget(self._Al)
        char_inner.addWidget(self._le)
        char_inner.addWidget(self._ln)
        char_inner.addWidget(self._weight)
        char_inner.addWidget(self._mu_core)
        char_inner.addWidget(self._window_length)
        char_inner.addWidget(self._Pv)
        
        char_center_lay.addWidget(char_container)
        char_center_lay.addStretch()
        cl.addLayout(char_center_lay)

        # ------------------------------------------------------------
        # BUTTONS
        # ------------------------------------------------------------
        cl.addSpacing(10)
        btn_row1 = QHBoxLayout()
        btn_row1.addStretch()
        
        self._btn_apply = QPushButton("Save Core Data")
        self._btn_apply.setStyleSheet("""
            QPushButton {
                background-color: #3E5C76;
                color: #F0EBD8;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #4A6E8C;
            }
            QPushButton:pressed {
                background-color: #273A56;
            }
        """)
        self._btn_apply.clicked.connect(self._on_save_clicked)
        btn_row1.addWidget(self._btn_apply)
        btn_row1.addStretch()
        cl.addLayout(btn_row1)
        
        cl.addSpacing(10)
        btn_row2 = QHBoxLayout()
        btn_row2.addStretch()
        
        self._btn_calc = QPushButton("Calculate Transformer")
        self._btn_calc.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: #FFFFFF;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self._btn_calc.clicked.connect(self._on_calc_clicked)
        btn_row2.addWidget(self._btn_calc)
        btn_row2.addStretch()
        cl.addLayout(btn_row2)

        # ------------------------------------------------------------
        # COMPUTED OUTPUTS
        # ------------------------------------------------------------
        cl.addSpacing(20)
        
        out_center_lay = QHBoxLayout()
        out_center_lay.addStretch()
        out_container = QWidget()
        out_container.setFixedWidth(450)
        out_inner = QVBoxLayout(out_container)
        out_inner.setContentsMargins(0, 0, 0, 0)
        
        from app.widgets.common import ResultRow
        out_inner.addWidget(SectionHeader("Computed Outputs", center=True))
        
        self._r_np = ResultRow("Primary turns (Np)", "", decimals=2)
        self._r_ns1 = ResultRow("Secondary turns 1 (Ns1)", "", decimals=2)
        self._r_ns2 = ResultRow("Secondary turns 2 (Ns2)", "", decimals=2)
        self._r_naux = ResultRow("Auxiliary turns (Naux)", "", decimals=2)
        self._r_lg = ResultRow("Air gap length (lg)", "mm", decimals=3)
        self._r_fringing = ResultRow("Fringing flux factor", "", decimals=3)
        self._r_lp_real = ResultRow("Real inductance (Lp_real)", "µH", decimals=2)
        self._r_bmax_real = ResultRow("Real flux density (B_max_real)", "T", decimals=4)
        
        from PyQt6.QtGui import QFont
        self._lbl_bmax_status = QLabel("")
        self._lbl_bmax_status.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self._lbl_bmax_status.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        
        out_inner.addWidget(self._r_np)
        out_inner.addWidget(self._r_ns1)
        out_inner.addWidget(self._r_ns2)
        out_inner.addWidget(self._r_naux)
        out_inner.addWidget(self._r_lg)
        out_inner.addWidget(self._r_fringing)
        out_inner.addWidget(self._r_lp_real)
        out_inner.addWidget(self._r_bmax_real)
        out_inner.addWidget(self._lbl_bmax_status)
        
        out_center_lay.addWidget(out_container)
        out_center_lay.addStretch()
        cl.addLayout(out_center_lay)

        # ------------------------------------------------------------
        # CONNECT SIGNALS & INITIALIZE
        # ------------------------------------------------------------
        self._cb_geom.currentTextChanged.connect(self._on_geom_changed)
        self._cb_ref.currentTextChanged.connect(self._on_ref_changed)

        # Initial population of ref dropdown
        self._on_geom_changed("All")

    # ---------------------------------------------------------------- #
    def _on_geom_changed(self, geom: str):
        self._cb_ref.blockSignals(True)
        self._cb_ref.clear()
        
        if geom == "Custom":
            self._cb_ref.addItem("-")
        else:
            for core in ComponentManager().get_components("cores"):
                if geom == "All" or core["geometry"] == geom:
                    self._cb_ref.addItem(core["ref"])
                    
        self._cb_ref.blockSignals(False)
        # Trigger the ref change logic for the first item
        self._on_ref_changed(self._cb_ref.currentText())

    def _on_ref_changed(self, ref: str):
        if not ref or ref == "-":
            return
            
        # Find the core data
        core_data = None
        for core in ComponentManager().get_components("cores"):
            if core["ref"] == ref:
                core_data = core
                break
                
        if core_data:
            self._le_core_ref.setText(core_data["ref"])
            self._Ae.value = core_data["Ae"]
            self._Aw.value = core_data["Aw"]
            self._Ap.value = core_data["Ap"]
            self._Ve.value = core_data["Ve"]
            self._Al.value = core_data["AL"]
            self._le.value = core_data["le"]
            self._ln.value = core_data["ln"]
            self._weight.value = core_data["weight"]
            self._mu_core.value = core_data["mu_core"]
            self._window_length.value = core_data["window_length"]
            self._Pv.value = core_data["Pv"]

    # ---------------------------------------------------------------- #
    def _load_from_state(self):
        ds = self.ds
        self._le_core_ref.setText(ds.core_ref)
        self._Ae.value = ds.Ae
        self._Aw.value = ds.Aw
        self._Ap.value = ds.AeAw_real
        self._Ve.value = ds.Ve
        self._Al.value = ds.Al
        self._le.value = ds.le
        self._ln.value = ds.MTl
        self._weight.value = ds.Wtfe
        self._mu_core.value = ds.mu_core
        self._window_length.value = ds.g
        self._Pv.value = ds.Pv
        self.refresh()

    # ---------------------------------------------------------------- #
    def _save_to_state(self):
        ds = self.ds
        ds.core_ref = self._le_core_ref.text()
        ds.Ae = self._Ae.value
        ds.Aw = self._Aw.value
        ds.AeAw_real = self._Ap.value
        ds.Ve = self._Ve.value
        ds.Al = self._Al.value
        ds.le = self._le.value
        ds.MTl = self._ln.value
        ds.Wtfe = self._weight.value
        ds.mu_core = self._mu_core.value
        ds.g = self._window_length.value
        ds.Pv = self._Pv.value
        
        ds.notify("transformer")
        self.refresh()

    def showEvent(self, event):
        super().showEvent(event)
        from models.calc_engine import calc_transformer
        try:
            calc_transformer(self.ds, self.res)
            self.refresh()
        except Exception:
            pass

    # ---------------------------------------------------------------- #
    def _on_save_clicked(self):
        reply = QMessageBox.question(
            self, 
            "Save Core Data", 
            "Are you sure you want to save these core characteristics?\nThis will overwrite the current values in the Flyback state.",
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
        )
        
        if reply == QMessageBox.StandardButton.Ok:
            self._save_to_state()

    def _on_calc_clicked(self):
        from models.calc_engine import calc_transformer
        try:
            calc_transformer(self.ds, self.res)
        except Exception as e:
            QMessageBox.warning(self, "Calculation Error", f"An error occurred during calculation:\n{e}")
            return
        
        # Force UI update
        self.refresh()

    def refresh(self):
        res = self.res
        ds = self.ds
        
        self._r_np.set_value(res.Np_calc)
        self._r_ns1.set_value(res.Ns1_calc)
        self._r_ns2.set_value(res.Ns2_calc)
        self._r_naux.set_value(res.Naux_calc)
        self._r_lg.set_value(res.lg_calc)
        self._r_fringing.set_value(res.Fringing_calc)
        self._r_lp_real.set_value(res.Lp_real_calc * 1e6) # H to uH
        self._r_bmax_real.set_value(res.B_max_real_calc)
        
        # Compare B_max_real_calc with B_max
        if res.B_max_real_calc > 0:
            if res.B_max_real_calc <= ds.B_max:
                self._lbl_bmax_status.setText(f"OK (≤ {ds.B_max} T)")
                self._lbl_bmax_status.setStyleSheet("color: #4CAF50;") # Green
            else:
                self._lbl_bmax_status.setText(f"Not OK (> {ds.B_max} T)")
                self._lbl_bmax_status.setStyleSheet("color: #F44336;") # Red
        else:
            self._lbl_bmax_status.setText("")
